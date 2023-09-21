import logging
_LOGGER = logging.getLogger(__name__)
class ProtectionSettingsData:
    def __init__(self, settings=None):
        if settings is None:
            settings = [0] * 87  # Initialize with zeros if settings not provided
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
        self.ambient_low_temperature_alarm = settings[40]
        self.ambient_low_temperature_recovery = settings[41]
        self.environmental_over_temperature_protection = settings[42]
        self.environmental_overtemperature_recovery = settings[43]
        self.environmental_under_temperature_protection = settings[44]
        self.environmental_undertemperature_recovery = settings[45]
        self.power_high_temperature_alarm = settings[46]
        self.power_high_temperature_recovery = settings[47]
        self.power_over_temperature_protection = settings[48]
        self.power_over_temperature_recovery = settings[49]
        self.charging_overcurrent_warning = settings[50]
        self.charging_overcurrent_recovery = settings[51]
        self.discharge_overcurrent_warning = settings[52]
        self.discharge_overcurrent_recovery = settings[53]
        self.charge_overcurrent_protection = settings[54]
        self.discharge_overcurrent_protection = settings[55]
        self.transient_overcurrent_protection = settings[56]
        self.output_soft_start_delay = settings[57]
        self.battery_rated_capacity = settings[58]
        self.soc = settings[59]
        self.cell_invalidation_differential_pressure = settings[60]
        self.cell_invalidation_recovery = settings[61]
        self.equalization_opening_pressure_difference = settings[62]
        self.equalization_closing_pressure_difference = settings[63]
        self.static_equilibrium_time = settings[64]
        self.battery_number_in_series = settings[65]
        self.charge_overcurrent_delay = settings[66]
        self.discharge_overcurrent_delay = settings[67]
        self.transient_overcurrent_delay = settings[68]
        self.overcurrent_delay_recovery = settings[69]
        self.overcurrent_recovery_times = settings[70]
        self.charge_current_limit_delay = settings[71]
        self.charge_activation_delay = settings[72]
        self.charging_activation_interval = settings[73]
        self.charge_activation_times = settings[74]
        self.work_record_interval = settings[75]
        self.standby_recording_interval = settings[76]
        self.standby_shutdown_delay = settings[77]
        self.remaining_capacity_alarm = settings[78]
        self.remaining_capacity_protection = settings[79]
        self.interval_charge_capacity = settings[80]
        self.cycle_cumulative_capacity = settings[81]
        self.connection_fault_impedance = settings[82]
        self.compensation_point_1_position = settings[83]
        self.compensation_point_1_impedance = settings[84]
        self.compensation_point_2_position = settings[85]
        self.compensation_point_2_impedance = settings[86]

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
            f"Charging High Temperature Warning: {self.charging_high_temperature_warning} ℃\n"
            f"Charging High Temperature Recovery: {self.charging_high_temperature_recovery} ℃\n"
            f"Charging Low Temperature Warning: {self.charging_low_temperature_warning} ℃\n"
            f"Charging Low Temperature Recovery: {self.charging_low_temperature_recovery} ℃\n"
            f"Charging Over Temperature Protection: {self.charging_over_temperature_protection} ℃\n"
            f"Charging Over Temperature Recovery: {self.charging_over_temperature_recovery} ℃\n"
            f"Charging Under Temperature Protection: {self.charging_under_temperature_protection} ℃\n"
            f"Charging Under Temperature Recovery: {self.charging_under_temperature_recovery} ℃\n"
            f"Discharge High Temperature Warning: {self.discharge_high_temperature_warning} ℃\n"
            f"Discharge High Temperature Recovery: {self.discharge_high_temperature_recovery} ℃\n"
            f"Discharge Low Temperature Warning: {self.discharge_low_temperature_warning} ℃\n"
            f"Discharge Low Temperature Recovery: {self.discharge_low_temperature_recovery} ℃\n"
            f"Discharge Over Temperature Protection: {self.discharge_over_temperature_protection} ℃\n"
            f"Discharge Over Temperature Recovery: {self.discharge_over_temperature_recovery} ℃\n"
            f"Discharge Under Temperature Protection: {self.discharge_under_temperature_protection} ℃\n"
            f"Discharge Under Temperature Recovery: {self.discharge_under_temperature_recovery} ℃\n"
            f"Cell Low Temperature Heating: {self.cell_low_temperature_heating} ℃\n"
            f"Cell Heating Recovery: {self.cell_heating_recovery} ℃\n"
            f"Ambient High Temperature Alarm: {self.ambient_high_temperature_alarm} ℃\n"
            f"Ambient High Temperature Recovery: {self.ambient_high_temperature_recovery} ℃\n"
            f"Ambient Low Temperature Alarm: {self.ambient_low_temperature_alarm} ℃\n"
            f"Ambient Low Temperature Recovery: {self.ambient_low_temperature_recovery} ℃\n"
            f"Environmental Over Temperature Protection: {self.environmental_over_temperature_protection} ℃\n"
            f"Environmental Overtemperature Recovery: {self.environmental_overtemperature_recovery} ℃\n"
            f"Environmental Under Temperature Protection: {self.environmental_under_temperature_protection} ℃\n"
            f"Environmental Undertemperature Recovery: {self.environmental_undertemperature_recovery} ℃\n"
            f"Power High Temperature Alarm: {self.power_high_temperature_alarm} ℃\n"
            f"Power High Temperature Recovery: {self.power_high_temperature_recovery} ℃\n"
            f"Power Over Temperature Protection: {self.power_over_temperature_protection} ℃\n"
            f"Power Over Temperature Recovery: {self.power_over_temperature_recovery} ℃\n"
            f"Charging Overcurrent Warning: {self.charging_overcurrent_warning}\n"
            f"Charging Overcurrent Recovery: {self.charging_overcurrent_recovery}\n"
            f"Discharge Overcurrent Warning: {self.discharge_overcurrent_warning}\n"
            f"Discharge Overcurrent Recovery: {self.discharge_overcurrent_recovery}\n"
            f"Charge Overcurrent Protection: {self.charge_overcurrent_protection}\n"
            f"Discharge Overcurrent Protection: {self.discharge_overcurrent_protection}\n"
            f"Transient Overcurrent Protection: {self.transient_overcurrent_protection}\n"
            f"Output Soft Start Delay: {self.output_soft_start_delay} s\n"
            f"Battery Rated Capacity: {self.battery_rated_capacity} Ah\n"
            f"SOC: {self.soc}%\n"
            f"Cell Invalidation Differential Pressure: {self.cell_invalidation_differential_pressure} V\n"
            f"Cell Invalidation Recovery: {self.cell_invalidation_recovery} V\n"
            f"Equalization Opening Pressure Difference: {self.equalization_opening_pressure_difference} V\n"
            f"Equalization Closing Pressure Difference: {self.equalization_closing_pressure_difference} V\n"
            f"Static Equilibrium Time: {self.static_equilibrium_time} s\n"
            f"Battery Number in Series: {self.battery_number_in_series}\n"
            f"Charge Overcurrent Delay: {self.charge_overcurrent_delay} ms\n"
            f"Discharge Overcurrent Delay: {self.discharge_overcurrent_delay} ms\n"
            f"Transient Overcurrent Delay: {self.transient_overcurrent_delay} ms\n"
            f"Overcurrent Delay Recovery: {self.overcurrent_delay_recovery} ms\n"
            f"Overcurrent Recovery Times: {self.overcurrent_recovery_times}\n"
            f"Charge Current Limit Delay: {self.charge_current_limit_delay} ms\n"
            f"Charge Activation Delay: {self.charge_activation_delay} ms\n"
            f"Charging Activation Interval: {self.charging_activation_interval} ms\n"
            f"Charge Activation Times: {self.charge_activation_times}\n"
            f"Work Record Interval: {self.work_record_interval} s\n"
            f"Standby Recording Interval: {self.standby_recording_interval} s\n"
            f"Standby Shutdown Delay: {self.standby_shutdown_delay} s\n"
            f"Remaining Capacity Alarm: {self.remaining_capacity_alarm} Ah\n"
            f"Remaining Capacity Protection: {self.remaining_capacity_protection} Ah\n"
            f"Interval Charge Capacity: {self.interval_charge_capacity} Ah\n"
            f"Cycle Cumulative Capacity: {self.cycle_cumulative_capacity} Ah\n"
            f"Connection Fault Impedance: {self.connection_fault_impedance}\n"
            f"Compensation Point 1 Position: {self.compensation_point_1_position}\n"
            f"Compensation Point 1 Impedance: {self.compensation_point_1_impedance}\n"
            f"Compensation Point 2 Position: {self.compensation_point_2_position}\n"
            f"Compensation Point 2 Impedance: {self.compensation_point_2_impedance}\n"
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

    datai_values = [
        # Monomer high voltage alarm: 3.550 V
        int.from_bytes(datai_bytes[0:2], byteorder='big') / 1000.0,

        # Monomer high pressure recovery: 3.400 V
        int.from_bytes(datai_bytes[2:4], byteorder='big') / 1000.0,

        # Monomer low pressure alarm: 2.900 V
        int.from_bytes(datai_bytes[4:6], byteorder='big') / 1000.0,

        # Monomer low pressure recovery: 3.000 V
        int.from_bytes(datai_bytes[6:8], byteorder='big') / 1000.0,

        # Monomer overvoltage protection: 3.650 V
        int.from_bytes(datai_bytes[8:10], byteorder='big') / 1000.0,

        # Monomer overvoltage recovery: 3.400 V
        int.from_bytes(datai_bytes[10:12], byteorder='big') / 1000.0,

        # Monomer undervoltage protection: 2.700 V
        int.from_bytes(datai_bytes[12:14], byteorder='big') / 1000.0,

        # Monomer undervoltage recovery: 2.900 V
        int.from_bytes(datai_bytes[14:16], byteorder='big') / 1000.0,

        # Equalization opening voltage: 3.400 V
        int.from_bytes(datai_bytes[16:18], byteorder='big') / 1000.0,

        # Battery low voltage forbidden charging: 1.500 V
        int.from_bytes(datai_bytes[18:20], byteorder='big') / 1000.0,

        # Total pressure high pressure alarm: 58.00 V
        int.from_bytes(datai_bytes[20:22], byteorder='big') / 100.0,

        # Total pressure and high pressure recovery: 54.40 V
        int.from_bytes(datai_bytes[22:24], byteorder='big') / 100.0,

        # Total pressure low pressure alarm: 46.40 V
        int.from_bytes(datai_bytes[24:26], byteorder='big') / 100.0,

        # Total pressure and low pressure recovery: 48.00 V
        int.from_bytes(datai_bytes[26:28], byteorder='big') / 100.0,

        # Total_voltage overvoltage protection: 56.80 V
        int.from_bytes(datai_bytes[28:30], byteorder='big') / 100.0,

        # Total pressure overpressure recovery: 54.40 V
        int.from_bytes(datai_bytes[30:32], byteorder='big') / 100.0,

        # Total_voltage undervoltage protection: 41.60 V
        int.from_bytes(datai_bytes[32:34], byteorder='big') / 100.0,

        # Total pressure undervoltage recovery: 46.00 V
        int.from_bytes(datai_bytes[34:36], byteorder='big') / 100.0,

        # Charging overvoltage protection: 56.80 V
        int.from_bytes(datai_bytes[36:38], byteorder='big') / 100.0,

        # Charging overvoltage recovery: 56.80 V
        int.from_bytes(datai_bytes[38:40], byteorder='big') / 100.0,

        # Charging high temperature warning: 50.0 ℃
        (int.from_bytes(datai_bytes[40:42], byteorder='big')  - 2731) / 10.0,

        # Charging high temperature recovery: 47.0 ℃
        (int.from_bytes(datai_bytes[42:44], byteorder='big')  - 2731) / 10.0,

        # Charging low temperature warning: 2.0 ℃
        (int.from_bytes(datai_bytes[44:46], byteorder='big')  - 2731) / 10.0,

        # Charging low temperature recovery: 5.0 ℃
        (int.from_bytes(datai_bytes[46:48], byteorder='big')  - 2731) / 10.0,

        # Charging over temperature protection: 55.0 ℃
        (int.from_bytes(datai_bytes[48:50], byteorder='big')  - 2731) / 10.0,

        # Charging over temperature recovery: 50.0 ℃
        (int.from_bytes(datai_bytes[50:52], byteorder='big')  - 2731) / 10.0,

        # Charging under-temperature protection: -10.0 ℃
        (int.from_bytes(datai_bytes[52:54], byteorder='big')  - 2731) / 10.0,

        # Charging under temperature recovery: 0.0 ℃
        (int.from_bytes(datai_bytes[54:56], byteorder='big')  - 2731) / 10.0,

        # Discharge high temperature warning: 52.0 ℃
        (int.from_bytes(datai_bytes[56:58], byteorder='big')  - 2731) / 10.0,

        # Discharge high temperature recovery: 47.0 ℃
        (int.from_bytes(datai_bytes[58:60], byteorder='big')  - 2731) / 10.0,

        # Discharge low temperature warning: -10.0 ℃
        (int.from_bytes(datai_bytes[60:62], byteorder='big')  - 2731) / 10.0,

        # Discharge low temperature recovery: 3.0 ℃
        (int.from_bytes(datai_bytes[62:64], byteorder='big')  - 2731) / 10.0,

        # Discharge over temperature protection: 60.0 ℃
        (int.from_bytes(datai_bytes[64:66], byteorder='big')  - 2731) / 10.0,

        # Discharge over temperature recovery: 55.0 ℃
        (int.from_bytes(datai_bytes[66:68], byteorder='big')  - 2731) / 10.0,

        # Discharge under temperature protection: -20.0 ℃
        (int.from_bytes(datai_bytes[68:70], byteorder='big')  - 2731) / 10.0,

        # Discharge under temperature recovery: -10.0 ℃
        (int.from_bytes(datai_bytes[70:72], byteorder='big')  - 2731) / 10.0,

        # Cell low temperature heating
        (int.from_bytes(datai_bytes[72:74], byteorder='big')  - 2731) / 10.0,

        # Cell heating recovery
        (int.from_bytes(datai_bytes[74:76], byteorder='big')  - 2731) / 10.0,

        # Ambient high temperature alarm
        (int.from_bytes(datai_bytes[76:78], byteorder='big')  - 2731) / 10.0,

        # Ambient high temperature recovery
        (int.from_bytes(datai_bytes[78:80], byteorder='big')  - 2731) / 10.0,

        # Ambient low temperature alarm
        (int.from_bytes(datai_bytes[80:82], byteorder='big')  - 2731) / 10.0,

        # Ambient low temperature recovery
        (int.from_bytes(datai_bytes[82:84], byteorder='big')  - 2731) / 10.0,

        # Environmental over-temperature protection
        (int.from_bytes(datai_bytes[84:86], byteorder='big')  - 2731) / 10.0,

        # Environmental overtemperature recovery
        (int.from_bytes(datai_bytes[86:88], byteorder='big')  - 2731) / 10.0,

        # Environmental under-temperature protection
        (int.from_bytes(datai_bytes[88:90], byteorder='big')  - 2731) / 10.0,

        # Environmental undertemperature recovery
        (int.from_bytes(datai_bytes[90:92], byteorder='big')  - 2731) / 10.0,

        # Power high temperature alarm
        (int.from_bytes(datai_bytes[92:94], byteorder='big')  - 2731) / 10.0,

        # Power high temperature recovery
        (int.from_bytes(datai_bytes[94:96], byteorder='big')  - 2731) / 10.0,

        # Power over temperature protection
        (int.from_bytes(datai_bytes[96:98], byteorder='big')  - 2731) / 10.0,

        # Power over temperature recovery
        (int.from_bytes(datai_bytes[98:100], byteorder='big')  - 2731) / 10.0,

        # Charging overcurrent warning
        int.from_bytes(datai_bytes[100:102], byteorder='big') / 10.0,

        # Charging overcurrent recovery
        int.from_bytes(datai_bytes[102:104], byteorder='big') / 10.0,

        # Discharge overcurrent warning
        int.from_bytes(datai_bytes[104:106], byteorder='big') / 10.0,

        # Discharge overcurrent recovery
        int.from_bytes(datai_bytes[106:108], byteorder='big') / 10.0,

        # Charge overcurrent protection
        int.from_bytes(datai_bytes[108:110], byteorder='big') / 10.0,

        # Discharge overcurrent protection
        int.from_bytes(datai_bytes[110:112], byteorder='big') / 10.0,

        # Transient overcurrent protection
        int.from_bytes(datai_bytes[112:114], byteorder='big') / 10.0,


        # Output soft start delay
        int.from_bytes(datai_bytes[114:116], byteorder='big') / 1000.0,

        # Battery rated capacity
        int.from_bytes(datai_bytes[116:118], byteorder='big') / 100.0,

        # SOC
        int.from_bytes(datai_bytes[118:120], byteorder='big') / 100.0,

        # Cell invalidation differential pressure
        int.from_bytes(datai_bytes[120:122], byteorder='big') / 1000.0,

        # Cell invalidation recovery
        int.from_bytes(datai_bytes[122:124], byteorder='big') / 1000.0,

        # Equalization opening pressure difference
        int.from_bytes(datai_bytes[124:126], byteorder='big') / 1000.0,

        # Equalization closing pressure difference
        int.from_bytes(datai_bytes[126:128], byteorder='big') / 1000.0,

        # Static equilibrium time
        int.from_bytes(datai_bytes[128:130], byteorder='big'),

        # Battery number in series
        int.from_bytes(datai_bytes[130:132], byteorder='big'),

        # Charge overcurrent delay
        int.from_bytes(datai_bytes[132:134], byteorder='big'),

        # Discharge overcurrent delay
        int.from_bytes(datai_bytes[134:136], byteorder='big'),

        # Transient overcurrent delay
        int.from_bytes(datai_bytes[136:138], byteorder='big'),

        # Overcurrent delay recovery
        int.from_bytes(datai_bytes[138:140], byteorder='big'),

        # Overcurrent recovery times
        int.from_bytes(datai_bytes[140:142], byteorder='big'),

        # Charge current limit delay
        int.from_bytes(datai_bytes[142:144], byteorder='big'),

        # Charge activation delay
        int.from_bytes(datai_bytes[144:146], byteorder='big'),

        # Charging activation interval
        int.from_bytes(datai_bytes[146:148], byteorder='big'),

        # Charge activation times
        int.from_bytes(datai_bytes[148:150], byteorder='big'),

        # Work record interval
        int.from_bytes(datai_bytes[150:152], byteorder='big'),

        # Standby recording interval
        int.from_bytes(datai_bytes[152:154], byteorder='big'),

        # Standby shutdown delay
        int.from_bytes(datai_bytes[154:156], byteorder='big'),

        # Remaining capacity alarm
        int.from_bytes(datai_bytes[156:158], byteorder='big') / 100.0,

        # Remaining capacity protection
        int.from_bytes(datai_bytes[158:160], byteorder='big') / 100.0,

        # Interval charge capacity
        int.from_bytes(datai_bytes[160:162], byteorder='big') / 100.0,

        # Cycle cumulative capacity
        int.from_bytes(datai_bytes[162:164], byteorder='big') / 100.0,

        # Connection fault impedance
        int.from_bytes(datai_bytes[164:166], byteorder='big'),

        # Compensation point 1 position
        int.from_bytes(datai_bytes[166:168], byteorder='big'),

        # Compensation point 1 impedance
        int.from_bytes(datai_bytes[168:170], byteorder='big'),

        # Compensation point 2 position
        int.from_bytes(datai_bytes[170:172], byteorder='big'),

        # Compensation point 2 impedance
        int.from_bytes(datai_bytes[172:174], byteorder='big')

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
    result.ambient_low_temperature_alarm = datai_values[40]
    result.ambient_low_temperature_recovery = datai_values[41]
    result.environmental_over_temperature_protection = datai_values[42]
    result.environmental_overtemperature_recovery = datai_values[43]
    result.environmental_under_temperature_protection = datai_values[44]
    result.environmental_undertemperature_recovery = datai_values[45]
    result.power_high_temperature_alarm = datai_values[46]
    result.power_high_temperature_recovery = datai_values[47]
    result.power_over_temperature_protection = datai_values[48]
    result.power_over_temperature_recovery = datai_values[49]
    result.charging_overcurrent_warning = datai_values[50]
    result.charging_overcurrent_recovery = datai_values[51]
    result.discharge_overcurrent_warning = datai_values[52]
    result.discharge_overcurrent_recovery = datai_values[53]
    result.charge_overcurrent_protection = datai_values[54]
    result.discharge_overcurrent_protection = datai_values[55]
    result.transient_overcurrent_protection = datai_values[56]
    result.output_soft_start_delay = datai_values[57]
    result.battery_rated_capacity = datai_values[58]
    result.soc_ah = datai_values[59]
    result.cell_invalidation_differential_pressure = datai_values[60]
    result.cell_invalidation_recovery = datai_values[61]
    result.equalization_opening_pressure_difference = datai_values[62]
    result.equalization_closing_pressure_difference = datai_values[63]
    result.static_equilibrium_time = datai_values[64]
    result.battery_number_in_series = datai_values[65]
    result.charge_overcurrent_delay = datai_values[66]
    result.discharge_overcurrent_delay = datai_values[67]
    result.transient_overcurrent_delay = datai_values[68]
    result.overcurrent_delay_recovery = datai_values[69]
    result.overcurrent_recovery_times = datai_values[70]
    result.charge_current_limit_delay = datai_values[71]
    result.charge_activation_delay = datai_values[72]
    result.charging_activation_interval = datai_values[73]
    result.charge_activation_times = datai_values[74]
    result.work_record_interval = datai_values[75]
    result.standby_recording_interval = datai_values[76]
    result.standby_shutdown_delay = datai_values[77]
    result.remaining_capacity_alarm = datai_values[78]
    result.remaining_capacity_protection = datai_values[79]
    result.interval_charge_capacity = datai_values[80]
    result.cycle_cumulative_capacity = datai_values[81]
    result.connection_fault_impedance = datai_values[82]
    result.compensation_point_1_position = datai_values[83]
    result.compensation_point_1_impedance = datai_values[84]
    result.compensation_point_2_position = datai_values[85]
    result.compensation_point_2_impedance = datai_values[86]



    return result