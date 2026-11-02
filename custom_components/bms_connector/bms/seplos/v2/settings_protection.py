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



# Settings field table for the 0x47 block.
# (attribute, offset, width, signed, addend, scale)
#
# The first 60 fields are 2-byte big-endian words (offsets 0-119). From
# offset 120 the protocol switches to single-byte fields; byte 123 is
# padding. Reading 2 bytes past 120 shifts every subsequent field and
# eventually lands in the ASCII model string.
FIELD_SPEC = (
    ("monomer_high_voltage_alarm", 0, 2, False, 0, 0.001),
    ("monomer_high_pressure_recovery", 2, 2, False, 0, 0.001),
    ("monomer_low_pressure_alarm", 4, 2, False, 0, 0.001),
    ("monomer_low_pressure_recovery", 6, 2, False, 0, 0.001),
    ("monomer_overvoltage_protection", 8, 2, False, 0, 0.001),
    ("monomer_overvoltage_recovery", 10, 2, False, 0, 0.001),
    ("monomer_undervoltage_protection", 12, 2, False, 0, 0.001),
    ("monomer_undervoltage_recovery", 14, 2, False, 0, 0.001),
    ("equalization_opening_voltage", 16, 2, False, 0, 0.001),
    ("battery_low_voltage_forbidden_charging", 18, 2, False, 0, 0.001),
    ("total_pressure_high_pressure_alarm", 20, 2, False, 0, 0.01),
    ("total_pressure_high_pressure_recovery", 22, 2, False, 0, 0.01),
    ("total_pressure_low_pressure_alarm", 24, 2, False, 0, 0.01),
    ("total_pressure_low_pressure_recovery", 26, 2, False, 0, 0.01),
    ("total_voltage_overvoltage_protection", 28, 2, False, 0, 0.01),
    ("total_pressure_overpressure_recovery", 30, 2, False, 0, 0.01),
    ("total_voltage_undervoltage_protection", 32, 2, False, 0, 0.01),
    ("total_pressure_undervoltage_recovery", 34, 2, False, 0, 0.01),
    ("charging_overvoltage_protection", 36, 2, False, 0, 0.01),
    ("charging_overvoltage_recovery", 38, 2, False, 0, 0.01),
    ("charging_high_temperature_warning", 40, 2, False, -2731, 0.1),
    ("charging_high_temperature_recovery", 42, 2, False, -2731, 0.1),
    ("charging_low_temperature_warning", 44, 2, False, -2731, 0.1),
    ("charging_low_temperature_recovery", 46, 2, False, -2731, 0.1),
    ("charging_over_temperature_protection", 48, 2, False, -2731, 0.1),
    ("charging_over_temperature_recovery", 50, 2, False, -2731, 0.1),
    ("charging_under_temperature_protection", 52, 2, False, -2731, 0.1),
    ("charging_under_temperature_recovery", 54, 2, False, -2731, 0.1),
    ("discharge_high_temperature_warning", 56, 2, False, -2731, 0.1),
    ("discharge_high_temperature_recovery", 58, 2, False, -2731, 0.1),
    ("discharge_low_temperature_warning", 60, 2, False, -2731, 0.1),
    ("discharge_low_temperature_recovery", 62, 2, False, -2731, 0.1),
    ("discharge_over_temperature_protection", 64, 2, False, -2731, 0.1),
    ("discharge_over_temperature_recovery", 66, 2, False, -2731, 0.1),
    ("discharge_under_temperature_protection", 68, 2, False, -2731, 0.1),
    ("discharge_under_temperature_recovery", 70, 2, False, -2731, 0.1),
    ("cell_low_temperature_heating", 72, 2, False, -2731, 0.1),
    ("cell_heating_recovery", 74, 2, False, -2731, 0.1),
    ("ambient_high_temperature_alarm", 76, 2, False, -2731, 0.1),
    ("ambient_high_temperature_recovery", 78, 2, False, -2731, 0.1),
    ("ambient_low_temperature_alarm", 80, 2, False, -2731, 0.1),
    ("ambient_low_temperature_recovery", 82, 2, False, -2731, 0.1),
    ("environmental_over_temperature_protection", 84, 2, False, -2731, 0.1),
    ("environmental_overtemperature_recovery", 86, 2, False, -2731, 0.1),
    ("environmental_under_temperature_protection", 88, 2, False, -2731, 0.1),
    ("environmental_undertemperature_recovery", 90, 2, False, -2731, 0.1),
    ("power_high_temperature_alarm", 92, 2, False, -2731, 0.1),
    ("power_high_temperature_recovery", 94, 2, False, -2731, 0.1),
    ("power_over_temperature_protection", 96, 2, False, -2731, 0.1),
    ("power_over_temperature_recovery", 98, 2, False, -2731, 0.1),
    ("charging_overcurrent_warning", 100, 2, False, 0, 0.01),
    ("charging_overcurrent_recovery", 102, 2, False, 0, 0.01),
    ("discharge_overcurrent_warning", 104, 2, True, 0, 0.01),
    ("discharge_overcurrent_recovery", 106, 2, True, 0, 0.01),
    ("charge_overcurrent_protection", 108, 2, False, 0, 0.01),
    ("discharge_overcurrent_protection", 110, 2, True, 0, 0.01),
    ("transient_overcurrent_protection", 112, 2, True, 0, 0.01),
    ("output_soft_start_delay", 114, 2, False, 0, 1),
    ("battery_rated_capacity", 116, 2, False, 0, 0.01),
    ("soc_ah", 118, 2, False, 0, 0.01),
    ("cell_invalidation_differential_pressure", 121, 1, False, 0, 0.01),
    ("cell_invalidation_recovery", 122, 1, False, 0, 0.01),
    ("equalization_opening_pressure_difference", 123, 1, False, 0, 0.001),
    ("equalization_closing_pressure_difference", 124, 1, False, 0, 0.001),
    ("static_equilibrium_time", 125, 1, False, 0, 1),
    ("battery_number_in_series", 126, 1, False, 0, 1),
    ("charge_overcurrent_delay", 127, 1, False, 0, 1),
    ("discharge_overcurrent_delay", 128, 1, False, 0, 1),
    ("transient_overcurrent_delay", 129, 1, False, 0, 1),
    ("overcurrent_delay_recovery", 130, 1, False, 0, 1),
    ("overcurrent_recovery_times", 131, 1, False, 0, 1),
    ("charge_current_limit_delay", 132, 1, False, 0, 1),
    ("charge_activation_delay", 133, 1, False, 0, 1),
    ("charging_activation_interval", 134, 1, False, 0, 1),
    ("charge_activation_times", 135, 1, False, 0, 1),
    ("work_record_interval", 136, 1, False, 0, 1),
    ("standby_recording_interval", 137, 1, False, 0, 1),
    ("standby_shutdown_delay", 138, 1, False, 0, 1),
    ("remaining_capacity_alarm", 139, 1, False, 0, 1),
    ("remaining_capacity_protection", 140, 1, False, 0, 1),
    ("interval_charge_capacity", 141, 1, False, 0, 1),
    ("cycle_cumulative_capacity", 142, 1, False, 0, 1),
    ("connection_fault_impedance", 143, 1, False, 0, 0.1),
    ("compensation_point_1_position", 144, 1, False, 0, 1),
    ("compensation_point_1_impedance", 145, 1, False, 0, 0.1),
    ("compensation_point_2_position", 146, 1, False, 0, 1),
    ("compensation_point_2_impedance", 147, 1, False, 0, 0.1),
)


def decode_fourseven(hex_string):
    """Decode the 0x47 settings payload into ProtectionSettingsData."""
    result = ProtectionSettingsData()

    if hex_string.startswith("~"):
        hex_string = hex_string[1:]

    try:
        raw = bytes.fromhex(hex_string)
    except ValueError:
        _LOGGER.error("Settings payload is not valid hex")
        return None

    if len(raw) < 8:
        return None

    # The caller passes LEN(2) + INFO; skip the length field.
    datai = raw[2:]
    if datai and datai[-1] == 0x0D:
        datai = datai[:-1]

    for name, offset, width, signed, addend, scale in FIELD_SPEC:
        chunk = datai[offset:offset + width]
        if len(chunk) != width:
            setattr(result, name, None)
            continue
        value = int.from_bytes(chunk, byteorder="big", signed=signed)
        value = (value + addend) * scale
        setattr(result, name, round(value, 4) if scale < 1 else value)

    return result
