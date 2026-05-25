from .const import (
    ALARM_MAPPINGS,
)

def extract_data(data):
    battery_address, telemetry, alarms, system_details, protection_settings = data
    return telemetry

def interpret_alarm(event, value):
    flags = ALARM_MAPPINGS.get(event, [])

    if not flags:
        return f"Unknown event: {event}"

    # For other alarm events, interpret them as bit flags
    triggered_alarms = [flag for idx, flag in enumerate(flags) if value is not None and value & (1 << idx)]
    #return ', '.join(str(triggered_alarms)) if triggered_alarms else "No Alarm"

    return ', '.join(str(alarm) for alarm in triggered_alarms) if triggered_alarms else "No Alarm"

def extract_alarms(data):
    battery_address, telemetry, alarms, system_details, protection_settings = data
    return alarms

def battery_watts(data):
    telemetry = extract_data(data)
    volts = getattr(telemetry, 'portVoltage', 0.0)
    amps = getattr(telemetry, 'current', 0.0)
    if isinstance(volts, float | int) and isinstance(amps, float | int):
        return int(round(volts * amps))
    return 0

def remaining_watts(data):
    telemetry = extract_data(data)
    volts = getattr(telemetry, 'voltage', 0.0)
    amps = getattr(telemetry, 'resCap', 0.0)
    return int(round(volts * amps))

def capacity_watts(data):
    telemetry = extract_data(data)
    volts = getattr(telemetry, 'voltage', 0.0)
    amps = getattr(telemetry, 'capacity', 0.0)
    return int(round(volts * amps))

def full_charge_amps(data):
    telemetry = extract_data(data)
    remaining = getattr(telemetry, 'resCap', 0.0)
    capacity = getattr(telemetry, 'capacity', 0.0)
    return int(round(capacity - remaining))

def full_charge_watts(data):
    telemetry = extract_data(data)
    voltage = getattr(telemetry, 'voltage', 0.0)
    resCap = getattr(telemetry, 'resCap', 0.0)
    capacity = getattr(telemetry, 'capacity', 0.0)
    remaining_w = voltage * resCap
    cap_w = voltage * capacity
    return int(round(cap_w - remaining_w))

def get_cell_extremes_and_difference(data):
    telemetry = extract_data(data)
    cell_voltages = getattr(telemetry, "cellVoltage", 0.0)
    highest_cell_voltage = max(cell_voltages)
    lowest_cell_voltage = min(cell_voltages)
    highest_cell_number = cell_voltages.index(highest_cell_voltage) + 1
    lowest_cell_number = cell_voltages.index(lowest_cell_voltage) + 1
    difference = highest_cell_voltage - lowest_cell_voltage
    return highest_cell_voltage, lowest_cell_voltage, difference, highest_cell_number, lowest_cell_number

def highest_cell_voltage(data):
    return get_cell_extremes_and_difference(data)[0]

def lowest_cell_voltage(data):
    return get_cell_extremes_and_difference(data)[1]

def cell_voltage_difference(data):
    return get_cell_extremes_and_difference(data)[2]

def highest_cell_number(data):
    return get_cell_extremes_and_difference(data)[3]

def lowest_cell_number(data):
    return get_cell_extremes_and_difference(data)[4]

def highest_temp(data):
    telemetry = extract_data(data)
    return max(getattr(telemetry, 'temperatures', [0.0]))

def lowest_temp(data):
    telemetry = extract_data(data)
    return min(getattr(telemetry, 'temperatures', [0.0]))

def delta_temp(data):
    telemetry = extract_data(data)
    temps = getattr(telemetry, 'temperatures', [])
    if temps:
        return max(temps) - min(temps)
    return 0.0

def highest_temp_sensor(data):
    telemetry = extract_data(data)
    telemetry = extract_data(data)
    temps = getattr(telemetry, 'temperatures', [])
    if temps:
        return f"Sensor {temps.index(max(temps)) + 1}"
    return "N/A"

def lowest_temp_sensor(data):
    telemetry = extract_data(data)
    telemetry = extract_data(data)
    temps = getattr(telemetry, 'temperatures', [])
    if temps:
        return f"Sensor {temps.index(min(temps)) + 1}"
    return "N/A"

def balancer_active(cell_number, data):
    """Check if a specific cell's balancer is active using direct bitmask operations.
    Cells 1-8 use equilibriumState0 (bits 0-7), cells 9-16 use equilibriumState1 (bits 0-7).
    """
    alarms = extract_alarms(data)
    if cell_number < 1 or cell_number > 16:
        return False
    if cell_number <= 8:
        state = getattr(alarms, 'equilibriumState0', 0)
        bit = 1 << (cell_number - 1)
    else:
        state = getattr(alarms, 'equilibriumState1', 0)
        bit = 1 << (cell_number - 9)
    return bool(state & bit)

def balancer_cell_1(data): return balancer_active(1, data)
def balancer_cell_2(data): return balancer_active(2, data)
def balancer_cell_3(data): return balancer_active(3, data)
def balancer_cell_4(data): return balancer_active(4, data)
def balancer_cell_5(data): return balancer_active(5, data)
def balancer_cell_6(data): return balancer_active(6, data)
def balancer_cell_7(data): return balancer_active(7, data)
def balancer_cell_8(data): return balancer_active(8, data)
def balancer_cell_9(data): return balancer_active(9, data)
def balancer_cell_10(data): return balancer_active(10, data)
def balancer_cell_11(data): return balancer_active(11, data)
def balancer_cell_12(data): return balancer_active(12, data)
def balancer_cell_13(data): return balancer_active(13, data)
def balancer_cell_14(data): return balancer_active(14, data)
def balancer_cell_15(data): return balancer_active(15, data)
def balancer_cell_16(data): return balancer_active(16, data)
