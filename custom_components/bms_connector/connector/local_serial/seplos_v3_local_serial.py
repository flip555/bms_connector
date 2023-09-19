import serial
import logging
import time
_LOGGER = logging.getLogger(__name__)

def send_serial_command(commands, port, baudrate=19200, timeout=2):
    responses = []
    _LOGGER.debug(commands)

    with serial.Serial(port, baudrate=19200, parity=serial.PARITY_NONE, stopbits=1, bytesize=8, timeout=1) as ser:
        for command in commands:
            _LOGGER.debug(command)
            ser.write(bytes.fromhex(command))
            time.sleep(0.5)
            response = ser.read(ser.in_waiting).hex()
            responses.append(response)
            _LOGGER.debug(response)

    return responses

# Usage example:
# commands = ["command1", "command2", "command3"]
# port = "/dev/ttyUSB0"  # Replace with your serial port
# responses = send_serial_commands(commands, port, baudrate=19200, timeout=2)
# for i, response in enumerate(responses):
#     _LOGGER.debug(f"Response {i + 1}: {response}")
