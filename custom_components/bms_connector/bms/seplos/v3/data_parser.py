"""Modbus RTU response parser for Seplos BMS V3 (PIA / PIB tables).

PIA  — registers 0x1000–0x1011 (18 regs) — pack-level data
PIB  — registers 0x1100–0x1119 (26 regs) — cell voltages + temperatures
"""

import struct
import logging

_LOGGER = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# CRC-16 Modbus
# ---------------------------------------------------------------------------

def modbus_crc(data: bytes) -> bytes:
    """Calculate the Modbus RTU CRC (little-endian, 2 bytes)."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return struct.pack('<H', crc)


def verify_crc(frame_hex: str) -> bool:
    """Validate CRC for an entire Modbus frame given as hex string."""
    try:
        raw = bytes.fromhex(frame_hex)
        if len(raw) < 4:
            return False
        payload = raw[:-2]
        received_crc = raw[-2:]
        expected_crc = modbus_crc(payload)
        return received_crc == expected_crc
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Command construction
# ---------------------------------------------------------------------------

def build_read_command(addr: int, register: int, count: int) -> str:
    """Build a Modbus RTU 0x04 (Read Input Registers) command with CRC.

    Args:
        addr:     Slave address (0x01–0x7F).
        register: Start register address (e.g. 0x1000 for PIA).
        count:    Number of registers to read.

    Returns:
        Complete command as a hex string (without spaces), CRC included.

    """
    payload = bytes([addr, 0x04]) + struct.pack('>HH', register, count)
    crc = modbus_crc(payload)
    cmd = (payload + crc).hex()
    _LOGGER.debug("Modbus command built: %s (addr=0x%02X, reg=0x%04X, count=%d)",
                  cmd, addr, register, count)
    return cmd


def build_commands_for_address(battery_addr: int) -> list:
    """Build PIA and PIB commands for a given battery address.

    PIA : register 0x1000, 18 registers  (0x12) — pack data
    PIB : register 0x1100, 26 registers  (0x1A) — cell voltages + temps
    """
    cmd_pia = build_read_command(battery_addr, 0x1000, 0x12)
    cmd_pib = build_read_command(battery_addr, 0x1100, 0x1A)
    _LOGGER.debug("Commands for battery 0x%02X: PIA=%s | PIB=%s",
                  battery_addr, cmd_pia, cmd_pib)
    return [cmd_pia, cmd_pib]


# ---------------------------------------------------------------------------
# BMS address discovery
# ---------------------------------------------------------------------------

# Valid PIA response: addr(1) + 0x04(1) + byte_count(1=0x24) + data(36) + crc(2) = 41 bytes
_PIA_RESPONSE_BYTES = 41
# Hex chars for a valid PIA response: 41 bytes × 2 = 82 hex chars
_PIA_RESPONSE_HEX_LEN = _PIA_RESPONSE_BYTES * 2


def discover_bms_address(send_fn, port, baudrate=19200, max_addr=0x0F):
    """Scan Modbus addresses 0x00–max_addr to find a BMS.

    Sends a PIA command to each address and validates the response
    (CRC, frame structure, expected byte count).

    Args:
        send_fn:  Callable (commands, port, baudrate) -> [response_hex_str, ...]
        port:     Serial port path (e.g. "/dev/ttyUSB0")
        baudrate: Baud rate
        max_addr: Highest address to scan (default 0x0F)

    Returns:
        (int | None) Found address, or None if no BMS responds.

    """
    _LOGGER.info("Scanning for BMS on %s (addresses 0x00–0x%02X)...", port, max_addr)

    for addr in range(max_addr + 1):
        cmd = build_read_command(addr, 0x1000, 0x12)
        responses = send_fn([cmd], port, baudrate)

        if not responses or not responses[0]:
            _LOGGER.debug("Address 0x%02X: no response", addr)
            continue

        response = responses[0]

        if len(response) < _PIA_RESPONSE_HEX_LEN:
            _LOGGER.debug(
                "Address 0x%02X: response too short (%d chars, expected %d)",
                addr, len(response), _PIA_RESPONSE_HEX_LEN
            )
            continue

        # First byte should match the address we queried
        if not response.startswith(f"{addr:02x}"):
            _LOGGER.debug(
                "Address 0x%02X: response starts with unexpected addr byte 0x%s",
                addr, response[:2]
            )
            continue

        # Function code must be 0x04
        if response[2:4] != "04":
            _LOGGER.debug(
                "Address 0x%02X: unexpected function code 0x%s",
                addr, response[2:4]
            )
            continue

        # Byte count must be 0x24 (36 data bytes for PIA)
        if response[4:6] != "24":
            _LOGGER.debug(
                "Address 0x%02X: unexpected byte_count 0x%s",
                addr, response[4:6]
            )
            continue

        # CRC validation
        if not verify_crc(response):
            _LOGGER.debug("Address 0x%02X: CRC invalid", addr)
            continue

        _LOGGER.info(
            "BMS found at address 0x%02X — valid PIA response (%d chars)",
            addr, len(response)
        )
        return addr

    _LOGGER.warning(
        "No BMS found on %s scanning addresses 0x00–0x%02X",
        port, max_addr
    )
    return None


# ---------------------------------------------------------------------------
# Type conversion
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def convert_bytes_to_data(data_type: str, byte1: int, byte2: int):
    """Convert two bytes (MSB, LSB) to a typed value.

    Args:
        data_type: "UINT16" or "INT16"
        byte1:     Most-significant byte.
        byte2:     Least-significant byte.

    """
    if data_type == "UINT16":
        return (byte1 << 8) | byte2
    elif data_type == "INT16":
        value = (byte1 << 8) | byte2
        if value & 0x8000:
            value -= 0x10000
        return value
    return None


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

class V3PIATableData:
    """Pack Info A — general battery pack data."""

    def __init__(self):
        self.pack_voltage = 0                # V
        self.current = 0                     # A  (negative = discharge)
        self.remaining_capacity = 0          # Ah
        self.total_capacity = 0              # Ah
        self.total_discharge_capacity = 0    # Ah  (cumulative)
        self.soc = 0                         # %
        self.soh = 0                         # %
        self.cycle = 0                       # cycles
        self.avg_cell_voltage = 0            # V
        self.avg_cell_temperature = 0        # °C
        self.max_cell_voltage = 0            # V
        self.min_cell_voltage = 0            # V
        self.max_cell_temperature = 0        # °C
        self.min_cell_temperature = 0        # °C
        self.max_discharge_current = 0       # A
        self.max_charge_current = 0          # A

    def __str__(self):
        return (
            f"pack_voltage={self.pack_voltage}V, "
            f"current={self.current}A, "
            f"remaining={self.remaining_capacity}Ah, "
            f"total={self.total_capacity}Ah, "
            f"discharge_total={self.total_discharge_capacity}Ah, "
            f"soc={self.soc}%, soh={self.soh}%, cycle={self.cycle}, "
            f"avg_cell_v={self.avg_cell_voltage}V, "
            f"avg_cell_t={self.avg_cell_temperature}°C, "
            f"max_cell_v={self.max_cell_voltage}V, "
            f"min_cell_v={self.min_cell_voltage}V, "
            f"max_cell_t={self.max_cell_temperature}°C, "
            f"min_cell_t={self.min_cell_temperature}°C"
        )


class V3PIBTableData:
    """Pack Info B — cell voltages and temperatures."""

    def __init__(self):
        # Cell voltages (V)
        self.cell1_voltage = 0
        self.cell2_voltage = 0
        self.cell3_voltage = 0
        self.cell4_voltage = 0
        self.cell5_voltage = 0
        self.cell6_voltage = 0
        self.cell7_voltage = 0
        self.cell8_voltage = 0
        self.cell9_voltage = 0
        self.cell10_voltage = 0
        self.cell11_voltage = 0
        self.cell12_voltage = 0
        self.cell13_voltage = 0
        self.cell14_voltage = 0
        self.cell15_voltage = 0
        self.cell16_voltage = 0
        # Cell temperatures (°C)
        self.cell_temperature_1 = 0
        self.cell_temperature_2 = 0
        self.cell_temperature_3 = 0
        self.cell_temperature_4 = 0
        # Environment temperatures (°C)
        self.environment_temperature = 0
        self.power_temperature = 0

    def __str__(self):
        cells = ", ".join(
            f"cell{i}_v={getattr(self, f'cell{i}_voltage')}V"
            for i in range(1, 17)
        )
        return (
            f"{cells}, "
            f"temp1={self.cell_temperature_1}°C, "
            f"temp2={self.cell_temperature_2}°C, "
            f"temp3={self.cell_temperature_3}°C, "
            f"temp4={self.cell_temperature_4}°C, "
            f"env_temp={self.environment_temperature}°C, "
            f"pwr_temp={self.power_temperature}°C"
        )


# ---------------------------------------------------------------------------
# PIA decoding
# ---------------------------------------------------------------------------

def decode_pia_table(response: str):
    """Decode the Modbus response to a PIA command (registers 0x1000–0x1011).

    Frame layout:
        [addr, 0x04, LEN, DATA..., CRC_lo, CRC_hi]

    Register layout (per Seplos V3 Modbus spec):
        0x1000  pack_voltage             UINT16  10mV    → × 0.01   → V
        0x1001  current                  INT16   10mA    → × 0.01   → A
        0x1002  remaining_capacity       UINT16  10mAh   → × 0.01   → Ah
        0x1003  total_capacity           UINT16  10mAh   → × 0.01   → Ah
        0x1004  total_discharge_capacity UINT16  10Ah    → × 10     → Ah
        0x1005  soc                      UINT16  0.1%    → × 0.1    → %
        0x1006  soh                      UINT16  0.1%    → × 0.1    → %
        0x1007  cycle                    UINT16  1
        0x1008  avg_cell_voltage         UINT16  1mV     → × 0.001  → V
        0x1009  avg_cell_temperature     UINT16  0.1K    → × 0.1 − 273.15 → °C
        0x100A  max_cell_voltage         UINT16  1mV     → × 0.001  → V
        0x100B  min_cell_voltage         UINT16  1mV     → × 0.001  → V
        0x100C  max_cell_temperature     UINT16  0.1K    → × 0.1 − 273.15 → °C
        0x100D  min_cell_temperature     UINT16  0.1K    → × 0.1 − 273.15 → °C
        0x100E  (reserved)
        0x100F  max_discharge_current    UINT16  1A
        0x1010  max_charge_current       UINT16  1A
        0x1011  (reserved)
    """
    if not response:
        _LOGGER.warning("decode_pia_table: empty response")
        return None

    # Strip possible legacy '~' prefix
    if response.startswith("~"):
        response = response[1:]

    # CRC check — reject immediately on failure
    if not verify_crc(response):
        _LOGGER.error("decode_pia_table: CRC invalid for frame %s — discarding", response)
        return None

    try:
        raw = bytes.fromhex(response)
    except ValueError as e:
        _LOGGER.error("decode_pia_table: unable to decode hex frame: %s", e)
        return None

    # Minimum length: 3 header + 36 data + 2 CRC = 41 bytes
    if len(raw) < 41:
        _LOGGER.warning("decode_pia_table: frame too short (%d bytes, expected >= 41)", len(raw))
        return None

    data = raw[3:-2]  # skip header, drop CRC
    pia = V3PIATableData()

    try:
        pia.pack_voltage             = convert_bytes_to_data("UINT16", data[0],  data[1])  * 0.01
        pia.current                  = convert_bytes_to_data("INT16",  data[2],  data[3])  * 0.01
        pia.remaining_capacity       = convert_bytes_to_data("UINT16", data[4],  data[5])  * 0.01
        pia.total_capacity           = convert_bytes_to_data("UINT16", data[6],  data[7])  * 0.01
        # Spec says unit = 10Ah for total_discharge_capacity
        pia.total_discharge_capacity = convert_bytes_to_data("UINT16", data[8],  data[9])  * 10
        pia.soc                      = convert_bytes_to_data("UINT16", data[10], data[11]) * 0.1
        pia.soh                      = convert_bytes_to_data("UINT16", data[12], data[13]) * 0.1
        pia.cycle                    = convert_bytes_to_data("UINT16", data[14], data[15])
        pia.avg_cell_voltage         = convert_bytes_to_data("UINT16", data[16], data[17]) * 0.001
        pia.avg_cell_temperature     = convert_bytes_to_data("UINT16", data[18], data[19]) * 0.1 - 273.15
        pia.max_cell_voltage         = convert_bytes_to_data("UINT16", data[20], data[21]) * 0.001
        pia.min_cell_voltage         = convert_bytes_to_data("UINT16", data[22], data[23]) * 0.001
        pia.max_cell_temperature     = convert_bytes_to_data("UINT16", data[24], data[25]) * 0.1 - 273.15
        pia.min_cell_temperature     = convert_bytes_to_data("UINT16", data[26], data[27]) * 0.1 - 273.15
        # byte[28,29] = reserved 0x100E
        pia.max_discharge_current    = convert_bytes_to_data("UINT16", data[30], data[31])
        pia.max_charge_current       = convert_bytes_to_data("UINT16", data[32], data[33])
        # byte[34,35] = reserved 0x1011
    except (IndexError, TypeError) as e:
        _LOGGER.error("decode_pia_table: index/type error: %s", e)
        return None

    _LOGGER.debug("PIA decoded: %s", pia)
    return pia


# ---------------------------------------------------------------------------
# PIB decoding
# ---------------------------------------------------------------------------

def decode_pib_table(response: str):
    """Decode the Modbus response to a PIB command (registers 0x1100–0x1119).

    Frame layout:
        [addr, 0x04, LEN, DATA..., CRC_lo, CRC_hi]

    Register layout:
        0x1100–0x110F  cell voltages 1–16       UINT16  1mV    → × 0.001 → V
        0x1110–0x1113  cell temperatures 1–4     UINT16  0.1K   → × 0.1 − 273.15 → °C
        0x1114–0x1117  (reserved)
        0x1118         environment temperature   UINT16  0.1K   → × 0.1 − 273.15 → °C
        0x1119         power temperature          UINT16  0.1K   → × 0.1 − 273.15 → °C
    """
    if not response:
        _LOGGER.warning("decode_pib_table: empty response")
        return None

    if response.startswith("~"):
        response = response[1:]

    # CRC check — reject immediately on failure
    if not verify_crc(response):
        _LOGGER.error("decode_pib_table: CRC invalid for frame %s — discarding", response)
        return None

    try:
        raw = bytes.fromhex(response)
    except ValueError as e:
        _LOGGER.error("decode_pib_table: unable to decode hex frame: %s", e)
        return None

    # Minimum length: 3 header + 52 data + 2 CRC = 57 bytes
    if len(raw) < 57:
        _LOGGER.warning("decode_pib_table: frame too short (%d bytes, expected >= 57)", len(raw))
        return None

    data = raw[3:-2]
    pib = V3PIBTableData()

    try:
        # Cell voltages (registers 0x1100–0x110F, 16 cells)
        pib.cell1_voltage  = convert_bytes_to_data("UINT16", data[0],  data[1])  * 0.001
        pib.cell2_voltage  = convert_bytes_to_data("UINT16", data[2],  data[3])  * 0.001
        pib.cell3_voltage  = convert_bytes_to_data("UINT16", data[4],  data[5])  * 0.001
        pib.cell4_voltage  = convert_bytes_to_data("UINT16", data[6],  data[7])  * 0.001
        pib.cell5_voltage  = convert_bytes_to_data("UINT16", data[8],  data[9])  * 0.001
        pib.cell6_voltage  = convert_bytes_to_data("UINT16", data[10], data[11]) * 0.001
        pib.cell7_voltage  = convert_bytes_to_data("UINT16", data[12], data[13]) * 0.001
        pib.cell8_voltage  = convert_bytes_to_data("UINT16", data[14], data[15]) * 0.001
        pib.cell9_voltage  = convert_bytes_to_data("UINT16", data[16], data[17]) * 0.001
        pib.cell10_voltage = convert_bytes_to_data("UINT16", data[18], data[19]) * 0.001
        pib.cell11_voltage = convert_bytes_to_data("UINT16", data[20], data[21]) * 0.001
        pib.cell12_voltage = convert_bytes_to_data("UINT16", data[22], data[23]) * 0.001
        pib.cell13_voltage = convert_bytes_to_data("UINT16", data[24], data[25]) * 0.001
        pib.cell14_voltage = convert_bytes_to_data("UINT16", data[26], data[27]) * 0.001
        pib.cell15_voltage = convert_bytes_to_data("UINT16", data[28], data[29]) * 0.001
        pib.cell16_voltage = convert_bytes_to_data("UINT16", data[30], data[31]) * 0.001

        # Cell temperatures (registers 0x1110–0x1113)
        pib.cell_temperature_1 = convert_bytes_to_data("UINT16", data[32], data[33]) * 0.1 - 273.15
        pib.cell_temperature_2 = convert_bytes_to_data("UINT16", data[34], data[35]) * 0.1 - 273.15
        pib.cell_temperature_3 = convert_bytes_to_data("UINT16", data[36], data[37]) * 0.1 - 273.15
        pib.cell_temperature_4 = convert_bytes_to_data("UINT16", data[38], data[39]) * 0.1 - 273.15

        # Registers 0x1114–0x1117 are reserved (bytes 40–47)

        # Environment temperature (register 0x1118)
        if len(data) >= 50:
            pib.environment_temperature = convert_bytes_to_data("UINT16", data[48], data[49]) * 0.1 - 273.15

        # Power temperature (register 0x1119)
        if len(data) >= 52:
            pib.power_temperature = convert_bytes_to_data("UINT16", data[50], data[51]) * 0.1 - 273.15

    except (IndexError, TypeError) as e:
        _LOGGER.error("decode_pib_table: index/type error during decoding: %s", e)
        return None

    _LOGGER.debug("PIB decoded: %s", pib)
    return pib


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def extract_data_from_message(msg, telemetry_requested=True, teledata_requested=True,
                               debug=True, config_battery_address=None):
    """Parse PIA + PIB Modbus responses and return structured data.

    Args:
        msg:                     List of 2 hex strings (PIA response, PIB response).
        telemetry_requested:     Legacy — unused.
        teledata_requested:      Legacy — unused.
        debug:                   Legacy — unused.
        config_battery_address:  Battery address for display (int or str).

    Returns:
        Tuple (battery_address, pia_data, pib_data, [], []).

    """
    # Normalise address for display
    if isinstance(config_battery_address, int):
        address_string = f"0x{config_battery_address:02X}"
    else:
        address_string = str(config_battery_address) if config_battery_address else "unknown"

    pia_data = None
    pib_data = None

    if not msg or len(msg) < 2:
        _LOGGER.error("extract_data_from_message: msg must contain at least 2 frames")
        return address_string, pia_data, pib_data, [], []

    for idx, response in enumerate(msg):
        if isinstance(response, str) and response.startswith("~"):
            response = response[1:]

        _LOGGER.debug("Frame %d received: %s", idx, response)

        if idx == 0:
            pia_data = decode_pia_table(response)
            if pia_data is None:
                _LOGGER.error("PIA decoding failed for battery %s", address_string)
            else:
                _LOGGER.debug("PIA OK: %s", pia_data)
        elif idx == 1:
            pib_data = decode_pib_table(response)
            if pib_data is None:
                _LOGGER.error("PIB decoding failed for battery %s", address_string)
            else:
                _LOGGER.debug("PIB OK: %s", pib_data)

    return address_string, pia_data, pib_data, [], []
