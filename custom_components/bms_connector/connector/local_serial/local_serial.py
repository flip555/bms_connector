import serial
import logging

_LOGGER = logging.getLogger(__name__)

def send_serial_commands(commands, port, baudrate=19200, timeout=2):
    responses = []

    with serial.Serial(port, baudrate=baudrate, timeout=timeout) as ser:
        for command in commands:
            ser.write(command.encode())
            response = ''
            while True:
                char = ser.read(1).decode()
                if char == '\n' or ser.timeout:
                    break
                response += char
            _LOGGER.debug("Response:")
            _LOGGER.debug(response)
            responses.append(response)

    return responses

# Usage example:
# commands = ["command1", "command2", "command3"]
# port = "/dev/ttyUSB0"  # Replace with your serial port
# responses = send_serial_commands(commands, port, baudrate=19200, timeout=2)
# for i, response in enumerate(responses):
#     _LOGGER.debug(f"Response {i + 1}: {response}")
