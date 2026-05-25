"""Modbus RTU serial/Telnet transport for Seplos BMS V3.

RS485 half-duplex handling:
  - reset_input_buffer() before each command
  - Explicit echo consumption after write — some USB-RS485 adapters
    loop back transmitted bytes into the RX buffer.
  - Byte-level frame synchronisation on [addr, 0x04, LEN] to avoid
    confusing echo bytes or stale frames with the real response.
  - CRC-16 Modbus validation on every received frame.
"""

import serial
import logging
import struct
import time
import telnetlib

_LOGGER = logging.getLogger(__name__)

# Known data-byte counts for V3 Modbus responses
# PIA : 18 registers x 2 = 36 = 0x24
# PIB : 26 registers x 2 = 52 = 0x34
_VALID_DATA_LENS = (0x24, 0x34)

# ---------------------------------------------------------------------------
# CRC-16 Modbus
# ---------------------------------------------------------------------------

def _modbus_crc(data: bytes) -> bytes:
    """Return CRC-16 (Modbus) as 2 bytes, little-endian."""
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return struct.pack("<H", crc)


def _frame_crc_ok(frame: bytes) -> bool:
    """Check that the last 2 bytes of *frame* are a valid Modbus CRC."""
    if len(frame) < 4:
        return False
    payload = frame[:-2]
    expected = _modbus_crc(payload)
    return frame[-2:] == expected


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _expected_data_len(command_hex: str) -> int:
    """Derive the expected response data byte count from a Modbus command.

    A Read Input Registers command (0x04) has the register count at
    bytes [4:6] (big-endian). Each register is 2 bytes → data_len = count * 2.
    """
    try:
        raw = bytes.fromhex(command_hex)
        count = (raw[4] << 8) | raw[5]
        return count * 2
    except Exception:
        return 0


def _read_modbus_frame(ser, expected_addr: int, expected_data_len: int,
                       sync_timeout: float = 2.0) -> bytes:
    """Read one Modbus RTU response frame with byte-level synchronisation.

    Phase 1 — byte-by-byte sync on [expected_addr, 0x04]
    Phase 2 — read LEN byte, validate it
    Phase 3 — read DATA + CRC, validate CRC

    Args:
        ser:                Open pySerial object.
        expected_addr:      Expected slave address (e.g. 0x01).
        expected_data_len:  Expected data byte count (e.g. 36 for PIA).
        sync_timeout:       Total time to spend looking for a valid frame.

    Returns:
        The complete frame including addr/cmd/len/data/crc, or b'' if
        no valid frame was found within the timeout.

    """
    deadline = time.monotonic() + sync_timeout

    while time.monotonic() < deadline:
        # Phase 1 — find [addr, 0x04]
        addr_byte = ser.read(1)
        if not addr_byte:
            continue
        if addr_byte[0] != expected_addr:
            continue

        cmd_byte = ser.read(1)
        if not cmd_byte:
            continue
        if cmd_byte[0] != 0x04:
            continue

        # Phase 2 — read LEN
        len_byte = ser.read(1)
        if not len_byte:
            continue
        data_len = len_byte[0]

        # Reject data lengths that aren't valid for this BMS family.
        # This filters out false-positive syncs on echo bytes where
        # [addr, 0x04] appears by coincidence.
        if data_len not in _VALID_DATA_LENS:
            _LOGGER.debug(
                "Sync false-positive — LEN=0x%02X not in %s, resyncing",
                data_len, _VALID_DATA_LENS
            )
            continue

        # If this is a real frame but the wrong type (e.g. PIB when
        # expecting PIA), skip the whole frame and resync.
        if data_len != expected_data_len:
            _LOGGER.debug(
                "Skipping frame LEN=0x%02X (expected 0x%02X) — wrong type",
                data_len, expected_data_len
            )
            ser.read(data_len + 2)   # discard data + CRC
            continue

        # Phase 3 — read data + CRC
        frame = bytes([expected_addr, 0x04, data_len]) + ser.read(data_len + 2)

        if len(frame) < 3 + data_len + 2:
            _LOGGER.warning(
                "Incomplete frame — got %d bytes, expected %d",
                len(frame), 3 + data_len + 2
            )
            continue

        if not _frame_crc_ok(frame):
            _LOGGER.warning(
                "CRC mismatch on frame (%d bytes): %s",
                len(frame), frame.hex()
            )
            continue

        _LOGGER.debug(
            "Valid frame addr=0x%02X LEN=%d (%d bytes): %s",
            expected_addr, data_len, len(frame), frame.hex()
        )
        return frame

    _LOGGER.warning(
        "Timeout — no valid Modbus frame found for addr=0x%02X in %.1fs",
        expected_addr, sync_timeout
    )
    return b""


# ---------------------------------------------------------------------------
# Serial transport
# ---------------------------------------------------------------------------

def send_serial_command(commands, port, baudrate=19200, timeout=2):
    """Send Modbus RTU commands over RS485 and return hex-string responses.

    Each command is sent as raw binary. RS485 half-duplex echo is consumed
    explicitly, then the response is read with frame-level synchronisation
    and CRC validation.

    Args:
        commands:  List of hex strings, each a complete Modbus RTU command.
        port:      Serial device path (e.g. /dev/ttyUSB0).
        baudrate:  Baud rate (default 19200).
        timeout:   Per-command sync timeout in seconds (default 2).

    Returns:
        List of hex strings. One element per command — empty string if a
        valid response could not be obtained.

    """
    responses = []
    _LOGGER.debug("send_serial_command: commands=%s port=%s", commands, port)

    try:
        with serial.Serial(
            port,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.2,          # inter-byte timeout for frame sync
        ) as ser:

            for command in commands:
                _LOGGER.debug("Sending: %s", command)

                try:
                    cmd_bytes = bytes.fromhex(command)
                except Exception as e:
                    _LOGGER.error("Invalid command: %s — %s", command, e)
                    responses.append("")
                    continue

                expected_addr = cmd_bytes[0]
                expected_data_len = _expected_data_len(command)
                _LOGGER.debug(
                    "Expected addr=0x%02X data_len=%d",
                    expected_addr, expected_data_len
                )

                # --- Flush, write, consume echo ---
                ser.reset_input_buffer()
                ser.write(cmd_bytes)
                _LOGGER.debug(
                    "Sent raw (%d bytes): %s",
                    len(cmd_bytes), cmd_bytes.hex()
                )

                # Temporarily shorten timeout so echo read doesn't
                # block for long if the adapter suppresses echo.
                saved_timeout = ser.timeout
                ser.timeout = 0.15
                echo = ser.read(len(cmd_bytes))
                ser.timeout = saved_timeout

                if len(echo) == len(cmd_bytes):
                    _LOGGER.debug(
                        "Echo consumed (%d bytes) — adapter loops back TX",
                        len(echo)
                    )
                elif len(echo) > 0:
                    _LOGGER.debug(
                        "Partial echo (%d/%d bytes)", len(echo), len(cmd_bytes)
                    )
                else:
                    _LOGGER.debug(
                        "No echo — adapter suppresses RX loopback"
                    )

                # --- Read Modbus response frame ---
                raw = _read_modbus_frame(ser, expected_addr, expected_data_len)

                if not raw:
                    _LOGGER.warning(
                        "No valid response for addr=0x%02X", expected_addr
                    )
                    responses.append("")
                else:
                    _LOGGER.debug(
                        "Response OK addr=0x%02X (%d bytes): %s",
                        expected_addr, len(raw), raw.hex()
                    )
                    responses.append(raw.hex())

                # Gap between commands — gives the BMS time to process
                time.sleep(0.3)

    except serial.SerialException as e:
        _LOGGER.error("Serial error on %s: %s", port, e)
        return [""] * len(commands)

    _LOGGER.debug("Final responses: %s", responses)
    return responses


# ---------------------------------------------------------------------------
# Telnet transport
# ---------------------------------------------------------------------------

def send_telnet_command(commands: list[str], host: str, port: int = 23,
                        timeout: int = 8) -> list[str]:
    """Send Modbus RTU commands via Telnet and return hex-string responses.

    Telnet is full-duplex so there is no RS485 echo to consume. Responses
    are read with silence detection (900ms of no data = end of frame).

    Args:
        commands:  List of hex strings, each a complete Modbus RTU command.
        host:      Telnet server address.
        port:      Telnet server port (default 23).
        timeout:   Per-command silence-detection timeout (default 8s).

    Returns:
        List of hex strings. One element per command — empty string if
        a response could not be obtained.

    """
    responses = []
    _LOGGER.debug("send_telnet_command: connecting to %s:%s", host, port)

    try:
        tn = telnetlib.Telnet(host, port, timeout=5)

        try:
            for command in commands:
                _LOGGER.debug("Sending: %s", command)

                try:
                    cmd_bytes = bytes.fromhex(command)
                except Exception as e:
                    _LOGGER.error("Invalid command: %s — %s", command, e)
                    responses.append("")
                    continue

                tn.write(cmd_bytes)
                _LOGGER.debug("Sent telnet raw (%d bytes): %s", len(cmd_bytes), cmd_bytes.hex())
                time.sleep(0.5)

                # Receive with silence detection
                chunks = []
                last_data = time.monotonic()
                deadline = last_data + timeout

                while time.monotonic() < deadline:
                    try:
                        chunk = tn.read_very_eager()
                        if chunk:
                            chunks.append(chunk)
                            last_data = time.monotonic()
                        else:
                            if time.monotonic() - last_data > 0.9:
                                break
                    except EOFError:
                        break

                    time.sleep(0.03)

                raw = b"".join(chunks)
                response = raw.hex()
                if raw:
                    _LOGGER.debug("Telnet response (%d bytes): %s", len(raw), response)
                else:
                    _LOGGER.warning("Telnet empty response — check wiring and BMS address")
                responses.append(response)

        finally:
            tn.close()

    except Exception as e:
        _LOGGER.error("Telnet error on %s:%s — %s", host, port, e)
        return [""] * len(commands)

    return responses
