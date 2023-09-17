import logging
_LOGGER = logging.getLogger(__name__)
class BMSSystemDetails:
    def __init__(self):
        self.device_name = 0
        self.software_version = 0
        self.manufacturer_name = 0
    def __str__(self):
        return (
            f"device_name: {self.device_name}, "
            f"software_version: {self.software_version}, "
            f"manufacturer_name: {self.manufacturer_name} "
        )
        
def hex_to_ascii(hex_str):
    """Converts a hexadecimal string to an ASCII string."""
    hex_values = hex_str.split()
    ascii_str = ''.join(chr(int(hex_value, 16)) for hex_value in hex_values)
    return ascii_str

def decode_fiveone(message_bytes):
    result = BMSSystemDetails()

    message_hex_str = message_bytes

    SOI = message_hex_str[0:2]
    VER = message_hex_str[2:4]
    ADR = message_hex_str[4:6]
    CID1 = message_hex_str[6:8]
    CID2 = message_hex_str[8:10]
    LENGTH = message_hex_str[10:14]  # Fix the LENGTH slice
    _LOGGER.debug("ATru. ADR: %s", ADR)

    # Attempt to convert LENGTH to decimal
    length_in_dec = int(LENGTH, 16) & 0x0FFF

    INFO = message_hex_str[14:14 + length_in_dec * 2]
    CHKSUM = message_hex_str[-4:]
    _LOGGER.debug("INFO Field (hex): %s", ' '.join(hex(ord(char)) for char in INFO))

    # Getting data from INFO
    result.device_name = hex_to_ascii(INFO[16:36])  # Adjust slice for Device Name
    result.software_version = int(float(INFO[0:4]), 16)  # Convert Software Version to integer
    result.manufacturer_name = hex_to_ascii(INFO[36:])
    _LOGGER.debug("Decoded values: %s", result)

    return result