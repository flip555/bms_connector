# Full setting extraction from Seplos V2. Some values may need some tweaking. should match entry by entry if you save your parameter xml in Battery Monitor

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

    soi = hex_string[0]
    ver = hex_string[1]
    adr = hex_string[2]
    infoflag = hex_string[3]

    # Extract length correctly
    length = int.from_bytes(hex_string[4:6], byteorder='big')

    # Extract datai correctly as bytes
    datai_start = 8
    datai_end = datai_start + length
    datai_bytes = hex_string[datai_start:datai_end]



    # Convert DATAI to human-readable format
    datai_values = [
        int.from_bytes(datai_bytes[0:2], byteorder='big') / 1000.0,  # Monomer high voltage alarm: 3.550 V
        int.from_bytes(datai_bytes[2:4], byteorder='big') / 1000.0,  # Monomer high pressure recovery: 3.400 V
        int.from_bytes(datai_bytes[4:6], byteorder='big') / 1000.0,  # Monomer low pressure alarm: 2.900 V
        int.from_bytes(datai_bytes[6:8], byteorder='big') / 1000.0,  # Monomer low pressure recovery: 3.000 V
        int.from_bytes(datai_bytes[8:10], byteorder='big') / 1000.0,  # Monomer overvoltage protection: 3.650 V
        int.from_bytes(datai_bytes[10:12], byteorder='big') / 1000.0,  # Monomer overvoltage recovery: 3.400 V
        int.from_bytes(datai_bytes[12:14], byteorder='big') / 1000.0,  # Monomer undervoltage protection: 2.700 V
        int.from_bytes(datai_bytes[14:16], byteorder='big') / 1000.0,  # Monomer undervoltage recovery: 2.900 V
        int.from_bytes(datai_bytes[16:18], byteorder='big') / 1000.0,  # Equalization opening voltage: 3.400 V
        int.from_bytes(datai_bytes[18:20], byteorder='big') / 1000.0,  # Battery low voltage forbidden charging: 1.500 V
        int.from_bytes(datai_bytes[20:22], byteorder='big') / 100.0,  # Total pressure high pressure alarm: 58.00 V
        int.from_bytes(datai_bytes[22:24], byteorder='big') / 100.0,  # Total pressure and high pressure recovery: 54.40 V
        int.from_bytes(datai_bytes[24:26], byteorder='big') / 100.0,  # Total pressure low pressure alarm: 46.40 V
        int.from_bytes(datai_bytes[26:28], byteorder='big') / 100.0,  # Total pressure and low pressure recovery: 48.00 V
        int.from_bytes(datai_bytes[28:30], byteorder='big') / 100.0,  # Total_voltage overvoltage protection: 56.80 V
        int.from_bytes(datai_bytes[30:32], byteorder='big') / 100.0,  # Total pressure overpressure recovery: 54.40 V
        int.from_bytes(datai_bytes[32:34], byteorder='big') / 100.0,  # Total_voltage undervoltage protection: 41.60 V
        int.from_bytes(datai_bytes[34:36], byteorder='big') / 100.0,  # Total pressure undervoltage recovery: 46.00 V
        int.from_bytes(datai_bytes[36:38], byteorder='big') / 100.0,  # Charging overvoltage protection: 56.80 V
        int.from_bytes(datai_bytes[38:40], byteorder='big') / 100.0,  # Charging overvoltage recovery: 56.80 V
        (int.from_bytes(datai_bytes[40:42], byteorder='big')  - 2731) / 10.0,  # Charging high temperature warning: 323.15 K
        (int.from_bytes(datai_bytes[42:44], byteorder='big')  - 2731) / 10.0,  # Charging high temperature recovery: 320.15 K
        (int.from_bytes(datai_bytes[44:46], byteorder='big')  - 2731) / 10.0,  # Charging low temperature warning: 275.15 K
        (int.from_bytes(datai_bytes[46:48], byteorder='big')  - 2731) / 10.0,  # Charging low temperature recovery: 278.15 K
        (int.from_bytes(datai_bytes[48:50], byteorder='big')  - 2731) / 10.0,  # Charging over temperature protection: 328.15 K
        (int.from_bytes(datai_bytes[50:52], byteorder='big')  - 2731) / 10.0,  # Charging over temperature recovery: 323.15 K
        (int.from_bytes(datai_bytes[52:54], byteorder='big')  - 2731) / 10.0,  # Charging under-temperature protection: 263.15 K
        (int.from_bytes(datai_bytes[54:56], byteorder='big')  - 2731) / 10.0,  # Charging under temperature recovery: 273.15 K
        (int.from_bytes(datai_bytes[56:58], byteorder='big')  - 2731) / 10.0,  # Discharge high temperature warning: 325.15 K
        (int.from_bytes(datai_bytes[58:60], byteorder='big')  - 2731) / 10.0,  # Discharge high temperature recovery: 320.15 K
        (int.from_bytes(datai_bytes[60:62], byteorder='big')  - 2731) / 10.0,  # Discharge low temperature warning: 263.15 K
        (int.from_bytes(datai_bytes[62:64], byteorder='big')  - 2731) / 10.0,  # Discharge low temperature recovery: 276.15 K
        (int.from_bytes(datai_bytes[64:66], byteorder='big')  - 2731) / 10.0,  # Discharge over temperature protection: 328.15 K
        (int.from_bytes(datai_bytes[66:68], byteorder='big')  - 2731) / 10.0,  # Discharge over temperature recovery: 323.15 K
        (int.from_bytes(datai_bytes[68:70], byteorder='big')  - 2731) / 10.0,  # Discharge under-temperature protection: 258.15 K
        (int.from_bytes(datai_bytes[70:72], byteorder='big')  - 2731) / 10.0,  # Discharge under temperature recovery: 273.15 K
        (int.from_bytes(datai_bytes[72:74], byteorder='big')  - 2731) / 10.0,  # Cell low temperature heating: 273.15 K
        (int.from_bytes(datai_bytes[74:76], byteorder='big')  - 2731) / 10.0,  # Cell heating recovery: 283.15 K
        (int.from_bytes(datai_bytes[76:78], byteorder='big')  - 2731) / 10.0,  # Ambient high temperature alarm: 323.15 K
        (int.from_bytes(datai_bytes[78:80], byteorder='big')  - 2731) / 10.0,  # Ambient high temperature recovery: 320.15 K
        (int.from_bytes(datai_bytes[80:82], byteorder='big')  - 2731) / 10.0,  # Ambient low temperature warning: 273.15 K
        (int.from_bytes(datai_bytes[82:84], byteorder='big')  - 2731) / 10.0,  # Ambient low temperature recovery: 276.15 K
        int.from_bytes(datai_bytes[84:86], byteorder='big'),  # Fan fault: 10 sec
        int.from_bytes(datai_bytes[86:88], byteorder='big'),  # Fan fault recovery: 5 sec
        int.from_bytes(datai_bytes[88:90], byteorder='big'),  # CAN communication fault: 10 sec
        int.from_bytes(datai_bytes[90:92], byteorder='big'),  # CAN communication fault recovery: 5 sec
        int.from_bytes(datai_bytes[92:94], byteorder='big'),  # MOS short circuit protection: 10 sec
        int.from_bytes(datai_bytes[94:96], byteorder='big'),  # MOS short circuit protection recovery: 5 sec
        (int.from_bytes(datai_bytes[96:98], byteorder='big')  - 2731) / 10.0,  # Power high temperature recovery: 373.15 K
        (int.from_bytes(datai_bytes[98:100], byteorder='big')  - 2731) / 10.0,  # Power over temperature protection: 358.15 K
        (int.from_bytes(datai_bytes[100:102], byteorder='big')  - 2731) / 10.0,  # Power over temperature recovery: 273.15 K
        int.from_bytes(datai_bytes[102:104], byteorder='big') / 100.0,  # Charging overcurrent warning: 200.00 A
        int.from_bytes(datai_bytes[104:106], byteorder='big') / 100.0,  # Charging overcurrent recovery: 195.00 A
        int.from_bytes(datai_bytes[106:108], byteorder='big') / 100.0,  # Discharge overcurrent warning: -205.00 A
        int.from_bytes(datai_bytes[108:110], byteorder='big') / 100.0,  # Discharge overcurrent recovery: -203.00 A
        int.from_bytes(datai_bytes[110:112], byteorder='big') / 100.0,  # Charge overcurrent protection: 210.00 A
        int.from_bytes(datai_bytes[112:114], byteorder='big') / 100.0,  # Discharge overcurrent protection: -210.00 A
        int.from_bytes(datai_bytes[114:116], byteorder='big') / 100.0,  # Transient overcurrent protection: -300.00 A
        int.from_bytes(datai_bytes[116:118], byteorder='big') / 1000.0,  # Output soft start delay: 2000 ms
        int.from_bytes(datai_bytes[118:120], byteorder='big'),  # Battery rated capacity: 230.00 Ah
        int.from_bytes(datai_bytes[120:122], byteorder='big'),  # SOC: 100.00 Ah
        int.from_bytes(datai_bytes[122:124], byteorder='big') / 100.0,  # Cell invalidation differential pressure: 0.50 V
        int.from_bytes(datai_bytes[124:126], byteorder='big') / 100.0,  # Cell invalidation recovery: 0.30 V
        int.from_bytes(datai_bytes[126:128], byteorder='big') / 1000.0,  # Equalization opening pressure difference: 0.030 V
        int.from_bytes(datai_bytes[128:130], byteorder='big') / 1000.0,  # Equalization closing pressure difference: 0.020 V
        int.from_bytes(datai_bytes[130:132], byteorder='big'),  # Static equilibrium time: 10 sec
        int.from_bytes(datai_bytes[132:134], byteorder='big'),  # Battery number in series: 16 String
        int.from_bytes(datai_bytes[134:136], byteorder='big') / 1000.0,  # Charge overcurrent delay: 10 sec
        int.from_bytes(datai_bytes[136:138], byteorder='big') / 1000.0,  # Discharge overcurrent delay: 10 sec
        int.from_bytes(datai_bytes[138:140], byteorder='big') / 1000.0,  # Transient overcurrent delay: 30 ms
        int.from_bytes(datai_bytes[140:142], byteorder='big') / 1000.0,  # Overcurrent delay recovery: 60 sec
        int.from_bytes(datai_bytes[142:144], byteorder='big'),  # Overcurrent recovery times: 5 times
        int.from_bytes(datai_bytes[144:146], byteorder='big') / 60.0,  # Charge current limit delay: 5 min
        int.from_bytes(datai_bytes[146:148], byteorder='big') / 60.0,  # Charge activation delay: 1 min
        int.from_bytes(datai_bytes[148:150], byteorder='big'),  # Charging activation interval: 10 sec
        int.from_bytes(datai_bytes[150:152], byteorder='big'),  # Charge activation times: 10 times
        int.from_bytes(datai_bytes[152:154], byteorder='big') / 60.0,  # Work record interval: 30 min
        int.from_bytes(datai_bytes[154:156], byteorder='big') / 60.0,  # Standby recording interval: 240 min
        int.from_bytes(datai_bytes[156:158], byteorder='big'),  # Standby shutdown delay: 48 sec
        int.from_bytes(datai_bytes[158:160], byteorder='big') / 100.0,  # Remaining capacity alarm: 15 %
        int.from_bytes(datai_bytes[160:162], byteorder='big') / 100.0,  # Remaining capacity protection: 5 %
        int.from_bytes(datai_bytes[162:164], byteorder='big') / 100.0,  # Interval charge capacity: 96 %
        int.from_bytes(datai_bytes[164:166], byteorder='big') / 100.0,  # Cycle cumulative capacity: 80 %
        int.from_bytes(datai_bytes[166:168], byteorder='big') / 1000.0,  # Connection fault impedance: 10.0 mΩ
        int.from_bytes(datai_bytes[168:170], byteorder='big'),  # Compensation point 1 position: 9 String
        int.from_bytes(datai_bytes[170:172], byteorder='big') / 1000.0,  # Compensation point 1 impedance: 0.0 mΩ
        int.from_bytes(datai_bytes[172:174], byteorder='big'),  # Compensation point 2 position: 13 String
        int.from_bytes(datai_bytes[174:176], byteorder='big') / 1000.0,  # Compensation point 2 impedance: 0.0 mΩ
        int.from_bytes(datai_bytes[176:178], byteorder='big'),  # Compensation point 3 position: 0 String
        int.from_bytes(datai_bytes[178:180], byteorder='big') / 1000.0,  # Compensation point 3 impedance: 0.0 mΩ
        int.from_bytes(datai_bytes[180:182], byteorder='big'),  # Compensation point 4 position: 0 String
        int.from_bytes(datai_bytes[182:184], byteorder='big') / 1000.0  # Compensation point 4 impedance: 0.0 mΩ
    ]

       

    attributes = [
        "monomer_high_voltage_alarm", "monomer_high_pressure_recovery", "monomer_low_pressure_alarm",
        "monomer_low_pressure_recovery", "monomer_overvoltage_protection", "monomer_overvoltage_recovery",
        "monomer_undervoltage_protection", "monomer_undervoltage_recovery", "equalization_opening_voltage",
        "battery_low_voltage_forbidden_charging", "total_pressure_high_pressure_alarm",
        "total_pressure_high_pressure_recovery", "total_pressure_low_pressure_alarm",
        "total_pressure_low_pressure_recovery", "total_voltage_overvoltage_protection",
        "total_pressure_overpressure_recovery", "total_voltage_undervoltage_protection",
        "total_pressure_undervoltage_recovery", "charging_overvoltage_protection",
        "charging_overvoltage_recovery", "charging_high_temperature_warning",
        "charging_high_temperature_recovery", "charging_low_temperature_warning",
        "charging_low_temperature_recovery", "charging_over_temperature_protection",
        "charging_over_temperature_recovery", "charging_under_temperature_protection",
        "charging_under_temperature_recovery", "discharge_high_temperature_warning",
        "discharge_high_temperature_recovery", "discharge_low_temperature_warning",
        "discharge_low_temperature_recovery", "discharge_over_temperature_protection",
        "discharge_over_temperature_recovery", "discharge_under_temperature_protection",
        "discharge_under_temperature_recovery", "cell_low_temperature_heating",
        "cell_heating_recovery", "ambient_high_temperature_alarm",
        "ambient_high_temperature_recovery", "ambient_low_temperature_warning",
        "ambient_low_temperature_recovery", "fan_fault", "fan_fault_recovery",
        "can_communication_fault", "can_communication_fault_recovery",
        "mos_short_circuit_protection", "mos_short_circuit_protection_recovery",
        "power_high_temperature_recovery", "power_over_temperature_protection",
        "power_over_temperature_recovery", "charging_overcurrent_warning",
        "charging_overcurrent_recovery", "discharge_overcurrent_warning",
        "discharge_overcurrent_recovery", "charge_overcurrent_protection",
        "discharge_overcurrent_protection", "transient_overcurrent_protection",
        "output_soft_start_delay", "battery_rated_capacity", "soc",
        "cell_invalidation_differential_pressure", "cell_invalidation_recovery",
        "equalization_opening_pressure_difference", "equalization_closing_pressure_difference",
        "static_equilibrium_time", "battery_number_in_series", "charge_overcurrent_delay",
        "discharge_overcurrent_delay", "transient_overcurrent_delay",
        "overcurrent_delay_recovery", "overcurrent_recovery_times",
        "charge_current_limit_delay", "charge_activation_delay", "charge_activation_interval",
        "charge_activation_times", "work_record_interval", "standby_recording_interval",
        "standby_shutdown_delay", "remaining_capacity_alarm", "remaining_capacity_protection",
        "interval_charge_capacity", "cycle_cumulative_capacity", "connection_fault_impedance",
        "compensation_point_1_position", "compensation_point_1_impedance",
        "compensation_point_2_position", "compensation_point_2_impedance",
        "compensation_point_3_position", "compensation_point_3_impedance",
        "compensation_point_4_position", "compensation_point_4_impedance"
    ]

    for i, attr in enumerate(attributes):
        setattr(result, attr, datai_values[i])
        print(attr, " ", datai_values[i])


    return result

def send_serial_command(command: str, port: str, baudrate: int = 19200, timeout: int = 2) -> str:
    with serial.Serial(port, baudrate=baudrate, timeout=timeout) as ser:
        print("Serial Comms Sending: %s", command)
        ser.write(command.encode())
        time.sleep(0.5)
        response = ser.read(ser.in_waiting).decode().replace('\r', '').replace('\n', '')
        if response.startswith("~"):
            response = response[1:]
        print("Serial Comms Received: %s", response)
        decode_47H_response(response)
        
send_serial_command("~20004647E00200FD32\r", "/dev/ttyUSB0", 19200, 2)


