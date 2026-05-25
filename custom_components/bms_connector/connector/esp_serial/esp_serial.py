import socket
import logging

# Configure the logger
_LOGGER = logging.getLogger(__name__)

def communicate_with_esphome(ip, port, commands, timeout):
    responses = []

    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the ESPHome device
        client_socket.connect((ip, port))
        _LOGGER.debug("Connected to %s:%s", ip, port)

        for command in commands:
            # Send the command to the device
            client_socket.sendall(command.encode())

            # Set a timeout for receiving the response
            client_socket.settimeout(timeout)

            # Read and log the response
            response = client_socket.recv(1024).decode('utf-8')
            _LOGGER.debug("Response:")
            _LOGGER.debug(response)

            responses.append(response)

    except KeyboardInterrupt:
        _LOGGER.debug("Connection closed by user.")
    except TimeoutError:
        _LOGGER.debug("Timeout (%s seconds) exceeded while waiting for a response.", timeout)
    except Exception as e:
        _LOGGER.debug("An error occurred: %s", e)
    finally:
        # Close the socket when done
        client_socket.close()
        _LOGGER.debug("Connection closed.")

    return responses

# Usage example:
# commands = ["command1\n", "command2\n", "command3\n"]
# responses = communicate_with_esphome("192.168.1.100", 3232, commands, 10)
# for i, response in enumerate(responses):
#     _LOGGER.debug(f"Response {i + 1}: {response}")
