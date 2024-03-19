from homeassistant.helpers.entity import Entity, DeviceInfo
ALARM_MAPPINGS = {
    "alarmEvent0": [
        "No Alarm", 
        "Alarm that analog quantity reaches the lower limit", 
        "Alarm that analog quantity reaches the upper limit", 
        "Other alarms"
    ],
    "alarmEvent1": [
        "Voltage sensor fault", 
        "Temperature sensor fault", 
        "Current sensor fault", 
        "Key switch fault", 
        "Cell voltage dropout fault", 
        "Charge switch fault", 
        "Discharge switch fault", 
        "Current limit switch fault"
    ],
    "alarmEvent2": [
        "Monomer high voltage alarm", 
        "Monomer overvoltage protection", 
        "Monomer low voltage alarm", 
        "Monomer under voltage protection", 
        "High voltage alarm for total voltage", 
        "Overvoltage protection for total voltage", 
        "Low voltage alarm for total voltage", 
        "Under voltage protection for total voltage"
    ],
    "alarmEvent3": [
        "Charge high temperature alarm", 
        "Charge over temperature protection", 
        "Charge low temperature alarm", 
        "Charge under temperature protection", 
        "Discharge high temperature alarm", 
        "Discharge over temperature protection", 
        "Discharge low temperature alarm", 
        "Discharge under temperature protection"
    ],
    "alarmEvent4": [
        "Environment high temperature alarm", 
        "Environment over temperature protection", 
        "Environment low temperature alarm", 
        "Environment under temperature protection", 
        "Power over temperature protection", 
        "Power high temperature alarm", 
        "Cell low temperature heating", 
        "Reservation bit"
    ],
    "alarmEvent5": [
        "Charge over current alarm", 
        "Charge over current protection", 
        "Discharge over current alarm", 
        "Discharge over current protection", 
        "Transient over current protection", 
        "Output short circuit protection", 
        "Transient over current lockout", 
        "Output short circuit lockout"
    ],
    "alarmEvent6": [
        "Charge high voltage protection", 
        "Intermittent recharge waiting", 
        "Residual capacity alarm", 
        "Residual capacity protection", 
        "Cell low voltage charging prohibition", 
        "Output reverse polarity protection", 
        "Output connection fault", 
        "Inside bit"
    ],
    "alarmEvent7": [
        "Inside bit", 
        "Inside bit", 
        "Inside bit", 
        "Inside bit", 
        "Automatic charging waiting", 
        "Manual charging waiting", 
        "Inside bit", 
        "Inside bit"
    ],
    "alarmEvent8": [
        "EEP storage fault", 
        "RTC error", 
        "Voltage calibration not performed", 
        "Current calibration not performed", 
        "Zero calibration not performed", 
        "Inside bit", 
        "Inside bit", 
        "Inside bit"
    ],
    "cellAlarm": {
        0: "No Alarm",
        1: "Alarm"
    },
    "tempAlarm": {
        0: "No Alarm",
        1: "Alarm"
    },
    "currentAlarm": {
        1: "Charge/Discharge Current Alarm"
    },
    "voltageAlarm": {
        1: "Total Battery Voltage Alarm"
    },
    "onOffState": [
        "Discharge switch state",
        "Charge switch state",
        "Current limit switch state",
        "Heating switch state",
        "Reservation bit",
        "Reservation bit",
        "Reservation bit",
        "Reservation bit"
    ],
    "equilibriumState0": [
        "Cell 01 equilibrium",
        "Cell 02 equilibrium",
        "Cell 03 equilibrium",
        "Cell 04 equilibrium",
        "Cell 05 equilibrium",
        "Cell 06 equilibrium",
        "Cell 07 equilibrium",
        "Cell 08 equilibrium"
    ],
    "equilibriumState1": [
        "Cell 09 equilibrium",
        "Cell 10 equilibrium",
        "Cell 11 equilibrium",
        "Cell 12 equilibrium",
        "Cell 13 equilibrium",
        "Cell 14 equilibrium",
        "Cell 15 equilibrium",
        "Cell 16 equilibrium"
    ],
    "systemState": [
        "Discharge",
        "Charge",
        "Floating charge",
        "Reservation bit",
        "Standby",
        "Shutdown",
        "Reservation bit",
        "Reservation bit"
    ],
    "disconnectionState0": [
        "Cell 01 disconnection",
        "Cell 02 disconnection",
        "Cell 03 disconnection",
        "Cell 04 disconnection",
        "Cell 05 disconnection",
        "Cell 06 disconnection",
        "Cell 07 disconnection",
        "Cell 08 disconnection"
    ],
    "disconnectionState1": [
        "Cell 09 disconnection",
        "Cell 10 disconnection",
        "Cell 11 disconnection",
        "Cell 12 disconnection",
        "Cell 13 disconnection",
        "Cell 14 disconnection",
        "Cell 15 disconnection",
        "Cell 16 disconnection"
    ]
}
async def process_cid_44(CID_44_RESPONSE, battery_address, name_prefix, entry, lowest_voltage_value, highest_voltage_value, cellsCount, cellVoltage):
    sensors = {}
    data_coll = {}
    binary_sensors = {}
    info_str = CID_44_RESPONSE

    def get_value(battery_address, data, attribute):
        """Retrieve the value from the data based on the attribute name."""
        # Check if the attribute name indicates list access (e.g., 'cellVoltages[0]')
        if '[' in attribute and ']' in attribute:
            attr, index = attribute.split('[')
            index = int(index.rstrip(']'))  # Convert index to integer
            # Check if the attribute exists in data and is a list
            if attr in data and isinstance(data[attr], list):
                list_data = data[attr]
                if index < len(list_data):
                    return list_data[index]  # Return the value at the specified index
        else:
            # For non-list attributes, directly access the dictionary
            return data.get(attribute, None)  # Safely return None if key doesn't exist

        return None  # Return None if attribute format is incorrect or index is out of range

    def interpret_alarm(event, value):
        """Interpret the alarm based on the event and value."""
        flags = ALARM_MAPPINGS.get(event, [])

        if not flags:
            return f"Unknown event: {event}"

        # Interpret the value as bit flags
        triggered_alarms = [flag for idx, flag in enumerate(flags) if value is not None and value & (1 << idx)]
        return ', '.join(str(alarm) for alarm in triggered_alarms) if triggered_alarms else "No Alarm"

    if info_str.startswith("~"):
        info_str = info_str[1:]

    msg_wo_chk_sum = info_str[:-4]
    info_str = msg_wo_chk_sum[12:]
    cursor = 4
    result = {}

    def remaining_length():
        return len(info_str) - cursor

    # Assign cellsCount to the result dictionary
    result['cellsCount'] = int(info_str[cursor:cursor+2], 16)
    cursor += 2

    # Initialize cellAlarm as a list in the result dictionary
    result['cellAlarm'] = []
    for _ in range(result['cellsCount']):
        if remaining_length() < 2:
            return result
        result['cellAlarm'].append(int(info_str[cursor:cursor+2], 16))
        cursor += 2

    # Assign tempCount to the result dictionary
    result['tempCount'] = int(info_str[cursor:cursor+2], 16)
    cursor += 2

    # Initialize tempAlarm as a list in the result dictionary
    result['tempAlarm'] = []
    for _ in range(result['tempCount']):
        if remaining_length() < 2:
            return result
        result['tempAlarm'].append(int(info_str[cursor:cursor+2], 16))
        cursor += 2

    # Add other attributes to the result dictionary
    for attribute in ['currentAlarm', 'voltageAlarm', 'customAlarms', 'alarmEvent0', 'alarmEvent1', 'alarmEvent2', 'alarmEvent3', 'alarmEvent4', 'alarmEvent5', 'onOffState', 'equilibriumState0', 'equilibriumState1', 'systemState', 'disconnectionState0', 'disconnectionState1', 'alarmEvent6', 'alarmEvent7']:
        if remaining_length() < 2:
            return result
        result[attribute] = int(info_str[cursor:cursor+2], 16)
        cursor += 2

    currentAlarm = interpret_alarm('currentAlarm', get_value(battery_address, result, 'currentAlarm'))
    sensors["bms_"+battery_address+"currentAlarm"] = {
        'state': currentAlarm,
        'name': f"{name_prefix} {battery_address} - Current Alarm",
        'unique_id': f"{name_prefix} {battery_address} - Current Alarm",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    voltageAlarm = interpret_alarm('voltageAlarm', get_value(battery_address, result, 'voltageAlarm'))
    sensors["bms_"+battery_address+"voltageAlarm"] = {
        'state': voltageAlarm,
        'name': f"{name_prefix} {battery_address} - Voltage Alarm",
        'unique_id': f"{name_prefix} {battery_address} - Voltage Alarm",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
#        customAlarms = interpret_alarm('customAlarms', get_value(battery_address, result, 'customAlarms'))
#        sensors["bms_"+battery_address+"customAlarms"] = {
#            'state': customAlarms,
#            'name': f"{name_prefix} {battery_address} - Custom Alarms",
#            'unique_id': f"{name_prefix} {battery_address} - Custom Alarms",
#            'unit': "",  # Assuming the unit is Celsius
#            'icon': "",  # Example icon, you can change it
#            'device_class': "",
#            'state_class': "",
#            'attributes': {},
#       }
    alarmEvent0 = interpret_alarm('alarmEvent0', get_value(battery_address, result, 'alarmEvent0'))
    sensors["bms_"+battery_address+"alarmEvent0"] = {
        'state': alarmEvent0,
        'name': f"{name_prefix} {battery_address} - Alarm Event 0",
        'unique_id': f"{name_prefix} {battery_address} - Alarm Event 0",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    alarmEvent1 = interpret_alarm('alarmEvent1', get_value(battery_address, result, 'alarmEvent1'))
    sensors["bms_"+battery_address+"alarmEvent1"] = {
        'state': alarmEvent1,
        'name': f"{name_prefix} {battery_address} - Alarm Event 1",
        'unique_id': f"{name_prefix} {battery_address} - Alarm Event 1",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    alarmEvent2 = interpret_alarm('alarmEvent2', get_value(battery_address, result, 'alarmEvent2'))
    sensors["bms_"+battery_address+"alarmEvent2"] = {
        'state': alarmEvent2,
        'name': f"{name_prefix} {battery_address} - Alarm Event 2",
        'unique_id': f"{name_prefix} {battery_address} - Alarm Event 2",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    alarmEvent3 = interpret_alarm('alarmEvent3', get_value(battery_address, result, 'alarmEvent3'))
    sensors["bms_"+battery_address+"alarmEvent3"] = {
        'state': alarmEvent3,
        'name': f"{name_prefix} {battery_address} - Alarm Event 3",
        'unique_id': f"{name_prefix} {battery_address} - Alarm Event 3",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    alarmEvent4 = interpret_alarm('alarmEvent4', get_value(battery_address, result, 'alarmEvent4'))
    sensors["bms_"+battery_address+"alarmEvent4"] = {
        'state': alarmEvent4,
        'name': f"{name_prefix} {battery_address} - Alarm Event 4",
        'unique_id': f"{name_prefix} {battery_address} - Alarm Event 4",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    alarmEvent5 = interpret_alarm('alarmEvent5', get_value(battery_address, result, 'alarmEvent5'))
    sensors["bms_"+battery_address+"alarmEvent5"] = {
        'state': alarmEvent5,
        'name': f"{name_prefix} {battery_address} - Alarm Event 5",
        'unique_id': f"{name_prefix} {battery_address} - Alarm Event 5",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    alarmEvent6 = interpret_alarm('alarmEvent6', get_value(battery_address, result, 'alarmEvent6'))
    sensors["bms_"+battery_address+"alarmEvent6"] = {
        'state': alarmEvent6,
        'name': f"{name_prefix} {battery_address} - Alarm Event 6",
        'unique_id': f"{name_prefix} {battery_address} - Alarm Event 6",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    alarmEvent7 = interpret_alarm('alarmEvent7', get_value(battery_address, result, 'alarmEvent7'))
    sensors["bms_"+battery_address+"alarmEvent7"] = {
        'state': alarmEvent7,
        'name': f"{name_prefix} {battery_address} - Alarm Event 7",
        'unique_id': f"{name_prefix} {battery_address} - Alarm Event 7",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    onOffState = interpret_alarm('onOffState', get_value(battery_address, result, 'onOffState'))
    sensors["bms_"+battery_address+"onOffState"] = {
        'state': onOffState,
        'name': f"{name_prefix} {battery_address} - On Off State",
        'unique_id': f"{name_prefix} {battery_address} - On Off State",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    equilibriumState0 = interpret_alarm('equilibriumState0', get_value(battery_address, result, 'equilibriumState0'))
    sensors["bms_"+battery_address+"equilibriumState0"] = {
        'state': equilibriumState0,
        'name': f"{name_prefix} {battery_address} - Equilibrium State 0",
        'unique_id': f"{name_prefix} {battery_address} - Equilibrium State 0",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    equilibriumState1 = interpret_alarm('equilibriumState1', get_value(battery_address, result, 'equilibriumState1'))
    sensors["bms_"+battery_address+"equilibriumState1"] = {
        'state': equilibriumState1,
        'name': f"{name_prefix} {battery_address} - Equilibrium State 1",
        'unique_id': f"{name_prefix} {battery_address} - Equilibrium State 1",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }

    for i in range(cellsCount):
        CELL_STATE_LOWEST = False
        CELL_STATE_HIGHEST = False
        cell_voltage_key = f"cell_{i+1}_voltage{battery_address}"  # Create a unique key for each cell
        if lowest_voltage_value == cellVoltage[i]:
            CELL_STATE_LOWEST = True
        if highest_voltage_value == cellVoltage[i]:
            CELL_STATE_HIGHEST = True
        if f"Cell 0{i+1}" in equilibriumState0 or f"Cell 0{i+1}" in equilibriumState1 or f"Cell {i+1}" in equilibriumState1:
            balancerActiveCell = True
        else:
            balancerActiveCell = False 
            
        balance_key = f"{battery_address}balancell{i+1}"  # Create a unique key for each cell
        binary_sensors[balance_key] = {
            'state': balancerActiveCell,
            'name': f"{name_prefix} {battery_address} - Balancer Active Cell {i+1}",
            'unique_id': f"{name_prefix} {battery_address} - Balancer Active Cell {i+1}",
            'device_class': "",
            'state_class': "",
            'icon': "mdi:battery",
            'attributes': {},
            'device_register': DeviceInfo(
                        identifiers={("bms_connector", entry.entry_id, battery_address)},
                    )
        }

        sensors[cell_voltage_key] = {
            'state': cellVoltage[i],
            'name': f"{name_prefix} {battery_address} - Cell Voltage {i+1}",
            'unique_id': f"{name_prefix} {battery_address} - Cell Voltage {i+1}",
            'unit': "mV",
            'icon': "mdi:battery",
            'device_class': "",
            'state_class': "",
            'attributes': {
                'CELL_STATE_LOWEST': CELL_STATE_LOWEST,
                'CELL_STATE_HIGHEST': CELL_STATE_HIGHEST,
                'CELL_STATE_BALANCING': balancerActiveCell
            },
            'device_register': DeviceInfo(
                        identifiers={("bms_connector", entry.entry_id, battery_address)},
                    )
        }


    systemState = interpret_alarm('systemState', get_value(battery_address, result, 'systemState'))
    sensors["bms_"+battery_address+"systemState"] = {
        'state': systemState,
        'name': f"{name_prefix} {battery_address} - System State",
        'unique_id': f"{name_prefix} {battery_address} - System State",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'availability': True,
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    disconnectionState0 = interpret_alarm('disconnectionState0', get_value(battery_address, result, 'disconnectionState0'))
    sensors["bms_"+battery_address+"disconnectionState0"] = {
        'state': disconnectionState0,
        'name': f"{name_prefix} {battery_address} - Disconnection State 0",
        'unique_id': f"{name_prefix} {battery_address} - Disconnection State 0",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    disconnectionState1 = interpret_alarm('disconnectionState1', get_value(battery_address, result, 'disconnectionState1'))
    sensors["bms_"+battery_address+"disconnectionState1"] = {
        'state': disconnectionState1,
        'name': f"{name_prefix} {battery_address} - Disconnection State 1",
        'unique_id': f"{name_prefix} {battery_address} - Disconnection State 1",
        'unit': None,
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }

    return sensors, binary_sensors
