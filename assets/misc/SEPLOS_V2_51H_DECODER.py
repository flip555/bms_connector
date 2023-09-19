# Decode 51H data for Seplos V2 BMS
# These settings appear to relate to hardware versions and CAN bus configuration
# Serial Comms Sending: ~20004651E00200FD37
# Serial Comms Received: 20004600C040313130312D5350373620100443414E3A56696374726F6E202020202020202020F098
# Decoded Data:
# Device Name: 1101-SP76
# Software Version: 16.4
# Manufacturer Name: CAN:Victron

import serial
import time
import logging

_LOGGER = logging.getLogger(__name__)

class BMSData:
    pass

def decode_47H_response(hex_string):
    result = BMSData()
    hex_string = bytes.fromhex(hex_string)
    if len(hex_string) < 10:
        return None
    device_name_bytes = hex_string[6:16]
    software_version_bytes = hex_string[16:18]
    manufacturer_name_bytes = hex_string[18:38]

    # Convert bytes to ASCII strings
    result.device_name = device_name_bytes.decode('ascii')
    
    # Interpret the software version correctly
    software_version = int.from_bytes(software_version_bytes, byteorder='big') / 1000 * 4  # Really unsure if this is correct ... my version is 16.4 so * 4 made 4.1 16.4
    result.software_version = "{:.1f}".format(software_version)

    result.manufacturer_name = manufacturer_name_bytes.decode('ascii')

    return result

def send_serial_command(command: str, port: str, baudrate: int = 19200, timeout: int = 2) -> str:
    with serial.Serial(port, baudrate=baudrate, timeout=timeout) as ser:
        print("Serial Comms Sending:", command)
        ser.write(command.encode())
        time.sleep(0.5)
        response = ser.read(ser.in_waiting).decode().replace('\r', '').replace('\n', '')
        if response.startswith("~"):
            response = response[1:]
        print("Serial Comms Received:", response)
        decoded_data = decode_47H_response(response)
        if decoded_data:
            print("Decoded Data:")
            print("Device Name:", decoded_data.device_name)
            print("Software Version:", decoded_data.software_version)
            print("Manufacturer Name:", decoded_data.manufacturer_name)

send_serial_command("~20004651E00200FD37\r", "/dev/ttyUSB0", 19200, 2)
