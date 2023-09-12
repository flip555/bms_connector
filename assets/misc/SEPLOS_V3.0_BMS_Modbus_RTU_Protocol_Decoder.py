# SEPLOS V3.0 BMS Modbus RTU Protocol Decoder
# This script is designed to decode data from a SEPLOS V3.0 BMS using the Modbus RTU protocol.
# It establishes a serial connection to the BMS, sends Modbus requests, and decodes the responses.
# The decoded data points are defined in the MODBUS_REQUESTS dictionary.

# GitHub Repository: https://github.com/flip555/seplos_bms_ha
# Discussions and issues can be found on the GitHub discussion board.
import serial

# Set the COM port and pack address here
COM_PORT = '/dev/ttyUSB0'
PACK_ADDRESS = 0x01

# Modbus RTU requests configuration
MODBUS_REQUESTS = {
    0x1000: {"name": "Pack Voltage", "type": "UINT16", "scale": 0.01, "unit": "V"},
    0x1001: {"name": "Current", "type": "INT16", "scale": 0.01, "unit": "A"},
    0x1002: {"name": "Remaining capacity", "type": "UINT16", "scale": 0.1, "unit": "Ah"},
    0x1003: {"name": "Total Capacity", "type": "UINT16", "scale": 0.1, "unit": "Ah"},
    0x1004: {"name": "Total Discharge Capacity", "type": "UINT16", "scale": 1, "unit": "Ah"},
    0x1005: {"name": "SOC", "type": "UINT16", "scale": 0.1, "unit": "%"},
    0x1006: {"name": "SOH", "type": "UINT16", "scale": 0.1, "unit": "%"},
    0x1007: {"name": "Cycle", "type": "UINT16", "scale": 1, "unit": ""},
    0x1008: {"name": "Average of Cell Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x1009: {"name": "Average of Cell Temperature", "type": "UINT16", "scale": 0.1, "unit": "K"},
    0x100A: {"name": "Max Cell Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x100B: {"name": "Min Cell Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x100C: {"name": "Max Cell Temperature", "type": "UINT16", "scale": 0.1, "unit": "K"},
    0x100D: {"name": "Min Cell Temperature", "type": "UINT16", "scale": 0.1, "unit": "K"},
    0x100E: {"name": "reserve", "type": "", "scale": 1, "unit": ""},
    0x100F: {"name": "MaxDisCurt", "type": "UINT16", "scale": 1, "unit": "A"},
    0x1010: {"name": "MaxChgCurt", "type": "UINT16", "scale": 1, "unit": "A"},
    0x1100: {"name": "Cell1 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x1101: {"name": "Cell2 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x1102: {"name": "Cell3 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x1103: {"name": "Cell4 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x1104: {"name": "Cell5 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x1105: {"name": "Cell6 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x1106: {"name": "Cell7 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x1107: {"name": "Cell8 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x1108: {"name": "Cell9 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x1109: {"name": "Cell10 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x110A: {"name": "Cell11 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x110B: {"name": "Cell12 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x110C: {"name": "Cell13 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x110D: {"name": "Cell14 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x110E: {"name": "Cell15 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x110F: {"name": "Cell16 Voltage", "type": "UINT16", "scale": 0.001, "unit": "V"},
    0x1110: {"name": "Cell temperature 1", "type": "UINT16", "scale": 0.1, "unit": "K"},
    0x1111: {"name": "Cell temperature 2", "type": "UINT16", "scale": 0.1, "unit": "K"},
    0x1112: {"name": "Cell temperature 3", "type": "UINT16", "scale": 0.1, "unit": "K"},
    0x1113: {"name": "Cell temperature 4", "type": "UINT16", "scale": 0.1, "unit": "K"},
    0x1118: {"name": "Environment Temperature", "type": "UINT16", "scale": 0.1, "unit": "K"},
    0x1119: {"name": "Power Temperature", "type": "UINT16", "scale": 0.1, "unit": "K"},
}

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

# Serial communication setup
ser = serial.Serial(COM_PORT, baudrate=19200, parity=serial.PARITY_NONE, stopbits=1, bytesize=8, timeout=1)

try:
    # Iterate through the Modbus requests and send each one to the device
    for register, config in MODBUS_REQUESTS.items():
        print(f"Sending request for {config['name']} (Register {hex(register)})")

        # Build Modbus RTU request
        request = bytes([PACK_ADDRESS, 0x04, (register >> 8) & 0xFF, register & 0xFF, 0x00, 0x02, 0x00, 0x00])
        ser.write(request)
        print(f"Request sent: {request.hex()}")

        response = ser.read(5)  # Assuming the response is 5 bytes
        print(f"Response received: {response.hex()}")

        # Extract and convert data from the response
        if len(response) == 5:
            data_value = convert_bytes_to_data(config["type"], response[3], response[4])
            if data_value is not None:
                scaled_value = data_value * config["scale"]
                print(f"{config['name']}: {scaled_value} {config['unit']}")

except serial.SerialException as e:
    print("Serial communication error:", str(e))
finally:
    ser.close()