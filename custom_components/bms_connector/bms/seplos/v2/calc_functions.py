def extract_data(data):
    battery_address, telemetry, alarms, system_details, protection_settings = data
    return telemetry
    
def battery_watts(data):
    telemetry = extract_data(data)
    volts = getattr(telemetry, 'portVoltage', 0.0)
    amps = getattr(telemetry, 'current', 0.0)
    if isinstance(volts, (float, int)) and isinstance(amps, (float, int)):
        return volts * amps
    return 0.0  # Handle the case when volts or amps are not numeric values

def remaining_watts(data):
    telemetry = extract_data(data)
    volts = getattr(telemetry, 'voltage', 0.0)
    amps = getattr(telemetry, 'resCap', 0.0)
    return volts * amps

def capacity_watts(data):
    telemetry = extract_data(data)
    volts = getattr(telemetry, 'voltage', 0.0)
    amps = getattr(telemetry, 'capacity', 0.0)
    return volts * amps

def full_charge_amps(data):
    telemetry = extract_data(data)
    remaining = getattr(telemetry, 'resCap', 0.0)
    capacity = getattr(telemetry, 'capacity', 0.0)
    return capacity - remaining

def full_charge_watts(data):
    telemetry = extract_data(data)
    voltage = getattr(telemetry, 'voltage', 0.0)
    resCap = getattr(telemetry, 'resCap', 0.0)
    capacity = getattr(telemetry, 'capacity', 0.0)
    remaining_w = voltage * resCap
    cap_w = voltage * capacity
    return cap_w - remaining_w

def get_cell_extremes_and_difference(data):
    telemetry = extract_data(data)
    cell_voltages = getattr(telemetry, f"cellVoltage", 0.0)
    highest_cell_voltage = max(cell_voltages)
    lowest_cell_voltage = min(cell_voltages)
    highest_cell_number = cell_voltages.index(highest_cell_voltage) + 1
    lowest_cell_number = cell_voltages.index(lowest_cell_voltage) + 1
    difference = highest_cell_voltage - lowest_cell_voltage
    return highest_cell_voltage, lowest_cell_voltage, difference, highest_cell_number, lowest_cell_number

def highest_cell_voltage(data):
    telemetry = extract_data(data)
    return get_cell_extremes_and_difference(data)[0]

def lowest_cell_voltage(data):
    telemetry = extract_data(data)
    return get_cell_extremes_and_difference(data)[1]

def cell_voltage_difference(data):
    telemetry = extract_data(data)
    return get_cell_extremes_and_difference(data)[2]

def highest_cell_number(data):
    telemetry = extract_data(data)
    return get_cell_extremes_and_difference(data)[3]

def lowest_cell_number(data):
    telemetry = extract_data(data)
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
    temps = getattr(telemetry, 'temperatures', [])
    if temps:
        return f"Sensor {temps.index(max(temps)) + 1}"
    return "N/A"

def lowest_temp_sensor(data):
    telemetry = extract_data(data)
    temps = getattr(telemetry, 'temperatures', [])
    if temps:
        return f"Sensor {temps.index(min(temps)) + 1}"
    return "N/A"