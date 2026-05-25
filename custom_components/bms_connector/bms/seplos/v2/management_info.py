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

def decode_fiveone(hex_string):
    result = BMSSystemDetails()
    hex_string = bytes.fromhex(hex_string)
    if len(hex_string) < 10:
        return None
    device_name_bytes = hex_string[0:10]
    software_version_bytes = hex_string[10:12]
    manufacturer_name_bytes = hex_string[12:24]

    # Convert bytes to ASCII strings
    result.device_name = device_name_bytes.decode('ascii')

    # Interpret the software version correctly
    software_version = int.from_bytes(software_version_bytes, byteorder='big') / 1000 * 4  # Really unsure if this is correct ... my version is 16.4 so * 4 made 4.1 16.4
    result.software_version = f"{software_version:.1f}"

    result.manufacturer_name = manufacturer_name_bytes.decode('ascii')

    return result
