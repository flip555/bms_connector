# Decode 51H data for Seplos V2 BMS
# These settings appear to relate to hardware versions and CAN bus configuration
# Encoded Data: Full HEX string: 20004600c040313130312d5350373620100443414e3a56696374726f6e202020202020202020f098
# Length in decimal: 305
# SOI: 20
# VER: 00
# ADR: 46
# CID1: 00
# CID2: c0
# LENGTH: 3131 (In Decimal: 305)
# Device Name: SP76
# Software/Hardware Version: 101
# Manufacturer Name: CAN: Victron
# CHKSUM: f098

import serial
import time
import logging
import serial
_LOGGER = logging.getLogger(__name__)

def hex_to_ascii(hex_str):
    ascii_str = ""
    for i in range(0, len(hex_str), 2):
        ascii_str += chr(int(hex_str[i:i+2], 16))
    return ascii_str
def decode_message(message_bytes):
    # Convert bytes to a hex string
    message_hex_str = message_bytes.hex()
    
    # Print the entire hex string for debugging
    print(f"Full HEX string: {message_hex_str}")
    
    # Slice the hex string to extract fields (adjust indices accordingly)
    SOI = message_hex_str[0:2]
    VER = message_hex_str[2:4]
    ADR = message_hex_str[4:6]
    CID1 = message_hex_str[6:8]
    CID2 = message_hex_str[8:10]
    LENGTH = message_hex_str[12:16]
    # Attempt to convert LENGTH to decimal
    try:
        length_in_dec = int(LENGTH, 16) & 0x0FFF
        print(f"Length in decimal: {length_in_dec}")
    except ValueError as e:
        print(f"Failed to convert LENGTH to decimal: {e}")
    
    INFO = message_hex_str[14:-4]
    CHKSUM = message_hex_str[-4:]
    
    # Getting data from INFO
    device_name = hex_to_ascii(INFO[8:16])  # Extracting bytes representing "SP76"
    software_version = hex_to_ascii(INFO[0:6])  # Extracting bytes representing "10E"
    manufacturer_name = hex_to_ascii(INFO[16:])  # Extracting bytes representing "CAN:Victron"
    
    # Printing the decoded fields
    print(f"SOI: {SOI}")
    print(f"VER: {VER}")
    print(f"ADR: {ADR}")
    print(f"CID1: {CID1}")
    print(f"CID2: {CID2}")
    print(f"LENGTH: {LENGTH} (In Decimal: {length_in_dec})")
    print(f"Device Name: {device_name.strip()}")
    print(f"Software/Hardware? Version: {software_version.strip()}")
    print(f"Manufacturer Name: {manufacturer_name.strip()}")
    print(f"CHKSUM: {CHKSUM}")
    
def send_serial_command(command: str, port: str, baudrate: int = 19200, timeout: int = 2) -> str:
    with serial.Serial(port, baudrate=baudrate, timeout=timeout) as ser:
        print("Serial Comms Sending: %s", command)
        print("Serial Comms Port: %s", port)

        ser.write(command.encode())
        time.sleep(0.5)

        response = ser.read(ser.in_waiting).decode().replace('\r', '').replace('\n', '')
        if response.startswith("~"):
            response = response[1:]
        print("Serial Comms Received: %s", response)
        return response
        


decode_message(bytes.fromhex(send_serial_command("~20004651E00200FD37\r", "/dev/ttyUSB0", 19200, 2)))
