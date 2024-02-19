from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.components.binary_sensor import BinarySensorEntity
import serial
import time
import aiohttp
import json
import asyncio
import logging
from datetime import datetime, timezone, timedelta
from homeassistant.helpers import device_registry as dr

from ....const import (
    NAME,
    DOMAIN,
    VERSION,
    ATTRIBUTION,
)
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
_LOGGER = logging.getLogger(__name__)

async def SeplosV2BMS(hass, entry):
    async def send_serial_commands(commands, port, baudrate=19200, timeout=2):
        responses = []
        _LOGGER.debug(commands)

        with serial.Serial(port, baudrate=baudrate, timeout=timeout) as ser:
            for command in commands:
                _LOGGER.debug(command)
                ser.write(command.encode())
                await asyncio.sleep(0.3)
                responses.append(ser.read(ser.in_waiting).decode().replace('\r', '').replace('\n', ''))
        _LOGGER.debug(responses)

        return responses

    ha_update_time = entry.data.get("sensor_update_frequency")
    usb_port = entry.data.get("usb_port")
    battery_address = entry.data.get("battery_address")
    name_prefix = entry.data.get("name_prefix")
    sensors = {}
    binary_sensors = {}
    async def async_update_data():

        V2_COMMAND_ARRAY = {
            "0x00": ["~20004642E00200FD37\r", "~20004644E00200FD35\r", "~20004647E00200FD32\r", "~20004651E00200FD37\r"],
            "0x01": ["~20004642E00215FD31\r", "~20004644E00200FD35\r", "~20004647E00200FD32\r", "~20004651E00200FD37\r"],
            "0x02": ["~20004642E00200FD37\r", "~20004644E00200FD35\r", "~20004647E00200FD32\r", "~20004651E00200FD37\r"],
            "0x03": ["~20004642E00200FD37\r", "~20004644E00200FD35\r", "~20004647E00200FD32\r", "~20004651E00200FD37\r"],
        }

        commands = V2_COMMAND_ARRAY[battery_address]
        data = await send_serial_commands(commands, usb_port, baudrate=19200, timeout=2)

        # PROCESS 42H CODES
        info_str = data[0]
        if info_str.startswith("~"):
            info_str = info_str[1:]

        msg_wo_chk_sum = info_str[:-4]
        info_str = msg_wo_chk_sum[12:]
        cursor = 4

        cellsCount = int(info_str[cursor:cursor+2], 16)
        cursor += 2
        cellVoltage = []
        temperatures = []
        for _ in range(cellsCount):
            cellVoltage.append(int(info_str[cursor:cursor+4], 16))
            cursor += 4

        tempCount = int(info_str[cursor:cursor+2], 16)
        cursor += 2
        for _ in range(tempCount):
            temperature = (int(info_str[cursor:cursor+4], 16) - 2731) / 10
            temperatures.append(temperature)
            cursor += 4


        current = int(info_str[cursor:cursor+4], 16)
        if current > 32767:
            current -= 65536 
        current /= 100 
        cursor += 4
        voltage = int(info_str[cursor:cursor+4], 16) / 100
        cursor += 4
        resCap = int(info_str[cursor:cursor+4], 16) / 100
        cursor += 4
        customNumber = int(info_str[cursor:cursor+2], 16)
        cursor += 2
        capacity = int(info_str[cursor:cursor+4], 16) / 100
        cursor += 4
        soc = int(info_str[cursor:cursor+4], 16) / 10
        cursor += 4
        ratedCapacity = int(info_str[cursor:cursor+4], 16) / 100
        cursor += 4
        cycles = int(info_str[cursor:cursor+4], 16)
        cursor += 4
        soh = int(info_str[cursor:cursor+4], 16) / 10
        cursor += 4
        portVoltage = int(info_str[cursor:cursor+4], 16) / 100

        # Assuming cellVoltage is a list containing the voltages of each cell
        highest_voltage = max(enumerate(cellVoltage), key=lambda x: x[1])
        lowest_voltage = min(enumerate(cellVoltage), key=lambda x: x[1])

        # highest_voltage and lowest_voltage are tuples in the form (index, value)
        highest_voltage_cell_number = highest_voltage[0] + 1  # Adding 1 because cell numbering usually starts from 1
        highest_voltage_value = highest_voltage[1]

        lowest_voltage_cell_number = lowest_voltage[0] + 1  # Adding 1 for the same reason
        lowest_voltage_value = lowest_voltage[1]
        cell_difference =  highest_voltage[1] - lowest_voltage[1]
        nominal_voltage = cellsCount * 3.3125

        sensors = {
                    'cellsCount': {
                        'state': cellsCount,
                        'name': f"{name_prefix}Number of Cells",
                        'unique_id': f"{name_prefix}Number of Cells",
                        'unit': "",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    }, 
                    'resCap': {
                        'state': resCap,
                        'name': f"{name_prefix}Residual Capacity",
                        'unique_id': f"{name_prefix}Residual Capacity",
                        'unit': "Ah",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    }, 
                    'capacity': {
                        'state': capacity,
                        'name': f"{name_prefix}Capacity",
                        'unique_id': f"{name_prefix}Capacity",
                        'unit': "Ah",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    }, 
                    'soc': {
                        'state': soc,
                        'name': f"{name_prefix}State of Charge",
                        'unique_id': f"{name_prefix}State of Charge",
                        'unit': "%",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    }, 
                    'ratedCapacity': {
                        'state': ratedCapacity,
                        'name': f"{name_prefix}Rated Capacity",
                        'unique_id': f"{name_prefix}Rated Capacity",
                        'unit': "Ah",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    }, 
                    'cycles': {
                        'state': cycles,
                        'name': f"{name_prefix}Cycles",
                        'unique_id': f"{name_prefix}Cycles",
                        'unit': "",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    }, 
                    'soh': {
                        'state': soh,
                        'name': f"{name_prefix}State of Health",
                        'unique_id': f"{name_prefix}State of Health",
                        'unit': "%",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    },  
                    'portVoltage': {
                        'state': portVoltage,
                        'name': f"{name_prefix}Port Voltage",
                        'unique_id': f"{name_prefix}Port Voltage",
                        'unit': "v",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    },                            
                    'current': {
                        'state': current,
                        'name': f"{name_prefix}Current",
                        'unique_id': f"{name_prefix}Current",
                        'unit': "A",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    },  
                    'voltage': {
                        'state': voltage,
                        'name': f"{name_prefix}Voltage",
                        'unique_id': f"{name_prefix}Voltage",
                        'unit': "v",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    },  
                    'battery_watts': {
                        'state': int(voltage * current),
                        'name': f"{name_prefix}Battery Watts",
                        'unique_id': f"{name_prefix}Battery Watts",
                        'unit': "w",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    }, 
                    'full_charge_watts': {
                        'state': int((capacity - resCap) * nominal_voltage),
                        'name': f"{name_prefix}Full Charge Watts",
                        'unique_id': f"{name_prefix}Full Charge Watts",
                        'unit': "w",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    }, 
                    'full_charge_amps': {
                        'state': int((capacity - resCap)),
                        'name': f"{name_prefix}Full Charge Amps",
                        'unique_id': f"{name_prefix}Full Charge Amps",
                        'unit': "Ah",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    },
                    'remaining_watts': {
                        'state': int(resCap * nominal_voltage),
                        'name': f"{name_prefix}Remaining Watts",
                        'unique_id': f"{name_prefix}Remaining Watts",
                        'unit': "w",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    }, 
                    'highest_cell_voltage': {
                        'state': highest_voltage_value,
                        'name': f"{name_prefix}Highest Cell Voltage",
                        'unique_id': f"{name_prefix}Highest Cell Voltage",
                        'unit': "mV",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    }, 
                    'highest_cell_number': {
                        'state': highest_voltage_cell_number,
                        'name': f"{name_prefix}Cell Number of Highest Voltage",
                        'unique_id': f"{name_prefix}Cell Number of Highest Voltage",
                        'unit': None,
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    }, 
                    'lowest_cell_voltage': {
                        'state': lowest_voltage_value,
                        'name': f"{name_prefix}Lowest Cell Voltage",
                        'unique_id': f"{name_prefix}Lowest Cell Voltage",
                        'unit': "mV",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    }, 
                    'lowest_cell_number': {
                        'state': lowest_voltage_cell_number,
                        'name': f"{name_prefix}Cell Number of Lowest Voltage",
                        'unique_id': f"{name_prefix}Cell Number of Lowest Voltage",
                        'unit': None,
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    }, 
                    'cell_difference': {
                        'state': cell_difference,
                        'name': f"{name_prefix}Cell Voltage Difference",
                        'unique_id': f"{name_prefix}Cell Voltage Difference",
                        'unit': "mV",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                    }, 


            }
        sensors["capacity_watts"] = {
            'state': nominal_voltage * capacity,
            'name': f"{name_prefix}Capacity Watts",
            'unique_id': f"{name_prefix}Capacity Watts",
            'unit': "w",
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }


        for i, temp in enumerate(temperatures):
            if i < tempCount - 2:
                # For the first (tempCount - 2) temperatures, label them as Cell 1 Temp, Cell 2 Temp, etc.
                sensor_key = f"cell temperature {i+1}"
                sensor_name = f"{name_prefix}Cell Temperature {i+1}"
            elif i == tempCount - 2:
                # The second last temperature is Power Temp
                sensor_key = "power_temperature"
                sensor_name = f"{name_prefix}Power Temperature"
            else:
                # The last temperature is Environment Temp
                sensor_key = "environment_temperature"
                sensor_name = f"{name_prefix}Environment Temperature"

            sensors[sensor_key] = {
                'state': temp,
                'name': sensor_name,
                'unique_id': f"{name_prefix}{sensor_key}",
                'unit': "°C",  # Assuming the unit is Celsius
                'icon': "mdi:thermometer",  # Example icon, you can change it
                'device_class': "",
                'state_class': "",
                'attributes': {},
            }

        def get_value(data, attribute):
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


        info_str = data[1]
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

        currentAlarm = interpret_alarm('currentAlarm', get_value(result, 'currentAlarm'))
        sensors["currentAlarm"] = {
            'state': currentAlarm,
            'name': f"{name_prefix}Current Alarm",
            'unique_id': f"{name_prefix}Current Alarm",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        voltageAlarm = interpret_alarm('voltageAlarm', get_value(result, 'voltageAlarm'))
        sensors["voltageAlarm"] = {
            'state': voltageAlarm,
            'name': f"{name_prefix}Voltage Alarm",
            'unique_id': f"{name_prefix}Voltage Alarm",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
#        customAlarms = interpret_alarm('customAlarms', get_value(result, 'customAlarms'))
#        sensors["customAlarms"] = {
#            'state': customAlarms,
#            'name': f"{name_prefix}Custom Alarms",
#            'unique_id': f"{name_prefix}Custom Alarms",
#            'unit': "",  # Assuming the unit is Celsius
#            'icon': "",  # Example icon, you can change it
#            'device_class': "",
#            'state_class': "",
#            'attributes': {},
#       }
        alarmEvent0 = interpret_alarm('alarmEvent0', get_value(result, 'alarmEvent0'))
        sensors["alarmEvent0"] = {
            'state': alarmEvent0,
            'name': f"{name_prefix}Alarm Event 0",
            'unique_id': f"{name_prefix}Alarm Event 0",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        alarmEvent1 = interpret_alarm('alarmEvent1', get_value(result, 'alarmEvent1'))
        sensors["alarmEvent1"] = {
            'state': alarmEvent1,
            'name': f"{name_prefix}Alarm Event 1",
            'unique_id': f"{name_prefix}Alarm Event 1",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        alarmEvent2 = interpret_alarm('alarmEvent2', get_value(result, 'alarmEvent2'))
        sensors["alarmEvent2"] = {
            'state': alarmEvent2,
            'name': f"{name_prefix}Alarm Event 2",
            'unique_id': f"{name_prefix}Alarm Event 2",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        alarmEvent3 = interpret_alarm('alarmEvent3', get_value(result, 'alarmEvent3'))
        sensors["alarmEvent3"] = {
            'state': alarmEvent3,
            'name': f"{name_prefix}Alarm Event 3",
            'unique_id': f"{name_prefix}Alarm Event 3",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        alarmEvent4 = interpret_alarm('alarmEvent4', get_value(result, 'alarmEvent4'))
        sensors["alarmEvent4"] = {
            'state': alarmEvent4,
            'name': f"{name_prefix}Alarm Event 4",
            'unique_id': f"{name_prefix}Alarm Event 4",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        alarmEvent5 = interpret_alarm('alarmEvent5', get_value(result, 'alarmEvent5'))
        sensors["alarmEvent5"] = {
            'state': alarmEvent5,
            'name': f"{name_prefix}Alarm Event 5",
            'unique_id': f"{name_prefix}Alarm Event 5",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        alarmEvent6 = interpret_alarm('alarmEvent6', get_value(result, 'alarmEvent6'))
        sensors["alarmEvent6"] = {
            'state': alarmEvent6,
            'name': f"{name_prefix}Alarm Event 6",
            'unique_id': f"{name_prefix}Alarm Event 6",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        alarmEvent7 = interpret_alarm('alarmEvent7', get_value(result, 'alarmEvent7'))
        sensors["alarmEvent7"] = {
            'state': alarmEvent7,
            'name': f"{name_prefix}Alarm Event 7",
            'unique_id': f"{name_prefix}Alarm Event 7",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        onOffState = interpret_alarm('onOffState', get_value(result, 'onOffState'))
        sensors["onOffState"] = {
            'state': onOffState,
            'name': f"{name_prefix}On Off State",
            'unique_id': f"{name_prefix}On Off State",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        equilibriumState0 = interpret_alarm('equilibriumState0', get_value(result, 'equilibriumState0'))
        sensors["equilibriumState0"] = {
            'state': equilibriumState0,
            'name': f"{name_prefix}Equilibrium State 0",
            'unique_id': f"{name_prefix}Equilibrium State 0",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        equilibriumState1 = interpret_alarm('equilibriumState1', get_value(result, 'equilibriumState1'))
        sensors["equilibriumState1"] = {
            'state': equilibriumState1,
            'name': f"{name_prefix}Equilibrium State 1",
            'unique_id': f"{name_prefix}Equilibrium State 1",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }

        for i in range(cellsCount):
            CELL_STATE_LOWEST = False
            CELL_STATE_HIGHEST = False
            cell_voltage_key = f"cell_{i+1}_voltage"  # Create a unique key for each cell
            if lowest_voltage_value == cellVoltage[i]:
                CELL_STATE_LOWEST = True
            if highest_voltage_value == cellVoltage[i]:
                CELL_STATE_HIGHEST = True
            if f"Cell 0{i+1}" in equilibriumState0 or f"Cell 0{i+1}" in equilibriumState1 or f"Cell {i+1}" in equilibriumState1:
                balancerActiveCell = True
            else:
                balancerActiveCell = False 
            balance_key = f"balancerActiveCell{i+1}"  # Create a unique key for each cell
            binary_sensors[balance_key] = {
                'state': balancerActiveCell,
                'name': f"{name_prefix}Balancer Active Cell {i+1}",
                'unique_id': f"{name_prefix}Balancer Active Cell {i+1}",
                'device_class': "",
                'state_class': "",
                'icon': "mdi:battery",
                'attributes': {},
            }
            sensors[cell_voltage_key] = {
                'state': cellVoltage[i],
                'name': f"{name_prefix}Cell Voltage {i+1}",
                'unique_id': f"{name_prefix}Cell Voltage {i+1}",
                'unit': "mV",
                'icon': "mdi:battery",
                'device_class': "",
                'state_class': "",
                'attributes': {
                    'CELL_STATE_LOWEST': CELL_STATE_LOWEST,
                    'CELL_STATE_HIGHEST': CELL_STATE_HIGHEST,
                    'CELL_STATE_BALANCING': balancerActiveCell
                },
            }


        systemState = interpret_alarm('systemState', get_value(result, 'systemState'))
        sensors["systemState"] = {
            'state': systemState,
            'name': f"{name_prefix}System State",
            'unique_id': f"{name_prefix}System State",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        disconnectionState0 = interpret_alarm('disconnectionState0', get_value(result, 'disconnectionState0'))
        sensors["disconnectionState0"] = {
            'state': disconnectionState0,
            'name': f"{name_prefix}Disconnection State 0",
            'unique_id': f"{name_prefix}Disconnection State 0",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        disconnectionState1 = interpret_alarm('disconnectionState1', get_value(result, 'disconnectionState1'))
        sensors["disconnectionState1"] = {
            'state': disconnectionState1,
            'name': f"{name_prefix}Disconnection State 1",
            'unique_id': f"{name_prefix}Disconnection State 1",
            'unit': None,
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }

        # PROCESS 42H CODES
        info_str = data[3]
        if info_str.startswith("~"):
            info_str = info_str[1:]

        msg_wo_chk_sum = info_str[:-4]
        hex_string = msg_wo_chk_sum[12:]
        cursor = 4

        hex_string = bytes.fromhex(hex_string)
        if len(hex_string) < 10:
            return None
        device_name_bytes = hex_string[0:10]
        software_version_bytes = hex_string[10:12]
        manufacturer_name_bytes = hex_string[12:24]

        # Convert bytes to ASCII strings
        device_name = device_name_bytes.decode('ascii')
        
        # Interpret the software version correctly
        software_version = int.from_bytes(software_version_bytes, byteorder='big') / 1000 * 4  # Really unsure if this is correct ... my version is 16.4 so * 4 made 4.1 16.4
        software_version = "{:.1f}".format(software_version)

        manufacturer_name = manufacturer_name_bytes.decode('ascii')

        sensors["device_name"] = {
            'state': device_name,
            'name': f"{name_prefix}Device Name",
            'unique_id': f"{name_prefix}Device Name",
            'unit': None,  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["software_version"] = {
            'state': software_version,
            'name': f"{name_prefix}Software Version",
            'unique_id': f"{name_prefix}Software Version",
            'unit': None,  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["manufacturer_name"] = {
            'state': manufacturer_name,
            'name': f"{name_prefix}Inverter Manufacturer Name",
            'unique_id': f"{name_prefix}Inverter Manufacturer Name",
            'unit': None,  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }

        info_str = data[2]
        if info_str.startswith("~"):
            info_str = info_str[1:]

        msg_wo_chk_sum = info_str[:-4]
        hex_string = msg_wo_chk_sum[12:]
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

        sensors["monomer_high_voltage_alarm"] = {
            'state': int.from_bytes(datai_bytes[0:2], byteorder='big') / 1000.0,
            'name': f"{name_prefix}Monomer High Voltage Alarm",
            'unique_id': f"{name_prefix}Monomer High Voltage Alarm",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["monomer_high_pressure_recovery"] = {
            'state': int.from_bytes(datai_bytes[2:4], byteorder='big') / 1000.0,
            'name': f"{name_prefix}Monomer High Pressure Recovery",
            'unique_id': f"{name_prefix}Monomer High Pressure Recovery",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# monomer_low_pressure_alarm = datai_values[2]
        sensors["monomer_low_pressure_alarm"] = {
            'state': int.from_bytes(datai_bytes[4:6], byteorder='big') / 1000.0,
            'name': f"{name_prefix}Monomer Low Pressure Alarm",
            'unique_id': f"{name_prefix}Monomer High Pressure Alarm",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# monomer_low_pressure_recovery = datai_values[3]
        sensors["monomer_low_pressure_recovery"] = {
            'state': int.from_bytes(datai_bytes[6:8], byteorder='big') / 1000.0,
            'name': f"{name_prefix}Monomer Low Pressure Recovery",
            'unique_id': f"{name_prefix}Monomer Low Pressure Recovery",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# monomer_overvoltage_protection = datai_values[4]
        sensors["monomer_overvoltage_protection"] = {
            'state': int.from_bytes(datai_bytes[8:10], byteorder='big') / 1000.0,
            'name': f"{name_prefix}Monomer Overvoltage Protection",
            'unique_id': f"{name_prefix}Monomer Overvoltage Protection",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# monomer_overvoltage_recovery = datai_values[5]
        sensors["monomer_overvoltage_recovery"] = {
            'state': int.from_bytes(datai_bytes[10:12], byteorder='big') / 1000.0,
            'name': f"{name_prefix}Monomer Overvoltage Recovery",
            'unique_id': f"{name_prefix}Monomer Overvoltage Recovery",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# monomer_undervoltage_protection = datai_values[6]
        sensors["monomer_undervoltage_protection"] = {
            'state': int.from_bytes(datai_bytes[12:14], byteorder='big') / 1000.0,
            'name': f"{name_prefix}Monomer Undervoltage Protection",
            'unique_id': f"{name_prefix}Monomer Undervoltage Protection",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# monomer_undervoltage_recovery = datai_values[7]
        sensors["monomer_undervoltage_recovery"] = {
            'state': int.from_bytes(datai_bytes[14:16], byteorder='big') / 1000.0,
            'name': f"{name_prefix}Monomer Undervoltage Recovery",
            'unique_id': f"{name_prefix}Monomer Undervoltage Recovery",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# equalization_opening_voltage = datai_values[8]
        sensors["equalization_opening_voltage"] = {
            'state': int.from_bytes(datai_bytes[16:18], byteorder='big') / 1000.0,
            'name': f"{name_prefix}Equalization Opening Voltage",
            'unique_id': f"{name_prefix}Equalization Opening Voltage",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# battery_low_voltage_forbidden_charging = datai_values[9]
        sensors["battery_low_voltage_forbidden_charging"] = {
            'state': int.from_bytes(datai_bytes[18:20], byteorder='big') / 1000.0,
            'name': f"{name_prefix}Battery Low Voltage Forbidden Charging",
            'unique_id': f"{name_prefix}Battery Low Voltage Forbidden Charging",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# total_pressure_high_pressure_alarm = datai_values[10]
        sensors["total_pressure_high_pressure_alarm"] = {
            'state': int.from_bytes(datai_bytes[20:22], byteorder='big') / 100.0,
            'name': f"{name_prefix}Total Pressure High Pressure Alarm",
            'unique_id': f"{name_prefix}Total Pressure High Pressure Alarm",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# total_pressure_high_pressure_recovery = datai_values[11]
        sensors["total_pressure_high_pressure_recovery"] = {
            'state': int.from_bytes(datai_bytes[22:24], byteorder='big') / 100.0,
            'name': f"{name_prefix}Total Pressure High Pressure Recovery",
            'unique_id': f"{name_prefix}Total Pressure High Pressure Recovery",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# total_pressure_low_pressure_alarm = datai_values[12]
        sensors["total_pressure_low_pressure_alarm"] = {
            'state': int.from_bytes(datai_bytes[24:26], byteorder='big') / 100.0,
            'name': f"{name_prefix}Total Pressure Low Pressure Alarm",
            'unique_id': f"{name_prefix}Total Pressure Low Pressure Alarm",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# total_pressure_low_pressure_recovery = datai_values[13]
        sensors["total_pressure_low_pressure_recovery"] = {
            'state': int.from_bytes(datai_bytes[26:28], byteorder='big') / 100.0,
            'name': f"{name_prefix}Total Pressure Low Pressure Recovery",
            'unique_id': f"{name_prefix}Total Pressure Low Pressure Recovery",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# total_voltage_overvoltage_protection = datai_values[14]
        sensors["total_voltage_overvoltage_protection"] = {
            'state': int.from_bytes(datai_bytes[28:30], byteorder='big') / 100.0,
            'name': f"{name_prefix}Total Overvoltage Protection",
            'unique_id': f"{name_prefix}Total Overvoltage Protection",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# total_pressure_overpressure_recovery = datai_values[15]
        sensors["total_pressure_overpressure_recovery"] = {
            'state': int.from_bytes(datai_bytes[30:32], byteorder='big') / 100.0,
            'name': f"{name_prefix}Total Pressure Overpressure Recovery",
            'unique_id': f"{name_prefix}Total Pressure Overpressure Recovery",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# total_voltage_undervoltage_protection = datai_values[16]
        sensors["total_voltage_undervoltage_protection"] = {
            'state': int.from_bytes(datai_bytes[32:34], byteorder='big') / 100.0,
            'name': f"{name_prefix}Total Voltage Undervoltage Protection",
            'unique_id': f"{name_prefix}Total Voltage Undervoltage Protection",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# total_pressure_undervoltage_recovery = datai_values[17]
        sensors["total_pressure_undervoltage_recovery"] = {
            'state': int.from_bytes(datai_bytes[34:36], byteorder='big') / 100.0,
            'name': f"{name_prefix}Total Pressure Undervoltage Recovery",
            'unique_id': f"{name_prefix}Total Pressure Undervoltage Recovery",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# charging_overvoltage_protection = datai_values[18]
        sensors["charging_overvoltage_protection"] = {
            'state': int.from_bytes(datai_bytes[36:38], byteorder='big') / 100.0,
            'name': f"{name_prefix}Charging Overvoltage Protection",
            'unique_id': f"{name_prefix}Charging Overvoltage Protection",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# charging_overvoltage_recovery = datai_values[19]
        sensors["charging_overvoltage_recovery"] = {
            'state': int.from_bytes(datai_bytes[38:40], byteorder='big') / 100.0,
            'name': f"{name_prefix}Charging Overvoltage Recovery",
            'unique_id': f"{name_prefix}Charging Overvoltage Recovery",
            'unit': "v",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# charging_high_temperature_warning = datai_values[20]
        sensors["charging_high_temperature_warning"] = {
            'state': (int.from_bytes(datai_bytes[40:42], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Charging High Temperature Warning",
            'unique_id': f"{name_prefix}Charging High Temperature Warning",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# charging_high_temperature_recovery = datai_values[21]
        sensors["charging_high_temperature_recovery"] = {
            'state': (int.from_bytes(datai_bytes[42:44], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Charging High Temperature Recovery",
            'unique_id': f"{name_prefix}Charging High Temperature Recovery",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
# charging_low_temperature_warning = datai_values[22]
        sensors["charging_low_temperature_warning"] = {
            'state': (int.from_bytes(datai_bytes[44:46], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Charging Low Temperature Warning",
            'unique_id': f"{name_prefix}Charging Low Temperature Warning",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["charging_low_temperature_recovery"] = {
            'state': (int.from_bytes(datai_bytes[46:48], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Charging Low Temperature Recovery",
            'unique_id': f"{name_prefix}Charging Low Temperature Recovery",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["charging_over_temperature_protection"] = {
            'state': (int.from_bytes(datai_bytes[48:50], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Charging Over Temperature Protection",
            'unique_id': f"{name_prefix}Charging Over Temperature Protection",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["charging_over_temperature_recovery"] = {
            'state': (int.from_bytes(datai_bytes[50:52], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Charging Over Temperature Recovery",
            'unique_id': f"{name_prefix}Charging Over Temperature Recovery",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["charging_under_temperature_protection"] = {
            'state': (int.from_bytes(datai_bytes[52:54], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Charging Under Temperature Protection",
            'unique_id': f"{name_prefix}Charging Under Temperature Protection",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["charging_under_temperature_recovery"] = {
            'state': (int.from_bytes(datai_bytes[54:56], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Charging Under Temperature Recovery",
            'unique_id': f"{name_prefix}Charging Under Temperature Recovery",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["discharge_high_temperature_warning"] = {
            'state': (int.from_bytes(datai_bytes[56:58], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Discharge High Temperature Warning",
            'unique_id': f"{name_prefix}Discharge High Temperature Warning",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["discharge_high_temperature_recovery"] = {
            'state': (int.from_bytes(datai_bytes[58:60], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Discharge High Temperature Recovery",
            'unique_id': f"{name_prefix}Discharge High Temperature Recovery",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["discharge_low_temperature_warning"] = {
            'state': (int.from_bytes(datai_bytes[60:62], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Discharge Low Temperature Warning",
            'unique_id': f"{name_prefix}Discharge Low Temperature Warning",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["discharge_low_temperature_recovery"] = {
            'state': (int.from_bytes(datai_bytes[62:64], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Discharge Low Temperature Recovery",
            'unique_id': f"{name_prefix}Discharge Low Temperature Recovery",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["discharge_over_temperature_protection"] = {
            'state': (int.from_bytes(datai_bytes[64:66], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Discharge Over Temperature Protection",
            'unique_id': f"{name_prefix}Discharge Over Temperature Protection",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["discharge_over_temperature_recovery"] = {
            'state': (int.from_bytes(datai_bytes[66:68], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Discharge Over Temperature Recovery",
            'unique_id': f"{name_prefix}Discharge Over Temperature Recovery",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["discharge_under_temperature_protection"] = {
            'state': (int.from_bytes(datai_bytes[68:70], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Discharge Under Temperature Protection",
            'unique_id': f"{name_prefix}Discharge Under Temperature Protection",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["discharge_under_temperature_recovery"] = {
            'state': (int.from_bytes(datai_bytes[70:72], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Discharge Under Temperature Recovery",
            'unique_id': f"{name_prefix}Discharge Under Temperature Recovery",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["cell_low_temperature_heating"] = {
            'state': (int.from_bytes(datai_bytes[72:74], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Cell Low Temperature Heating",
            'unique_id': f"{name_prefix}Cell Low Temperature Heating",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["cell_heating_recovery"] = {
            'state': (int.from_bytes(datai_bytes[74:76], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Cell Heating Recovery",
            'unique_id': f"{name_prefix}Cell Heating Recovery",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["ambient_high_temperature_alarm"] = {
            'state': (int.from_bytes(datai_bytes[76:78], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Ambient High Temperature Alarm",
            'unique_id': f"{name_prefix}Ambient High Temperature Alarm",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["ambient_high_temperature_recovery"] = {
            'state': (int.from_bytes(datai_bytes[78:80], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Ambient High Temperature Recovery",
            'unique_id': f"{name_prefix}Ambient High Temperature Recovery",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["ambient_low_temperature_alarm"] = {
            'state': (int.from_bytes(datai_bytes[80:82], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Ambient Low Temperature Alarm",
            'unique_id': f"{name_prefix}Ambient Low Temperature Alarm",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["ambient_low_temperature_recovery"] = {
            'state': (int.from_bytes(datai_bytes[82:84], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Ambient Low Temperature Recovery",
            'unique_id': f"{name_prefix}Ambient Low Temperature Recovery",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["environment_over_temperature_protection"] = {
            'state': (int.from_bytes(datai_bytes[84:86], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Environment Over Temperature Protection",
            'unique_id': f"{name_prefix}Environment Over Temperature Protection",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["environment_over_temperature_recovery"] = {
            'state': (int.from_bytes(datai_bytes[86:88], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Environment Over Temperature Recovery",
            'unique_id': f"{name_prefix}Environment Over Temperature Recovery",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["environment_under_temperature_protection"] = {
            'state': (int.from_bytes(datai_bytes[88:90], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Environment Under Temperature Protection",
            'unique_id': f"{name_prefix}Environment Under Temperature Protection",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["environment_under_temperature_recovery"] = {
            'state': (int.from_bytes(datai_bytes[90:92], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Environment Under Temperature Recovery",
            'unique_id': f"{name_prefix}Environment Under Temperature Recovery",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["power_high_temperature_alarm"] = {
            'state': (int.from_bytes(datai_bytes[92:94], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Power High Temperature Alarm",
            'unique_id': f"{name_prefix}Power High Temperature Alarm",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["power_high_temperature_recovery"] = {
            'state': (int.from_bytes(datai_bytes[94:96], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Power High Temperature Recovery",
            'unique_id': f"{name_prefix}Power High Temperature Recovery",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["power_over_temperature_protection"] = {
            'state': (int.from_bytes(datai_bytes[96:98], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Power Over Temperature Protection",
            'unique_id': f"{name_prefix}Power Over Temperature Protection",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["power_over_temperature_recovery"] = {
            'state': (int.from_bytes(datai_bytes[98:100], byteorder='big')  - 2731) / 10.0 ,
            'name': f"{name_prefix}Power Over Temperature Recovery",
            'unique_id': f"{name_prefix}Power Over Temperature Recovery",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["charging_overcurrent_warning"] = {
            'state': int.from_bytes(datai_bytes[100:102], byteorder='big') / 100.0 ,
            'name': f"{name_prefix}Charging Overcurrent Warning",
            'unique_id': f"{name_prefix}Charging Overcurrent Warning",
            'unit': "A",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["charging_overcurrent_recovery"] = {
            'state': int.from_bytes(datai_bytes[102:104], byteorder='big') / 100.0 ,
            'name': f"{name_prefix}Charging Overcurrent Recovery",
            'unique_id': f"{name_prefix}Charging Overcurrent Recovery",
            'unit': "A",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        overcurrent = int.from_bytes(datai_bytes[104:106], byteorder='big')
        if overcurrent > 32767:
            overcurrent -= 65536 
        sensors["discharge_overcurrent_warning"] = {
            'state': overcurrent / 100.0 ,
            'name': f"{name_prefix}Discharge Overcurrent Warning",
            'unique_id': f"{name_prefix}Discharge Overcurrent Warning",
            'unit': "A",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        overcurrent = int.from_bytes(datai_bytes[106:108], byteorder='big')
        if overcurrent > 32767:
            overcurrent -= 65536 
        sensors["discharge_overcurrent_recovery"] = {
            'state': overcurrent / 100.0 ,
            'name': f"{name_prefix}Discharge Overcurrent Recovery",
            'unique_id': f"{name_prefix}Discharge Overcurrent Recovery",
            'unit': "A",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["charge_overcurrent_protection"] = {
            'state': int.from_bytes(datai_bytes[108:110], byteorder='big') / 100.0 ,
            'name': f"{name_prefix}Charge Overcurrent Protection",
            'unique_id': f"{name_prefix}Charge Overcurrent Protection",
            'unit': "A",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        overcurrent = int.from_bytes(datai_bytes[110:112], byteorder='big')
        if overcurrent > 32767:
            overcurrent -= 65536 
        sensors["discharge_overcurrent_protection"] = {
            'state': overcurrent / 100.0 ,
            'name': f"{name_prefix}Discharge Overcurrent Protection",
            'unique_id': f"{name_prefix}Discharge Overcurrent Protection",
            'unit': "A",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        overcurrent = int.from_bytes(datai_bytes[112:114], byteorder='big')
        if overcurrent > 32767:
            overcurrent -= 65536 
            # Transient overcurrent protection
        sensors["transient_overcurrent_protection"] = {
            'state': overcurrent / 100,
            'name': f"{name_prefix}Transient Overcurrent Protection",
            'unique_id': f"{name_prefix}Transient Overcurrent Protection",
            'unit': "A",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }

            # Output soft start delay
        sensors["output_soft_start_delay"] = {
            'state': int.from_bytes(datai_bytes[114:116], byteorder='big'),
            'name': f"{name_prefix}Output Soft Start Delay",
            'unique_id': f"{name_prefix}Output Soft Start Delay",
            'unit': "ms",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Battery rated capacity
        sensors["battery_rated_capacity"] = {
            'state': int.from_bytes(datai_bytes[116:118], byteorder='big') / 100.0 ,
            'name': f"{name_prefix}Battery Rated Capacity",
            'unique_id': f"{name_prefix}Battery Rated Capacity",
            'unit': "Ah",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }

        sensors["soc_ah"] = {
            'state': int.from_bytes(datai_bytes[118:120], byteorder='big') / 100.0 ,
            'name': f"{name_prefix}State of Charge - Ah",
            'unique_id': f"{name_prefix}State of Charge - Ah",
            'unit': "Ah",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Cell invalidation differential pressure
        sensors["cell_invalidation_differential_pressure"] = {
            'state': int.from_bytes(datai_bytes[121:122], byteorder='big') ,
            'name': f"{name_prefix}Cell Invalidation Differential Pressure",
            'unique_id': f"{name_prefix}Cell Invalidation Differential Pressure",
            'unit': "mV",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Cell invalidation recovery
        sensors["cell_invalidation_recovery"] = {
            'state': int.from_bytes(datai_bytes[120:121], byteorder='big'),
            'name': f"{name_prefix}Cell Invalidation Recovery",
            'unique_id': f"{name_prefix}Cell Invalidation Recovery",
            'unit': "mV",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Equalization opening pressure difference
        sensors["equalization_opening_pressure_difference"] = {
            'state': int.from_bytes(datai_bytes[122:123], byteorder='big') ,
            'name': f"{name_prefix}Equalization Opening Pressure Difference",
            'unique_id': f"{name_prefix}Equalization Opening Pressure Difference",
            'unit': "mV",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Equalization closing pressure difference
        sensors["equalization_closing_pressure_difference"] = {
            'state': int.from_bytes(datai_bytes[124:125], byteorder='big'),
            'name': f"{name_prefix}Equalization Closing Pressure Difference",
            'unique_id': f"{name_prefix}Equalization Closing Pressure Difference",
            'unit': "mV",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["static_equilibrium_time"] = {
            'state': int.from_bytes(datai_bytes[125:126], byteorder='big'),
            'name': f"{name_prefix}Static Equilibrium Time",
            'unique_id': f"{name_prefix}Static Equilibrium Time",
            'unit': "hours",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["battery_number_in_series"] = {
            'state': int.from_bytes(datai_bytes[126:127], byteorder='big'),
            'name': f"{name_prefix}Battery Number in Series",
            'unique_id': f"{name_prefix}Battery Number in Series",
            'unit': "cells",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["charge_overcurrent_delay"] = {
            'state': int.from_bytes(datai_bytes[127:128], byteorder='big'),
            'name': f"{name_prefix}Charge Overcurrent Delay",
            'unique_id': f"{name_prefix}Charge Overcurrent Delay",
            'unit': "s",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["discharge_overcurrent_delay"] = {
            'state': int.from_bytes(datai_bytes[128:129], byteorder='big'),
            'name': f"{name_prefix}Discharge Overcurrent Delay",
            'unique_id': f"{name_prefix}Discharge Overcurrent Delay",
            'unit': "s",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["transient_overcurrent_delay"] = {
            'state': int.from_bytes(datai_bytes[129:130], byteorder='big'),
            'name': f"{name_prefix}Transient Overcurrent Delay",
            'unique_id': f"{name_prefix}Transient Overcurrent Delay",
            'unit': "ms",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }

        sensors["overcurrent_delay_recovery"] = {
            'state': int.from_bytes(datai_bytes[130:131], byteorder='big'),
            'name': f"{name_prefix}Overcurrent Delay Recovery",
            'unique_id': f"{name_prefix}Overcurrent Delay Recovery",
            'unit': "s",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Overcurrent recovery times
        sensors["overcurrent_recovery_times"] = {
            'state': int.from_bytes(datai_bytes[131:132], byteorder='big'),
            'name': f"{name_prefix}Overcurrent Recovery Times",
            'unique_id': f"{name_prefix}Overcurrent Recovery Times",
            'unit': "times",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["charge_current_limit_delay"] = {
            'state': int.from_bytes(datai_bytes[132:133], byteorder='big'),
            'name': f"{name_prefix}Charge Current Limit Delay",
            'unique_id': f"{name_prefix}Charge Current Limit Delay",
            'unit': "minutes",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Charge activation delay
        sensors["charge_activation_delay"] = {
            'state': int.from_bytes(datai_bytes[133:134], byteorder='big'),
            'name': f"{name_prefix}Charge Activation Delay",
            'unique_id': f"{name_prefix}Charge Activation Delay",
            'unit': "minutes",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Charging activation interval
        sensors["charging_activation_interval"] = {
            'state': int.from_bytes(datai_bytes[134:135], byteorder='big'),
            'name': f"{name_prefix}Charging Activation Interval",
            'unique_id': f"{name_prefix}Charging Activation Interval",
            'unit': "hours",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Charge activation times
        sensors["charge_activation_times"] = {
            'state': int.from_bytes(datai_bytes[135:136], byteorder='big'),
            'name': f"{name_prefix}Charge Activation Times",
            'unique_id': f"{name_prefix}Charge Activation Times",
            'unit': "times",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Work record interval
        sensors["work_record_interval"] = {
            'state': int.from_bytes(datai_bytes[136:137], byteorder='big'),
            'name': f"{name_prefix}Work Record Interval",
            'unique_id': f"{name_prefix}Work Record Interval",
            'unit': "minutes",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Standby recording interval
        sensors["standby_recording_interval"] = {
            'state': int.from_bytes(datai_bytes[137:138], byteorder='big'),
            'name': f"{name_prefix}Standby Recording Interval",
            'unique_id': f"{name_prefix}Standby Recording Interval",
            'unit': "minutes",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Standby shutdown delay
        sensors["standby_shutdown_delay"] = {
            'state': int.from_bytes(datai_bytes[138:139], byteorder='big'),
            'name': f"{name_prefix}Standby Shutdown Delay",
            'unique_id': f"{name_prefix}Standby Shutdown Delay",
            'unit': "hours",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }


            # Remaining capacity alarm
        sensors["remaining_capacity_alarm"] = {
            'state': int.from_bytes(datai_bytes[139:140], byteorder='big'),
            'name': f"{name_prefix}Remaining Capacity Alarm",
            'unique_id': f"{name_prefix}Remaining Capacity Alarm",
            'unit': "%",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Remaining  protection
        sensors["remaining_capacity_protection"] = {
            'state': int.from_bytes(datai_bytes[140:141], byteorder='big'),
            'name': f"{name_prefix}Remaining Capacity Protection",
            'unique_id': f"{name_prefix}Remaining Capacity Protection",
            'unit': "%",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Interval charge capacity
        sensors["interval_charge_capacity"] = {
            'state': int.from_bytes(datai_bytes[141:142], byteorder='big'),
            'name': f"{name_prefix}Interval Charge Capacity",
            'unique_id': f"{name_prefix}Interval Charge Capacity",
            'unit': "%",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }

            # Cycle cumulative capacity
        sensors["cycle_cumulative_capacity"] = {
            'state': int.from_bytes(datai_bytes[142:143], byteorder='big'),
            'name': f"{name_prefix}Cycle Cumulative Capacity",
            'unique_id': f"{name_prefix}Cycle Cumulative Capacity",
            'unit': "%",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Connection fault impedance
        sensors["connection_fault_impedance"] = {
            'state': int.from_bytes(datai_bytes[143:144], byteorder='big') / 10.0,
            'name': f"{name_prefix}Connection Fault Impedance",
            'unique_id': f"{name_prefix}Connection Fault Impedance",
            'unit': "mΩ",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Compensation point 1 position
        sensors["compensation_point_1_position"] = {
            'state': int.from_bytes(datai_bytes[144:145], byteorder='big'),
            'name': f"{name_prefix}Compensation Point 1 Position",
            'unique_id': f"{name_prefix}Compensation Point 1 Position",
            'unit': "",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
            # Compensation point 1 impedance
        sensors["compensation_point_1_impedance"] = {
            'state': int.from_bytes(datai_bytes[145:146], byteorder='big') / 10.0,
            'name': f"{name_prefix}Compensation Point 1 Impedance",
            'unique_id': f"{name_prefix}Compensation Point 1 Impedance",
            'unit': "mΩ",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["compensation_point_2_position"] = {
            'state': int.from_bytes(datai_bytes[146:147], byteorder='big'),
            'name': f"{name_prefix}Compensation Point 2 Position",
            'unique_id': f"{name_prefix}Compensation Point 2 Position",
            'unit': "",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }
        sensors["compensation_point_2_impedance"] = {
            'state': int.from_bytes(datai_bytes[147:148], byteorder='big') / 10.0,
            'name': f"{name_prefix}Compensation Point 2 Impedance",
            'unique_id': f"{name_prefix}Compensation Point 2 Impedance",
            'unit': "mΩ",  # Assuming the unit is Celsius
            'icon': "",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
        }

        return {
                'binary_sensors': binary_sensors,
                'sensors': sensors
            }

    await async_update_data()

    hass.data[DOMAIN]["HOME_ENERGY_HUB_SENSOR_COORDINATOR"+entry.entry_id] = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="home_energy_hub_"+entry.entry_id,
        update_method=async_update_data,
        update_interval=timedelta(seconds=ha_update_time),  # Define how often to fetch data
    )
    await hass.data[DOMAIN]["HOME_ENERGY_HUB_SENSOR_COORDINATOR"+entry.entry_id].async_refresh() 