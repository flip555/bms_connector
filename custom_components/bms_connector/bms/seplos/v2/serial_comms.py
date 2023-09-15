import serial
import time
import logging
import serial
_LOGGER = logging.getLogger(__name__)

def send_serial_command(command: str, port: str, baudrate: int = 19200, timeout: int = 2) -> str:
    with serial.Serial(port, baudrate=baudrate, timeout=timeout) as ser:
        _LOGGER.debug("Serial Comms Sending: %s", command)
        _LOGGER.debug("Serial Comms Port: %s", port)

        ser.write(command.encode())
        time.sleep(0.5)

        response = ser.read(ser.in_waiting).decode().replace('\r', '').replace('\n', '')
        _LOGGER.debug("Serial Comms Received: %s", response)
        return response