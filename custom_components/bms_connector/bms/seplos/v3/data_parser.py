import logging
_LOGGER = logging.getLogger(__name__)
# Function to convert bytes to the appropriate data type based on the type field
def convert_bytes_to_data(data_type, byte1, byte2):
    if data_type == "UINT16":
        return (byte1 << 8) | byte2
    elif data_type == "INT16":
        value = (byte1 << 8) | byte2
        # Convert to signed integer
        if value & 0x8000:
            value -= 0x10000
        return value
    else:
        return None


class V3PIATableData:
    def __init__(self):
        self.pack_voltage = 0
        self.current = 0
        self.remaining_capacity = 0
        self.total_capacity = 0
        self.total_discharge_capacity = 0
        self.soc = 0
        self.soh = 0
        self.cycle = 0
        self.avg_cell_voltage = 0
        self.avg_cell_temperature = 0
        self.max_cell_voltage = 0
        self.min_cell_voltage = 0
        self.max_cell_temperature = 0
        self.min_cell_temperature = 0
        self.test = 0  # Example test field

    def __str__(self):
        return (
            f"pack_voltage: {self.pack_voltage}, "
            f"current: {self.current}, "
            f"remaining_capacity: {self.remaining_capacity}, "
            f"total_capacity: {self.total_capacity}, "
            f"total_discharge_capacity: {self.total_discharge_capacity}, "
            f"soc: {self.soc}, "
            f"soh: {self.soh}, "
            f"cycle: {self.cycle}, "
            f"avg_cell_voltage: {self.avg_cell_voltage}, "
            f"avg_cell_temperature: {self.avg_cell_temperature}, "
            f"max_cell_voltage: {self.max_cell_voltage}, "
            f"min_cell_voltage: {self.min_cell_voltage}, "
            f"max_cell_temperature: {self.max_cell_temperature}, "
            f"min_cell_temperature: {self.min_cell_temperature}, "
            f"test: {self.test}"
        )

class V3PIBTableData:
    def __init__(self):
        self.cell1_voltage = 0
        self.cell2_voltage = 0
        self.cell3_voltage = 0
        self.cell4_voltage = 0
        self.cell5_voltage = 0
        self.cell6_voltage = 0
        self.cell7_voltage = 0
        self.cell8_voltage = 0
        self.cell9_voltage = 0
        self.cell10_voltage = 0
        self.cell11_voltage = 0
        self.cell12_voltage = 0
        self.cell13_voltage = 0
        self.cell14_voltage = 0
        self.cell15_voltage = 0
        self.cell16_voltage = 0
        # Add more attributes as needed

    def __str__(self):
        return (
            f"cell1_voltage: {self.cell1_voltage}, "
            f"cell2_voltage: {self.cell2_voltage}, "
            f"cell3_voltage: {self.cell3_voltage}, "
            f"cell4_voltage: {self.cell4_voltage}, "
            f"cell5_voltage: {self.cell5_voltage}, "
            f"cell6_voltage: {self.cell6_voltage}, "
            f"cell7_voltage: {self.cell7_voltage}, "
            f"cell8_voltage: {self.cell8_voltage}, "
            f"cell9_voltage: {self.cell9_voltage}, "
            f"cell10_voltage: {self.cell10_voltage}, "
            f"cell11_voltage: {self.cell11_voltage}, "
            f"cell12_voltage: {self.cell12_voltage}, "
            f"cell13_voltage: {self.cell13_voltage}, "
            f"cell14_voltage: {self.cell14_voltage}, "
            f"cell15_voltage: {self.cell15_voltage}, "
            f"cell16_voltage: {self.cell16_voltage}"
            # Add more fields as needed
        )


def decode_pia_table(response):
    data_fields = "0004241499fe6338d63a98005d03ca03e700070cdf0b940ce50cda0b940b9400000096009603e84f7c"
    data_fields = response  # Function code for PIA
    if data_fields:
        data_fields = data_fields[6:]
        data_fields = bytes.fromhex(data_fields)
        pia_data = V3PIATableData()  # Create an instance of V3PIATableData

        # Set the attributes of the pia_data instance with the parsed values
        pia_data.pack_voltage = convert_bytes_to_data("UINT16", data_fields[0], data_fields[1]) * 0.01
        pia_data.current = convert_bytes_to_data("INT16", data_fields[2], data_fields[3]) * 0.01
        pia_data.remaining_capacity = convert_bytes_to_data("UINT16", data_fields[4], data_fields[5]) * 0.01
        pia_data.total_capacity = convert_bytes_to_data("UINT16", data_fields[6], data_fields[7]) * 0.01
        pia_data.total_discharge_capacity = convert_bytes_to_data("UINT16", data_fields[8], data_fields[9]) * 0.1
        pia_data.soc = convert_bytes_to_data("UINT16", data_fields[10], data_fields[11]) * 0.1
        pia_data.soh = convert_bytes_to_data("UINT16", data_fields[12], data_fields[13]) * 0.1
        pia_data.cycle = convert_bytes_to_data("UINT16", data_fields[14], data_fields[15])
        pia_data.avg_cell_voltage = convert_bytes_to_data("UINT16", data_fields[16], data_fields[17]) * 0.001
        pia_data.avg_cell_temperature = convert_bytes_to_data("UINT16", data_fields[18], data_fields[19]) * 0.1 - 273.15
        pia_data.max_cell_voltage = convert_bytes_to_data("UINT16", data_fields[20], data_fields[21]) * 0.001
        pia_data.min_cell_voltage = convert_bytes_to_data("UINT16", data_fields[22], data_fields[23]) * 0.001
        pia_data.max_cell_temperature = convert_bytes_to_data("UINT16", data_fields[24], data_fields[25]) * 0.1 - 273.15
        pia_data.min_cell_temperature = convert_bytes_to_data("UINT16", data_fields[26], data_fields[27]) * 0.1 - 273.15

        return pia_data  # Return the pia_data instance
    else:
        return None


def decode_pib_table(response):
    global pib_data
    data_fields = "0004240cdd0ce50cdf0cdd0ce40cdc0cda0ce10ce20ce20ce40cde0ce10cde0cdd0ce20b940b94e3e4"
    data_fields = response  # Function code for PIB
    if data_fields:
        data_fields = data_fields[6:]
        data_fields = bytes.fromhex(data_fields)
        pib_data = V3PIBTableData()  # Create an instance of V3PIBTableData

        # Set the attributes of the pib_data instance with the parsed values
        pib_data.cell1_voltage = convert_bytes_to_data("UINT16", data_fields[0], data_fields[1]) * 0.001
        pib_data.cell2_voltage = convert_bytes_to_data("UINT16", data_fields[2], data_fields[3]) * 0.001
        pib_data.cell3_voltage = convert_bytes_to_data("UINT16", data_fields[4], data_fields[5]) * 0.001
        pib_data.cell4_voltage = convert_bytes_to_data("UINT16", data_fields[6], data_fields[7]) * 0.001
        pib_data.cell5_voltage = convert_bytes_to_data("UINT16", data_fields[8], data_fields[9]) * 0.001
        pib_data.cell6_voltage = convert_bytes_to_data("UINT16", data_fields[10], data_fields[11]) * 0.001
        pib_data.cell7_voltage = convert_bytes_to_data("UINT16", data_fields[12], data_fields[13]) * 0.001
        pib_data.cell8_voltage = convert_bytes_to_data("UINT16", data_fields[14], data_fields[15]) * 0.001
        pib_data.cell9_voltage = convert_bytes_to_data("UINT16", data_fields[16], data_fields[17]) * 0.001
        pib_data.cell10_voltage = convert_bytes_to_data("UINT16", data_fields[18], data_fields[19]) * 0.001
        pib_data.cell11_voltage = convert_bytes_to_data("UINT16", data_fields[20], data_fields[21]) * 0.001
        pib_data.cell12_voltage = convert_bytes_to_data("UINT16", data_fields[22], data_fields[23]) * 0.001
        pib_data.cell13_voltage = convert_bytes_to_data("UINT16", data_fields[24], data_fields[25]) * 0.001
        pib_data.cell14_voltage = convert_bytes_to_data("UINT16", data_fields[26], data_fields[27]) * 0.001
        pib_data.cell15_voltage = convert_bytes_to_data("UINT16", data_fields[28], data_fields[29]) * 0.001
        pib_data.cell16_voltage = convert_bytes_to_data("UINT16", data_fields[30], data_fields[31]) * 0.001
        # Set other attributes as needed

        return pib_data  # Return the pib_data instance
    else:
        return None

# Function to retrieve PIC data
# PIC DOESNT WORK AT THE MOMENT!
def retrieve_pic_data(pack_address):
    data_fields = 0 # Function code for PIC
    if data_fields:
        data_fields = data_fields[6:]
        # Parse and display PIC data (if there's enough data)
        if len(data_fields) >= 13:
            pic_data = {
                "Cells Voltage 08-01 Low Alarm": int(data_fields[0]) & 0xFF,
                "Cells Voltage 16-09 Low Alarm": int(data_fields[1]) & 0xFF,
                "Cells Voltage 08-01 High Alarm": int(data_fields[2]) & 0xFF,
                "Cells Voltage 16-09 High Alarm": int(data_fields[3]) & 0xFF,
                "Cell 08-01 Temperature Tlow Alarm": int(data_fields[4]) & 0xFF,
                "Cell 08-01 Temperature Thigh Alarm": int(data_fields[5]) & 0xFF,
                "Cell 08-01 Equalization Event Code": int(data_fields[6]) & 0xFF,
                "Cell 16-09 Equalization Event Code": int(data_fields[7]) & 0xFF,
                "System State Code": int(data_fields[8]) & 0xFF,
                "Voltage Event Code": int(data_fields[9]) & 0xFF,
                "Cells Temperature Event Code": int(data_fields[10]) & 0xFF,
                "Environment and Power Temperature Event Code": int(data_fields[11]) & 0xFF,
                "Current Event Code 1": int(data_fields[12]) & 0xFF,
            }
            return pic_data
        else:
            return None
    else:
        return None

def extract_data_from_message(msg, telemetry_requested=True, teledata_requested=True, debug=True, config_battery_address=True):
    processed_data = []
    processed_data1 = []
    processed_data2 = []
    processed_data3 = []
    address_string = config_battery_address
    address_string1 = None
    address_string2 = None
    address_string3 = None
    
    # WHOLE SECTION NEEDS WORK

    for response in msg:
        if response.startswith("~"):
            response = response[1:] 
        
        _LOGGER.debug("Data Response: %s", response)
        if response == msg[0]:
            pia_data = decode_pia_table(response)
            _LOGGER.debug("pia_data: %s", pia_data)
        elif response == msg[1]:
            pib_data = decode_pib_table(response)
            _LOGGER.debug("pia_data: %s", pib_data)


    return address_string, pia_data, pib_data, processed_data3, processed_data2
