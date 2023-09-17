import serial
import logging
import time
_LOGGER = logging.getLogger(__name__)

def send_serial_command(commands, port, baudrate=19200, timeout=2):
    responses = []
    _LOGGER.debug(commands)

    with serial.Serial(port, baudrate=baudrate, timeout=timeout) as ser:
        for command in commands:
            _LOGGER.debug(command)
            ser.write(command.encode())
            time.sleep(0.5)
            responses.append(ser.read(ser.in_waiting).decode().replace('\r', '').replace('\n', ''))
    _LOGGER.debug(responses)

    return responses

# Usage example:
# commands = ["command1", "command2", "command3"]
# port = "/dev/ttyUSB0"  # Replace with your serial port
# responses = send_serial_commands(commands, port, baudrate=19200, timeout=2)
# for i, response in enumerate(responses):
#     _LOGGER.debug(f"Response {i + 1}: {response}")
