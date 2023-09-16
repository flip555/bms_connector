# Decode 47H data for Seplos V2 BMS
# These settings appear to pertain to OV/UV protection
# To identify the references, a comparison with actual Seplos data is needed
# Encoded Data: 200046008152003C0DDE0D480B540BB80E420D480A8C0B540D4805DC16A81540122012C016301540104011F8163016300C9F0C810ABF0ADD0CD10C9F0A470AAB0CB30C810A470AC90CD10C9F0A150AAB0AAB0B0F0C9F0C810AAB0AC90D030CD10A470AAB0E2F0DFD0E930DFD4E204C2CAFECB0B45208ADF88AD007D059D827101B321E1E140A100A0A1E3C0505010A0A1EF0300F0560506409000D0008FFFFFF3FBF81BF1E313130312D5350373620B2F1
# Decoded Data Bytes: [60, 3550, 3400, 2900, 3000, 3650, 3400, 2700, 2900, 3400, 1500, 5800]

import serial
import time
import logging
import serial
_LOGGER = logging.getLogger(__name__)
def decode_47H_response(hex_string):
    if len(hex_string) < 10:
        return None, None, None

    soi = hex_string[0]
    ver = hex_string[1]
    adr = hex_string[2]
    infoflag = hex_string[3]
    
    # Extract length correctly
    length = int.from_bytes(hex_string[4:6], byteorder='big')
    
    # Extract datai correctly as bytes
    datai_start = 6
    datai_end = datai_start + length
    datai_bytes = hex_string[datai_start:datai_end]
    
    chksum = hex_string[-4:-2]
    eoi = hex_string[-2]

    # Decode INFOFLAG
    cell_high_voltage_limit = infoflag & 0x01
    cell_low_voltage_limit_alarm = (infoflag >> 1) & 0x01
    cell_low_voltage_limit_protect = (infoflag >> 2) & 0x01
    charge_high_temperature_limit = (infoflag >> 3) & 0x01
    charge_low_temperature_limit = (infoflag >> 4) & 0x01
    charge_current_limit = (infoflag >> 5) & 0x01
    module_high_voltage_limit = (infoflag >> 6) & 0x01
    module_low_voltage_limit_alarm = (infoflag >> 7) & 0x01
    module_low_voltage_limit_protect = (infoflag >> 8) & 0x01
    discharge_high_temperature_limit = (infoflag >> 9) & 0x01
    discharge_low_temperature_limit = (infoflag >> 10) & 0x01
    discharge_current_limit = (infoflag >> 11) & 0x01

    # Convert DATAI to human-readable format
    datai_values = []
    datai_values.append(int.from_bytes(datai_bytes[0:2], byteorder='big'))  # Single cell high voltage limit
    datai_values.append(int.from_bytes(datai_bytes[2:4], byteorder='big'))  # Single cell low voltage limit (alarm)
    datai_values.append(int.from_bytes(datai_bytes[4:6], byteorder='big'))  # Single cell low voltage limit (protect)
    datai_values.append(int.from_bytes(datai_bytes[6:8], byteorder='big'))  # Charge high temperature limit
    datai_values.append(int.from_bytes(datai_bytes[8:10], byteorder='big'))  # Charge low temperature limit
    datai_values.append(int.from_bytes(datai_bytes[10:12], byteorder='big'))  # Charge current limit
    datai_values.append(int.from_bytes(datai_bytes[12:14], byteorder='big'))  # Module high voltage limit
    datai_values.append(int.from_bytes(datai_bytes[14:16], byteorder='big'))  # Module low voltage limit (alarm)
    datai_values.append(int.from_bytes(datai_bytes[16:18], byteorder='big'))  # Module low voltage limit (protect)
    datai_values.append(int.from_bytes(datai_bytes[18:20], byteorder='big'))  # Discharge high temperature limit
    datai_values.append(int.from_bytes(datai_bytes[20:22], byteorder='big'))  # Discharge low temperature limit
    datai_values.append(int.from_bytes(datai_bytes[22:24], byteorder='big'))  # Discharge current limit

    # Calculate accuracy for each value
    accuracies = [3, 3, 3, 1, 1, 3, 3, 3, 1, 1, 3, 3]
    decoded_data = {
        "60": datai_values[0],  # Single cell high voltage limit (mV)
        "3550": datai_values[1],  # Single cell low voltage limit (alarm) (mV)
        "3400": datai_values[2],  # Single cell low voltage limit (protect) (mV)
        "2900": datai_values[3],  # Charge high temperature limit (K)
        "3000": datai_values[4],  # Charge low temperature limit (K)
        "3650": datai_values[5],  # Charge current limit (A)
        "3400": datai_values[6],  # Module high voltage limit (mV)
        "2700": datai_values[7],  # Module low voltage limit (alarm) (mV)
        "2900": datai_values[8],  # Module low voltage limit (protect) (mV)
        "3400": datai_values[9],  # Discharge high temperature limit (K)
        "1500": datai_values[10],  # Discharge low temperature limit (K)
        "5800": datai_values[11],  # Discharge low temperature limit (K)
    }
    return infoflag, datai_values, decoded_data

    
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
        infoflag1, datai_bytes1, decoded_data1 = decode_47H_response(bytes.fromhex(response))

        print("Infoflag:", infoflag1)
        print("Datai Bytes:", datai_bytes1)
        for key, value in decoded_data1.items():
            print(f"{key}: {value}")
        return response
        
send_serial_command("~20004647E00200FD32\r", "/dev/ttyUSB0", 19200, 2)


