import logging
_LOGGER = logging.getLogger(__name__)
class ProtectionSettingsData:
    def __init__(self, settings=None):
        if settings is None:
            settings = [0] * 46  # Initialize with zeros if settings not provided
        self.monomer_high_voltage_alarm = settings[0]
        self.monomer_high_pressure_recovery = settings[1]
        self.monomer_low_pressure_alarm = settings[2]
        self.monomer_low_pressure_recovery = settings[3]
        self.monomer_overvoltage_protection = settings[4]
        self.monomer_overvoltage_recovery = settings[5]
        self.monomer_undervoltage_protection = settings[6]
        self.monomer_undervoltage_recovery = settings[7]
        self.equalization_opening_voltage = settings[8]
        self.battery_low_voltage_forbidden_charging = settings[9]
        self.total_pressure_high_pressure_alarm = settings[10]
        self.total_pressure_high_pressure_recovery = settings[11]
        self.total_pressure_low_pressure_alarm = settings[12]
        self.total_pressure_low_pressure_recovery = settings[13]
        self.total_voltage_overvoltage_protection = settings[14]
        self.total_pressure_overpressure_recovery = settings[15]
        self.total_voltage_undervoltage_protection = settings[16]
        self.total_pressure_undervoltage_recovery = settings[17]
        self.charging_overvoltage_protection = settings[18]
        self.charging_overvoltage_recovery = settings[19]
        self.charging_high_temperature_warning = settings[20]
        self.charging_high_temperature_recovery = settings[21]
        self.charging_low_temperature_warning = settings[22]
        self.charging_low_temperature_recovery = settings[23]
        self.charging_over_temperature_protection = settings[24]
        self.charging_over_temperature_recovery = settings[25]
        self.charging_under_temperature_protection = settings[26]
        self.charging_under_temperature_recovery = settings[27]
        self.discharge_high_temperature_warning = settings[28]
        self.discharge_high_temperature_recovery = settings[29]
        self.discharge_low_temperature_warning = settings[30]
        self.discharge_low_temperature_recovery = settings[31]
        self.discharge_over_temperature_protection = settings[32]
        self.discharge_over_temperature_recovery = settings[33]
        self.discharge_under_temperature_protection = settings[34]
        self.discharge_under_temperature_recovery = settings[35]
        self.cell_low_temperature_heating = settings[36]
        self.cell_heating_recovery = settings[37]
        self.ambient_high_temperature_alarm = settings[38]
        self.ambient_high_temperature_recovery = settings[39]
        self.ambient_low_temperature_warning = settings[40]
        self.ambient_low_temperature_recovery = settings[41]
        self.fan_fault = settings[42]
        self.fan_fault_recovery = settings[43]
        self.can_communication_fault = settings[44]
        self.can_communication_fault_recovery = settings[45]

    def __str__(self):
        return (
            f"Monomer High Voltage Alarm: {self.monomer_high_voltage_alarm} V\n"
            f"Monomer High Pressure Recovery: {self.monomer_high_pressure_recovery} V\n"
            f"Monomer Low Pressure Alarm: {self.monomer_low_pressure_alarm} V\n"
            f"Monomer Low Pressure Recovery: {self.monomer_low_pressure_recovery} V\n"
            f"Monomer Overvoltage Protection: {self.monomer_overvoltage_protection} V\n"
            f"Monomer Overvoltage Recovery: {self.monomer_overvoltage_recovery} V\n"
            f"Monomer Undervoltage Protection: {self.monomer_undervoltage_protection} V\n"
            f"Monomer Undervoltage Recovery: {self.monomer_undervoltage_recovery} V\n"
            f"Equalization Opening Voltage: {self.equalization_opening_voltage} V\n"
            f"Battery Low Voltage Forbidden Charging: {self.battery_low_voltage_forbidden_charging} V\n"
            f"Total Pressure High Pressure Alarm: {self.total_pressure_high_pressure_alarm} V\n"
            f"Total Pressure High Pressure Recovery: {self.total_pressure_high_pressure_recovery} V\n"
            f"Total Pressure Low Pressure Alarm: {self.total_pressure_low_pressure_alarm} V\n"
            f"Total Pressure Low Pressure Recovery: {self.total_pressure_low_pressure_recovery} V\n"
            f"Total Voltage Overvoltage Protection: {self.total_voltage_overvoltage_protection} V\n"
            f"Total Pressure Overpressure Recovery: {self.total_pressure_overpressure_recovery} V\n"
            f"Total Voltage Undervoltage Protection: {self.total_voltage_undervoltage_protection} V\n"
            f"Total Pressure Undervoltage Recovery: {self.total_pressure_undervoltage_recovery} V\n"
            f"Charging Overvoltage Protection: {self.charging_overvoltage_protection} V\n"
            f"Charging Overvoltage Recovery: {self.charging_overvoltage_recovery} V\n"
            f"Charging High Temperature Warning: {self.charging_high_temperature_warning} °C\n"
            f"Charging High Temperature Recovery: {self.charging_high_temperature_recovery} °C\n"
            f"Charging Low Temperature Warning: {self.charging_low_temperature_warning} °C\n"
            f"Charging Low Temperature Recovery: {self.charging_low_temperature_recovery} °C\n"
            f"Charging Over Temperature Protection: {self.charging_over_temperature_protection} °C\n"
            f"Charging Over Temperature Recovery: {self.charging_over_temperature_recovery} °C\n"
            f"Charging Under Temperature Protection: {self.charging_under_temperature_protection} °C\n"
            f"Charging Under Temperature Recovery: {self.charging_under_temperature_recovery} °C\n"
            f"Discharge High Temperature Warning: {self.discharge_high_temperature_warning} °C\n"
            f"Discharge High Temperature Recovery: {self.discharge_high_temperature_recovery} °C\n"
            f"Discharge Low Temperature Warning: {self.discharge_low_temperature_warning} °C\n"
            f"Discharge Low Temperature Recovery: {self.discharge_low_temperature_recovery} °C\n"
            f"Discharge Over Temperature Protection: {self.discharge_over_temperature_protection} °C\n"
            f"Discharge Over Temperature Recovery: {self.discharge_over_temperature_recovery} °C\n"
            f"Discharge Under Temperature Protection: {self.discharge_under_temperature_protection} °C\n"
            f"Discharge Under Temperature Recovery: {self.discharge_under_temperature_recovery} °C\n"
            f"Cell Low Temperature Heating: {self.cell_low_temperature_heating} °C\n"
            f"Cell Heating Recovery: {self.cell_heating_recovery} °C\n"
            f"Ambient High Temperature Alarm: {self.ambient_high_temperature_alarm} °C\n"
            f"Ambient High Temperature Recovery: {self.ambient_high_temperature_recovery} °C\n"
            f"Ambient Low Temperature Warning: {self.ambient_low_temperature_warning} °C\n"
            f"Ambient Low Temperature Recovery: {self.ambient_low_temperature_recovery} °C\n"
            f"Fan Fault: {self.fan_fault} When\n"
            f"Fan Fault Recovery: {self.fan_fault_recovery} When\n"
            f"CAN Communication Fault: {self.can_communication_fault} When\n"
            f"CAN Communication Fault Recovery: {self.can_communication_fault_recovery} When\n"
            f"MOS Short Circuit Protection: {self.mos_short_circuit_protection} When\n"
            f"MOS Short Circuit Protection Recovery: {self.mos_short_circuit_protection_recovery} When\n"
            f"Power High Temperature Recovery: {self.power_high_temperature_recovery} °C\n"
            f"Power Over Temperature Protection: {self.power_over_temperature_protection} °C\n"
            f"Power Over Temperature Recovery: {self.power_over_temperature_recovery} °C\n"
            f"Charging Overcurrent Warning: {self.charging_overcurrent_warning} A\n"
            f"Charging Overcurrent Recovery: {self.charging_overcurrent_recovery} A\n"
            f"Discharge Overcurrent Warning: {self.discharge_overcurrent_warning} A\n"
            f"Discharge Overcurrent Recovery: {self.discharge_overcurrent_recovery} A\n"
            f"Charge Overcurrent Protection: {self.charge_overcurrent_protection} A\n"
            f"Discharge Overcurrent Protection: {self.discharge_overcurrent_protection} A\n"
            f"Transient Overcurrent Protection: {self.transient_overcurrent_protection} A\n"
            f"Output Soft Start Delay: {self.output_soft_start_delay} ms\n"
            f"Battery Rated Capacity: {self.battery_rated_capacity} Ah\n"
            f"SOC: {self.soc} Ah\n"
            f"Cell Invalidation Differential Pressure: {self.cell_invalidation_differential_pressure} V\n"
            f"Cell Invalidation Recovery: {self.cell_invalidation_recovery} V\n"
            f"Equalization Opening Pressure Difference: {self.equalization_opening_pressure_difference} V\n"
            f"Equalization Closing Pressure Difference: {self.equalization_closing_pressure_difference} V\n"
            f"Static Equilibrium Time: {self.static_equilibrium_time} When\n"
            f"Battery Number in Series: {self.battery_number_in_series} String\n"
            f"Charge Overcurrent Delay: {self.charge_overcurrent_delay} S\n"
            f"Discharge Overcurrent Delay: {self.discharge_overcurrent_delay} S\n"
            f"Transient Overcurrent Delay: {self.transient_overcurrent_delay} ms\n"
            f"Overcurrent Delay Recovery: {self.overcurrent_delay_recovery} S\n"
            f"Overcurrent Recovery Times: {self.overcurrent_recovery_times} times\n"
            f"Charge Current Limit Delay: {self.charge_current_limit_delay} Minutes\n"
            f"Charge Activation Delay: {self.charge_activation_delay} Minutes\n"
            f"Charge Activation Interval: {self.charge_activation_interval} When\n"
            f"Charge Activation Times: {self.charge_activation_times} times\n"
            f"Work Record Interval: {self.work_record_interval} Minutes\n"
            f"Standby Recording Interval: {self.standby_recording_interval} Minutes\n"
            f"Standby Shutdown Delay: {self.standby_shutdown_delay} When\n"
            f"Remaining Capacity Alarm: {self.remaining_capacity_alarm} %\n"
            f"Remaining Capacity Protection: {self.remaining_capacity_protection} %\n"
            f"Interval Charge Capacity: {self.interval_charge_capacity} %\n"
            f"Cycle Cumulative Capacity: {self.cycle_cumulative_capacity} %\n"
            f"Connection Fault Impedance: {self.connection_fault_impedance} mΩ\n"
            f"Compensation Point 1 Position: {self.compensation_point_1_position} String\n"
            f"Compensation Point 1 Impedance: {self.compensation_point_1_impedance} mΩ\n"
            f"Compensation Point 2 Position: {self.compensation_point_2_position} String\n"
            f"Compensation Point 2 Impedance: {self.compensation_point_2_impedance} mΩ\n"
            f"Compensation Point 3 Position: {self.compensation_point_3_position} String\n"
            f"Compensation Point 3 Impedance: {self.compensation_point_3_impedance} mΩ\n"
            f"Compensation Point 4 Position: {self.compensation_point_4_position} String\n"
            f"Compensation Point 4 Impedance: {self.compensation_point_4_impedance} mΩ"
        )

def decode_fourseven(hex_string):
    result = ProtectionSettingsData()
    hex_string = bytes.fromhex(hex_string)
    if len(hex_string) < 10:
        return None, None, None

    soi = hex_string[0]
    ver = hex_string[1]
    adr = hex_string[2]
    infoflag = hex_string[3]
    
    # Extract length correctly
    length = int.from_bytes(hex_string[4:6], byteorder='big')
    
    # Extract datai correctly as bytes
    datai_start = 2
    datai_end = datai_start + length
    datai_bytes = hex_string[datai_start:datai_end]
    
    chksum = hex_string[-4:-2]
    eoi = hex_string[-2]


    # Convert DATAI to human-readable format
    datai_values = [
        int.from_bytes(datai_bytes[i:i+2], byteorder='big') 
        for i in range(0, len(datai_bytes), 2)
    ]


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
        int.from_bytes(datai_bytes[118:120], byteorder='big') / 100.0,  # Battery rated capacity: 230.00 Ah
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

        

    # Assign the calculated values to the result object
    result.monomer_high_voltage_alarm = datai_values[0]
    result.monomer_high_pressure_recovery = datai_values[1]
    result.monomer_low_pressure_alarm = datai_values[2]
    result.monomer_low_pressure_recovery = datai_values[3]
    result.monomer_overvoltage_protection = datai_values[4]
    result.monomer_overvoltage_recovery = datai_values[5]
    result.monomer_undervoltage_protection = datai_values[6]
    result.monomer_undervoltage_recovery = datai_values[7]
    result.equalization_opening_voltage = datai_values[8]
    result.battery_low_voltage_forbidden_charging = datai_values[9]
    result.total_pressure_high_pressure_alarm = datai_values[10]
    result.total_pressure_high_pressure_recovery = datai_values[11]
    result.total_pressure_low_pressure_alarm = datai_values[12]
    result.total_pressure_low_pressure_recovery = datai_values[13]
    result.total_voltage_overvoltage_protection = datai_values[14]
    result.total_pressure_overpressure_recovery = datai_values[15]
    result.total_voltage_undervoltage_protection = datai_values[16]
    result.total_pressure_undervoltage_recovery = datai_values[17]
    result.charging_overvoltage_protection = datai_values[18]
    result.charging_overvoltage_recovery = datai_values[19]
    result.charging_high_temperature_warning = datai_values[20]
    result.charging_high_temperature_recovery = datai_values[21]
    result.charging_low_temperature_warning = datai_values[22]
    result.charging_low_temperature_recovery = datai_values[23]
    result.charging_over_temperature_protection = datai_values[24]
    result.charging_over_temperature_recovery = datai_values[25]
    result.charging_under_temperature_protection = datai_values[26]
    result.charging_under_temperature_recovery = datai_values[27]
    result.discharge_high_temperature_warning = datai_values[28]
    result.discharge_high_temperature_recovery = datai_values[29]
    result.discharge_low_temperature_warning = datai_values[30]
    result.discharge_low_temperature_recovery = datai_values[31]
    result.discharge_over_temperature_protection = datai_values[32]
    result.discharge_over_temperature_recovery = datai_values[33]
    result.discharge_under_temperature_protection = datai_values[34]
    result.discharge_under_temperature_recovery = datai_values[35]
    result.cell_low_temperature_heating = datai_values[36]
    result.cell_heating_recovery = datai_values[37]
    result.ambient_high_temperature_alarm = datai_values[38]
    result.ambient_high_temperature_recovery = datai_values[39]
    result.ambient_low_temperature_warning = datai_values[40]
    result.ambient_low_temperature_recovery = datai_values[41]
    result.fan_fault = datai_values[42]
    result.fan_fault_recovery = datai_values[43]
    result.can_communication_fault = datai_values[44]
    result.can_communication_fault_recovery = datai_values[45]
    result.mos_short_circuit_protection = datai_values[46]
    result.mos_short_circuit_protection_recovery = datai_values[47]
    result.power_high_temperature_recovery = datai_values[48]
    result.power_over_temperature_protection = datai_values[49]
    result.power_over_temperature_recovery = datai_values[50]
    result.charging_overcurrent_warning = datai_values[51]
    result.charging_overcurrent_recovery = datai_values[52]
    result.discharge_overcurrent_warning = datai_values[53]
    result.discharge_overcurrent_recovery = datai_values[54]
    result.charge_overcurrent_protection = datai_values[55]
    result.discharge_overcurrent_protection = datai_values[56]
    result.transient_overcurrent_protection = datai_values[57]
    result.output_soft_start_delay = datai_values[58]
    result.battery_rated_capacity = datai_values[59]
    result.soc = datai_values[60]
    result.cell_invalidation_differential_pressure = datai_values[61]
    result.cell_invalidation_recovery = datai_values[62]
    result.equalization_opening_pressure_difference = datai_values[63]
    result.equalization_closing_pressure_difference = datai_values[64]
    result.static_equilibrium_time = datai_values[65]
    result.battery_number_in_series = datai_values[66]
    result.charge_overcurrent_delay = datai_values[67]
    result.discharge_overcurrent_delay = datai_values[68]
    result.transient_overcurrent_delay = datai_values[69]
    result.overcurrent_delay_recovery = datai_values[70]
    result.overcurrent_recovery_times = datai_values[71]
    result.charge_current_limit_delay = datai_values[72]
    result.charge_activation_delay = datai_values[73]
    result.charge_activation_interval = datai_values[74]
    result.charge_activation_times = datai_values[75]
    result.work_record_interval = datai_values[76]
    result.standby_recording_interval = datai_values[77]
    result.standby_shutdown_delay = datai_values[78]
    result.remaining_capacity_alarm = datai_values[79]
    result.remaining_capacity_protection = datai_values[80]
    result.interval_charge_capacity = datai_values[81]
    result.cycle_cumulative_capacity = datai_values[82]
    result.connection_fault_impedance = datai_values[83]
    result.compensation_point_1_position = datai_values[84]
    result.compensation_point_1_impedance = datai_values[85]
    result.compensation_point_2_position = datai_values[86]
    result.compensation_point_2_impedance = datai_values[87]
    result.compensation_point_3_position = datai_values[88]
    result.compensation_point_3_impedance = datai_values[89]
    result.compensation_point_4_position = datai_values[90]
    result.compensation_point_4_impedance = datai_values[91]

    # Print the calculated values
    print("Monomer High Voltage Alarm:", result.monomer_high_voltage_alarm, "V")
    print("Monomer High Pressure Recovery:", result.monomer_high_pressure_recovery, "V")
    print("Monomer Low Pressure Alarm:", result.monomer_low_pressure_alarm, "V")
    print("Monomer Low Pressure Recovery:", result.monomer_low_pressure_recovery, "V")
    print("Monomer Overvoltage Protection:", result.monomer_overvoltage_protection, "V")
    print("Monomer Overvoltage Recovery:", result.monomer_overvoltage_recovery, "V")
    print("Monomer Undervoltage Protection:", result.monomer_undervoltage_protection, "V")
    print("Monomer Undervoltage Recovery:", result.monomer_undervoltage_recovery, "V")
    print("Equalization Opening Voltage:", result.equalization_opening_voltage, "V")
    print("Battery Low Voltage Forbidden Charging:", result.battery_low_voltage_forbidden_charging, "V")
    print("Total Pressure High Pressure Alarm:", result.total_pressure_high_pressure_alarm, "V")
    print("Total Pressure High Pressure Recovery:", result.total_pressure_high_pressure_recovery, "V")
    print("Total Pressure Low Pressure Alarm:", result.total_pressure_low_pressure_alarm, "V")
    print("Total Pressure Low Pressure Recovery:", result.total_pressure_low_pressure_recovery, "V")
    print("Total Voltage Overvoltage Protection:", result.total_voltage_overvoltage_protection, "V")
    print("Total Pressure Overpressure Recovery:", result.total_pressure_overpressure_recovery, "V")
    print("Total Voltage Undervoltage Protection:", result.total_voltage_undervoltage_protection, "V")
    print("Total Pressure Undervoltage Recovery:", result.total_pressure_undervoltage_recovery, "V")
    print("Charging Overvoltage Protection:", result.charging_overvoltage_protection, "V")
    print("Charging Overvoltage Recovery:", result.charging_overvoltage_recovery, "V")
    print("Charging High Temperature Warning:", result.charging_high_temperature_warning, "°C")
    print("Charging High Temperature Recovery:", result.charging_high_temperature_recovery, "°C")
    print("Charging Low Temperature Warning:", result.charging_low_temperature_warning, "°C")
    print("Charging Low Temperature Recovery:", result.charging_low_temperature_recovery, "°C")
    print("Charging Over Temperature Protection:", result.charging_over_temperature_protection, "°C")
    print("Charging Over Temperature Recovery:", result.charging_over_temperature_recovery, "°C")
    print("Charging Under Temperature Protection:", result.charging_under_temperature_protection, "°C")
    print("Charging Under Temperature Recovery:", result.charging_under_temperature_recovery, "°C")
    print("Discharge High Temperature Warning:", result.discharge_high_temperature_warning, "°C")
    print("Discharge High Temperature Recovery:", result.discharge_high_temperature_recovery, "°C")
    print("Discharge Low Temperature Warning:", result.discharge_low_temperature_warning, "°C")
    print("Discharge Low Temperature Recovery:", result.discharge_low_temperature_recovery, "°C")
    print("Discharge Over Temperature Protection:", result.discharge_over_temperature_protection, "°C")
    print("Discharge Over Temperature Recovery:", result.discharge_over_temperature_recovery, "°C")
    print("Discharge Under Temperature Protection:", result.discharge_under_temperature_protection, "°C")
    print("Discharge Under Temperature Recovery:", result.discharge_under_temperature_recovery, "°C")
    print("Cell Low Temperature Heating:", result.cell_low_temperature_heating, "°C")
    print("Cell Heating Recovery:", result.cell_heating_recovery, "°C")
    print("Ambient High Temperature Alarm:", result.ambient_high_temperature_alarm, "°C")
    print("Ambient High Temperature Recovery:", result.ambient_high_temperature_recovery, "°C")
    print("Ambient Low Temperature Warning:", result.ambient_low_temperature_warning, "°C")
    print("Ambient Low Temperature Recovery:", result.ambient_low_temperature_recovery, "°C")
    print("Fan Fault:", result.fan_fault, "times")
    print("Fan Fault Recovery:", result.fan_fault_recovery, "times")
    print("CAN Communication Fault:", result.can_communication_fault, "times")
    print("CAN Communication Fault Recovery:", result.can_communication_fault_recovery, "times")
    print("MOS Short Circuit Protection:", result.mos_short_circuit_protection, "times")
    print("MOS Short Circuit Protection Recovery:", result.mos_short_circuit_protection_recovery, "times")
    print("Power High Temperature Recovery:", result.power_high_temperature_recovery, "°C")
    print("Power Over Temperature Protection:", result.power_over_temperature_protection, "°C")
    print("Power Over Temperature Recovery:", result.power_over_temperature_recovery, "°C")
    print("Charging Overcurrent Warning:", result.charging_overcurrent_warning, "A")
    print("Charging Overcurrent Recovery:", result.charging_overcurrent_recovery, "A")
    print("Discharge Overcurrent Warning:", result.discharge_overcurrent_warning, "A")
    print("Discharge Overcurrent Recovery:", result.discharge_overcurrent_recovery, "A")
    print("Charge Overcurrent Protection:", result.charge_overcurrent_protection, "A")
    print("Discharge Overcurrent Protection:", result.discharge_overcurrent_protection, "A")
    print("Transient Overcurrent Protection:", result.transient_overcurrent_protection, "A")
    print("Output Soft Start Delay:", result.output_soft_start_delay, "ms")
    print("Battery Rated Capacity:", result.battery_rated_capacity, "Ah")
    print("SOC:", result.soc, "Ah")
    print("Cell Invalidation Differential Pressure:", result.cell_invalidation_differential_pressure, "V")
    print("Cell Invalidation Recovery:", result.cell_invalidation_recovery, "V")
    print("Equalization Opening Pressure Difference:", result.equalization_opening_pressure_difference, "V")
    print("Equalization Closing Pressure Difference:", result.equalization_closing_pressure_difference, "V")
    print("Static Equilibrium Time:", result.static_equilibrium_time, "times")
    print("Battery Number in Series:", result.battery_number_in_series, "strings")
    print("Charge Overcurrent Delay:", result.charge_overcurrent_delay, "s")
    print("Discharge Overcurrent Delay:", result.discharge_overcurrent_delay, "s")
    print("Transient Overcurrent Delay:", result.transient_overcurrent_delay, "s")
    print("Overcurrent Delay Recovery:", result.overcurrent_delay_recovery, "s")
    print("Overcurrent Recovery Times:", result.overcurrent_recovery_times, "times")
    print("Charge Current Limit Delay:", result.charge_current_limit_delay, "min")
    print("Charge Activation Delay:", result.charge_activation_delay, "min")
    print("Charge Activation Interval:", result.charge_activation_interval, "times")
    print("Charge Activation Times:", result.charge_activation_times, "times")
    print("Work Record Interval:", result.work_record_interval, "min")
    print("Standby Recording Interval:", result.standby_recording_interval, "min")
    print("Standby Shutdown Delay:", result.standby_shutdown_delay, "times")
    print("Remaining Capacity Alarm:", result.remaining_capacity_alarm, "%")
    print("Remaining Capacity Protection:", result.remaining_capacity_protection, "%")
    print("Interval Charge Capacity:", result.interval_charge_capacity, "%")
    print("Cycle Cumulative Capacity:", result.cycle_cumulative_capacity, "%")
    print("Connection Fault Impedance:", result.connection_fault_impedance, "mΩ")
    print("Compensation Point 1 Position:", result.compensation_point_1_position, "strings")
    print("Compensation Point 1 Impedance:", result.compensation_point_1_impedance, "mΩ")
    print("Compensation Point 2 Position:", result.compensation_point_2_position, "strings")
    print("Compensation Point 2 Impedance:", result.compensation_point_2_impedance, "mΩ")
    print("Compensation Point 3 Position:", result.compensation_point_3_position, "strings")
    print("Compensation Point 3 Impedance:", result.compensation_point_3_impedance, "mΩ")
    print("Compensation Point 4 Position:", result.compensation_point_4_position, "strings")
    print("Compensation Point 4 Impedance:", result.compensation_point_4_impedance, "mΩ")

    return result
