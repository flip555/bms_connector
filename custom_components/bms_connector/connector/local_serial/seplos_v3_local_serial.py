import serial
import logging
import time
import telnetlib
from typing import List

_LOGGER = logging.getLogger(__name__)


def send_serial_command(commands, port, baudrate=19200, timeout=2):
    """
    Envoie une liste de commandes Modbus RTU sur le port série et retourne
    les réponses sous forme de liste de chaînes hexadécimales.

    Commande = hex string (ex: "010410001200...") → convertie en bytes bruts,
    envoyée sur le port série. Réponse lue après un délai de 500ms.
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
            timeout=1,
        ) as ser:

            for command in commands:
                _LOGGER.debug("Sending: %s", command)

                try:
                    cmd_bytes = bytes.fromhex(command)
                except Exception as e:
                    _LOGGER.error("Invalid command: %s — %s", command, e)
                    responses.append("")
                    continue

                ser.reset_input_buffer()
                ser.write(cmd_bytes)
                _LOGGER.debug("Sent raw (%d bytes): %s", len(cmd_bytes), cmd_bytes.hex())
                time.sleep(0.5)

                raw_bytes = ser.read(ser.in_waiting)
                response = raw_bytes.hex()
                if raw_bytes:
                    _LOGGER.debug("Raw response (%d bytes): %s", len(raw_bytes), response)
                else:
                    _LOGGER.warning("Empty response — BMS may not be responding at configured address")
                responses.append(response)

    except serial.SerialException as e:
        _LOGGER.error("Serial error on %s: %s", port, e)
        return [""] * len(commands)

    return responses


def send_telnet_command(commands: List[str], host: str, port: int = 23, timeout: int = 8) -> List[str]:
    """
    Envoie une liste de commandes Modbus RTU via Telnet et retourne
    les réponses sous forme de liste de chaînes hexadécimales.

    Les commandes sont envoyées en binaire (bytes.fromhex) via Telnet.
    Les réponses sont lues avec détection de silence (900ms).
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
                    _LOGGER.error("Invalid command: %s \u2014 %s", command, e)
                    responses.append("")
                    continue

                tn.write(cmd_bytes)
                _LOGGER.debug("Sent telnet raw (%d bytes): %s", len(cmd_bytes), cmd_bytes.hex())
                time.sleep(0.5)

                # Receive response with silence detection
                messages = []
                last_data = time.monotonic()
                deadline = last_data + timeout

                while time.monotonic() < deadline:
                    try:
                        chunk = tn.read_very_eager()
                        if chunk:
                            messages.append(chunk)
                            last_data = time.monotonic()
                        else:
                            if time.monotonic() - last_data > 0.9:
                                break
                    except EOFError:
                        break

                    time.sleep(0.03)

                raw = b"".join(messages)
                response = raw.hex()
                if raw:
                    _LOGGER.debug("Telnet raw response (%d bytes): %s", len(raw), response)
                else:
                    _LOGGER.warning("Telnet empty response — BMS may not be responding at configured address")
                responses.append(response)

        finally:
            tn.close()

    except Exception as e:
        _LOGGER.error("Telnet error on %s:%s \u2014 %s", host, port, e)
        return [""] * len(commands)

    return responses
