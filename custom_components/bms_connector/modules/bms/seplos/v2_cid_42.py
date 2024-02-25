from homeassistant.helpers.entity import Entity, DeviceInfo

async def process_cid_42(CID_42_RESPONSE, battery_address, name_prefix, entry):
    new_sensors = {}
    sensors = {}
    data_coll = {}
    # PROCESS 42H CODES
    info_str = CID_42_RESPONSE

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
    data_coll['cur'] = current
    cursor += 4
    voltage = int(info_str[cursor:cursor+4], 16) / 100
    data_coll['v'] = voltage
    cursor += 4
    resCap = int(info_str[cursor:cursor+4], 16) / 100
    data_coll['remc'] = resCap
    cursor += 4
    customNumber = int(info_str[cursor:cursor+2], 16)
    cursor += 2
    capacity = int(info_str[cursor:cursor+4], 16) / 100
    cursor += 4
    soc = int(info_str[cursor:cursor+4], 16) / 10
    data_coll['soc'] = soc
    cursor += 4
    ratedCapacity = int(info_str[cursor:cursor+4], 16) / 100
    data_coll['ratec'] = ratedCapacity
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

    new_sensors =   {
                    'cellsCount'+battery_address: {
                        'state': cellsCount,
                        'name': f"{name_prefix} {battery_address} - Number of Cells",
                        'unique_id': f"{name_prefix} {battery_address} - Number of Cells",
                        'unit': "",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 
                    'resCap'+battery_address: {
                        'state': resCap,
                        'name': f"{name_prefix} {battery_address} - Residual Capacity",
                        'unique_id': f"{name_prefix} {battery_address} - Residual Capacity",
                        'unit': "Ah",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 
                    'capacity'+battery_address: {
                        'state': capacity,
                        'name': f"{name_prefix} {battery_address} - Capacity",
                        'unique_id': f"{name_prefix} {battery_address} - Capacity",
                        'unit': "Ah",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 
                    'soc'+battery_address: {
                        'state': soc,
                        'name': f"{name_prefix} {battery_address} - State of Charge",
                        'unique_id': f"{name_prefix} {battery_address} - State of Charge",
                        'unit': "%",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 
                    'ratedCapacity'+battery_address: {
                        'state': ratedCapacity,
                        'name': f"{name_prefix} {battery_address} - Rated Capacity",
                        'unique_id': f"{name_prefix} {battery_address} - Rated Capacity",
                        'unit': "Ah",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 
                    'cycles'+battery_address: {
                        'state': cycles,
                        'name': f"{name_prefix} {battery_address} - Cycles",
                        'unique_id': f"{name_prefix} {battery_address} - Cycles",
                        'unit': "",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 
                    'soh'+battery_address: {
                        'state': soh,
                        'name': f"{name_prefix} {battery_address} - State of Health",
                        'unique_id': f"{name_prefix} {battery_address} - State of Health",
                        'unit': "%",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    },  
                    'portVoltage'+battery_address: {
                        'state': portVoltage,
                        'name': f"{name_prefix} {battery_address} - Port Voltage",
                        'unique_id': f"{name_prefix} {battery_address} - Port Voltage",
                        'unit': "v",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 
                           
                    'current'+battery_address: {
                        'state': current,
                        'name': f"{name_prefix} {battery_address} - Current",
                        'unique_id': f"{name_prefix} {battery_address} - Current",
                        'unit': "A",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 

                    'voltage'+battery_address: {
                        'state': voltage,
                        'name': f"{name_prefix} {battery_address} - Voltage",
                        'unique_id': f"{name_prefix} {battery_address} - Voltage",
                        'unit': "v",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 

                    'battery_watts'+battery_address: {
                        'state': int(voltage * current),
                        'name': f"{name_prefix} {battery_address} - Battery Watts",
                        'unique_id': f"{name_prefix} {battery_address} - Battery Watts",
                        'unit': "w",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 

                    'full_charge_watts'+battery_address: {
                        'state': int((capacity - resCap) * nominal_voltage),
                        'name': f"{name_prefix} {battery_address} - Full Charge Watts",
                        'unique_id': f"{name_prefix} {battery_address} - Full Charge Watts",
                        'unit': "w",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 

                    'full_charge_amps'+battery_address: {
                        'state': int((capacity - resCap)),
                        'name': f"{name_prefix} {battery_address} - Full Charge Amps",
                        'unique_id': f"{name_prefix} {battery_address} - Full Charge Amps",
                        'unit': "Ah",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 

                    'remaining_watts'+battery_address: {
                        'state': int(resCap * nominal_voltage),
                        'name': f"{name_prefix} {battery_address} - Remaining Watts",
                        'unique_id': f"{name_prefix} {battery_address} - Remaining Watts",
                        'unit': "w",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 

                    'highest_cell_voltage'+battery_address: {
                        'state': highest_voltage_value,
                        'name': f"{name_prefix} {battery_address} - Highest Cell Voltage",
                        'unique_id': f"{name_prefix} {battery_address} - Highest Cell Voltage",
                        'unit': "mV",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 

                    'highest_cell_number'+battery_address: {
                        'state': highest_voltage_cell_number,
                        'name': f"{name_prefix} {battery_address} - Cell Number of Highest Voltage",
                        'unique_id': f"{name_prefix} {battery_address} - Cell Number of Highest Voltage",
                        'unit': None,
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 

                    'lowest_cell_voltage'+battery_address: {
                        'state': lowest_voltage_value,
                        'name': f"{name_prefix} {battery_address} - Lowest Cell Voltage",
                        'unique_id': f"{name_prefix} {battery_address} - Lowest Cell Voltage",
                        'unit': "mV",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 

                    'lowest_cell_number'+battery_address: {
                        'state': lowest_voltage_cell_number,
                        'name': f"{name_prefix} {battery_address} - Cell Number of Lowest Voltage",
                        'unique_id': f"{name_prefix} {battery_address} - Cell Number of Lowest Voltage",
                        'unit': None,
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 

                    'cell_difference'+battery_address: {
                        'state': cell_difference,
                        'name': f"{name_prefix} {battery_address} - Cell Voltage Difference",
                        'unique_id': f"{name_prefix} {battery_address} - Cell Voltage Difference",
                        'unit': "mV",
                        'icon': "",
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 
                    'capacity_watts'+battery_address: {
                        'state': nominal_voltage * capacity,
                        'name': f"{name_prefix} {battery_address} - Capacity Watts",
                        'unique_id': f"{name_prefix} {battery_address} - Capacity Watts",
                        'unit': "w",
                        'icon': "",  # Example icon, you can change it
                        'device_class': "",
                        'state_class': "",
                        'attributes': {},
                        'device_register': DeviceInfo(
                                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                                )
                    }, 

               }   

    for i, temp in enumerate(temperatures):
        if i < tempCount - 2:
            # For the first (tempCount - 2) temperatures, label them as Cell 1 Temp, Cell 2 Temp, etc.
            sensor_key = f"cell temperature {i+1}{battery_address}"
            sensor_name = f"{name_prefix} {battery_address} - Cell Temperature {i+1}"
        elif i == tempCount - 2:
            # The second last temperature is Power Temp
            sensor_key = f"power_temperature{battery_address}"
            sensor_name = f"{name_prefix} {battery_address} - Power Temperature"
        else:
            # The last temperature is Environment Temp
            sensor_key = f"environment_temperature{battery_address}"
            sensor_name = f"{name_prefix} {battery_address} - Environment Temperature"

        sensors[sensor_key] = {
            'state': temp,
            'name': sensor_name,
            'unique_id': f"{name_prefix} {battery_address} - {sensor_key}",
            'unit': "°C",  # Assuming the unit is Celsius
            'icon': "mdi:thermometer",  # Example icon, you can change it
            'device_class': "",
            'state_class': "",
            'attributes': {},
            'device_register': DeviceInfo(
                        identifiers={("bms_connector", entry.entry_id, battery_address)},
                    )
        }

    new_sensors.update(sensors)


    return new_sensors, lowest_voltage_value, highest_voltage_value, cellsCount, cellVoltage 
