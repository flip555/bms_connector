from homeassistant.helpers.entity import Entity, DeviceInfo

async def process_cid_47(CID_47_RESPONSE, battery_address, name_prefix, entry):
    sensors = {}
    data_coll = {}

    info_str = CID_47_RESPONSE

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

    sensors["bms_"+battery_address+"monomer_high_voltage_alarm"] = {
        'state': int.from_bytes(datai_bytes[0:2], byteorder='big') / 1000.0,
        'name': f"{name_prefix} {battery_address} - Monomer High Voltage Alarm",
        'unique_id': f"{name_prefix} {battery_address} - Monomer High Voltage Alarm",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'availability': True,
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"monomer_high_pressure_recovery"] = {
        'state': int.from_bytes(datai_bytes[2:4], byteorder='big') / 1000.0,
        'name': f"{name_prefix} {battery_address} - Monomer High Pressure Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Monomer High Pressure Recovery",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# monomer_low_pressure_alarm = datai_values[2]
    sensors["bms_"+battery_address+"monomer_low_pressure_alarm"] = {
        'state': int.from_bytes(datai_bytes[4:6], byteorder='big') / 1000.0,
        'name': f"{name_prefix} {battery_address} - Monomer Low Pressure Alarm",
        'unique_id': f"{name_prefix} {battery_address} - Monomer High Pressure Alarm",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# monomer_low_pressure_recovery = datai_values[3]
    sensors["bms_"+battery_address+"monomer_low_pressure_recovery"] = {
        'state': int.from_bytes(datai_bytes[6:8], byteorder='big') / 1000.0,
        'name': f"{name_prefix} {battery_address} - Monomer Low Pressure Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Monomer Low Pressure Recovery",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# monomer_overvoltage_protection = datai_values[4]
    sensors["bms_"+battery_address+"monomer_overvoltage_protection"] = {
        'state': int.from_bytes(datai_bytes[8:10], byteorder='big') / 1000.0,
        'name': f"{name_prefix} {battery_address} - Monomer Overvoltage Protection",
        'unique_id': f"{name_prefix} {battery_address} - Monomer Overvoltage Protection",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# monomer_overvoltage_recovery = datai_values[5]
    sensors["bms_"+battery_address+"monomer_overvoltage_recovery"] = {
        'state': int.from_bytes(datai_bytes[10:12], byteorder='big') / 1000.0,
        'name': f"{name_prefix} {battery_address} - Monomer Overvoltage Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Monomer Overvoltage Recovery",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# monomer_undervoltage_protection = datai_values[6]
    sensors["bms_"+battery_address+"monomer_undervoltage_protection"] = {
        'state': int.from_bytes(datai_bytes[12:14], byteorder='big') / 1000.0,
        'name': f"{name_prefix} {battery_address} - Monomer Undervoltage Protection",
        'unique_id': f"{name_prefix} {battery_address} - Monomer Undervoltage Protection",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# monomer_undervoltage_recovery = datai_values[7]
    sensors["bms_"+battery_address+"monomer_undervoltage_recovery"] = {
        'state': int.from_bytes(datai_bytes[14:16], byteorder='big') / 1000.0,
        'name': f"{name_prefix} {battery_address} - Monomer Undervoltage Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Monomer Undervoltage Recovery",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# equalization_opening_voltage = datai_values[8]
    sensors["bms_"+battery_address+"equalization_opening_voltage"] = {
        'state': int.from_bytes(datai_bytes[16:18], byteorder='big') / 1000.0,
        'name': f"{name_prefix} {battery_address} - Equalization Opening Voltage",
        'unique_id': f"{name_prefix} {battery_address} - Equalization Opening Voltage",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# battery_low_voltage_forbidden_charging = datai_values[9]
    sensors["bms_"+battery_address+"battery_low_voltage_forbidden_charging"] = {
        'state': int.from_bytes(datai_bytes[18:20], byteorder='big') / 1000.0,
        'name': f"{name_prefix} {battery_address} - Battery Low Voltage Forbidden Charging",
        'unique_id': f"{name_prefix} {battery_address} - Battery Low Voltage Forbidden Charging",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# total_pressure_high_pressure_alarm = datai_values[10]
    sensors["bms_"+battery_address+"total_pressure_high_pressure_alarm"] = {
        'state': int.from_bytes(datai_bytes[20:22], byteorder='big') / 100.0,
        'name': f"{name_prefix} {battery_address} - Total Pressure High Pressure Alarm",
        'unique_id': f"{name_prefix} {battery_address} - Total Pressure High Pressure Alarm",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# total_pressure_high_pressure_recovery = datai_values[11]
    sensors["bms_"+battery_address+"total_pressure_high_pressure_recovery"] = {
        'state': int.from_bytes(datai_bytes[22:24], byteorder='big') / 100.0,
        'name': f"{name_prefix} {battery_address} - Total Pressure High Pressure Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Total Pressure High Pressure Recovery",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# total_pressure_low_pressure_alarm = datai_values[12]
    sensors["bms_"+battery_address+"total_pressure_low_pressure_alarm"] = {
        'state': int.from_bytes(datai_bytes[24:26], byteorder='big') / 100.0,
        'name': f"{name_prefix} {battery_address} - Total Pressure Low Pressure Alarm",
        'unique_id': f"{name_prefix} {battery_address} - Total Pressure Low Pressure Alarm",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# total_pressure_low_pressure_recovery = datai_values[13]
    sensors["bms_"+battery_address+"total_pressure_low_pressure_recovery"] = {
        'state': int.from_bytes(datai_bytes[26:28], byteorder='big') / 100.0,
        'name': f"{name_prefix} {battery_address} - Total Pressure Low Pressure Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Total Pressure Low Pressure Recovery",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# total_voltage_overvoltage_protection = datai_values[14]
    sensors["bms_"+battery_address+"total_voltage_overvoltage_protection"] = {
        'state': int.from_bytes(datai_bytes[28:30], byteorder='big') / 100.0,
        'name': f"{name_prefix} {battery_address} - Total Overvoltage Protection",
        'unique_id': f"{name_prefix} {battery_address} - Total Overvoltage Protection",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# total_pressure_overpressure_recovery = datai_values[15]
    sensors["bms_"+battery_address+"total_pressure_overpressure_recovery"] = {
        'state': int.from_bytes(datai_bytes[30:32], byteorder='big') / 100.0,
        'name': f"{name_prefix} {battery_address} - Total Pressure Overpressure Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Total Pressure Overpressure Recovery",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# total_voltage_undervoltage_protection = datai_values[16]
    sensors["bms_"+battery_address+"total_voltage_undervoltage_protection"] = {
        'state': int.from_bytes(datai_bytes[32:34], byteorder='big') / 100.0,
        'name': f"{name_prefix} {battery_address} - Total Voltage Undervoltage Protection",
        'unique_id': f"{name_prefix} {battery_address} - Total Voltage Undervoltage Protection",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# total_pressure_undervoltage_recovery = datai_values[17]
    sensors["bms_"+battery_address+"total_pressure_undervoltage_recovery"] = {
        'state': int.from_bytes(datai_bytes[34:36], byteorder='big') / 100.0,
        'name': f"{name_prefix} {battery_address} - Total Pressure Undervoltage Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Total Pressure Undervoltage Recovery",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# charging_overvoltage_protection = datai_values[18]
    sensors["bms_"+battery_address+"charging_overvoltage_protection"] = {
        'state': int.from_bytes(datai_bytes[36:38], byteorder='big') / 100.0,
        'name': f"{name_prefix} {battery_address} - Charging Overvoltage Protection",
        'unique_id': f"{name_prefix} {battery_address} - Charging Overvoltage Protection",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# charging_overvoltage_recovery = datai_values[19]
    sensors["bms_"+battery_address+"charging_overvoltage_recovery"] = {
        'state': int.from_bytes(datai_bytes[38:40], byteorder='big') / 100.0,
        'name': f"{name_prefix} {battery_address} - Charging Overvoltage Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Charging Overvoltage Recovery",
        'unit': "v",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
         'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# charging_high_temperature_warning = datai_values[20]
    sensors["bms_"+battery_address+"charging_high_temperature_warning"] = {
        'state': (int.from_bytes(datai_bytes[40:42], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Charging High Temperature Warning",
        'unique_id': f"{name_prefix} {battery_address} - Charging High Temperature Warning",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# charging_high_temperature_recovery = datai_values[21]
    sensors["bms_"+battery_address+"charging_high_temperature_recovery"] = {
        'state': (int.from_bytes(datai_bytes[42:44], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Charging High Temperature Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Charging High Temperature Recovery",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
# charging_low_temperature_warning = datai_values[22]
    sensors["bms_"+battery_address+"charging_low_temperature_warning"] = {
        'state': (int.from_bytes(datai_bytes[44:46], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Charging Low Temperature Warning",
        'unique_id': f"{name_prefix} {battery_address} - Charging Low Temperature Warning",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"charging_low_temperature_recovery"] = {
        'state': (int.from_bytes(datai_bytes[46:48], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Charging Low Temperature Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Charging Low Temperature Recovery",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"charging_over_temperature_protection"] = {
        'state': (int.from_bytes(datai_bytes[48:50], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Charging Over Temperature Protection",
        'unique_id': f"{name_prefix} {battery_address} - Charging Over Temperature Protection",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"charging_over_temperature_recovery"] = {
        'state': (int.from_bytes(datai_bytes[50:52], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Charging Over Temperature Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Charging Over Temperature Recovery",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"charging_under_temperature_protection"] = {
        'state': (int.from_bytes(datai_bytes[52:54], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Charging Under Temperature Protection",
        'unique_id': f"{name_prefix} {battery_address} - Charging Under Temperature Protection",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"charging_under_temperature_recovery"] = {
        'state': (int.from_bytes(datai_bytes[54:56], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Charging Under Temperature Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Charging Under Temperature Recovery",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"discharge_high_temperature_warning"] = {
        'state': (int.from_bytes(datai_bytes[56:58], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Discharge High Temperature Warning",
        'unique_id': f"{name_prefix} {battery_address} - Discharge High Temperature Warning",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"discharge_high_temperature_recovery"] = {
        'state': (int.from_bytes(datai_bytes[58:60], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Discharge High Temperature Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Discharge High Temperature Recovery",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"discharge_low_temperature_warning"] = {
        'state': (int.from_bytes(datai_bytes[60:62], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Discharge Low Temperature Warning",
        'unique_id': f"{name_prefix} {battery_address} - Discharge Low Temperature Warning",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"discharge_low_temperature_recovery"] = {
        'state': (int.from_bytes(datai_bytes[62:64], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Discharge Low Temperature Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Discharge Low Temperature Recovery",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"discharge_over_temperature_protection"] = {
        'state': (int.from_bytes(datai_bytes[64:66], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Discharge Over Temperature Protection",
        'unique_id': f"{name_prefix} {battery_address} - Discharge Over Temperature Protection",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"discharge_over_temperature_recovery"] = {
        'state': (int.from_bytes(datai_bytes[66:68], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Discharge Over Temperature Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Discharge Over Temperature Recovery",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"discharge_under_temperature_protection"] = {
        'state': (int.from_bytes(datai_bytes[68:70], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Discharge Under Temperature Protection",
        'unique_id': f"{name_prefix} {battery_address} - Discharge Under Temperature Protection",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"discharge_under_temperature_recovery"] = {
        'state': (int.from_bytes(datai_bytes[70:72], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Discharge Under Temperature Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Discharge Under Temperature Recovery",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"cell_low_temperature_heating"] = {
        'state': (int.from_bytes(datai_bytes[72:74], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Cell Low Temperature Heating",
        'unique_id': f"{name_prefix} {battery_address} - Cell Low Temperature Heating",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"cell_heating_recovery"] = {
        'state': (int.from_bytes(datai_bytes[74:76], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Cell Heating Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Cell Heating Recovery",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"ambient_high_temperature_alarm"] = {
        'state': (int.from_bytes(datai_bytes[76:78], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Ambient High Temperature Alarm",
        'unique_id': f"{name_prefix} {battery_address} - Ambient High Temperature Alarm",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"ambient_high_temperature_recovery"] = {
        'state': (int.from_bytes(datai_bytes[78:80], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Ambient High Temperature Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Ambient High Temperature Recovery",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"ambient_low_temperature_alarm"] = {
        'state': (int.from_bytes(datai_bytes[80:82], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Ambient Low Temperature Alarm",
        'unique_id': f"{name_prefix} {battery_address} - Ambient Low Temperature Alarm",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"ambient_low_temperature_recovery"] = {
        'state': (int.from_bytes(datai_bytes[82:84], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Ambient Low Temperature Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Ambient Low Temperature Recovery",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"environment_over_temperature_protection"] = {
        'state': (int.from_bytes(datai_bytes[84:86], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Environment Over Temperature Protection",
        'unique_id': f"{name_prefix} {battery_address} - Environment Over Temperature Protection",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"environment_over_temperature_recovery"] = {
        'state': (int.from_bytes(datai_bytes[86:88], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Environment Over Temperature Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Environment Over Temperature Recovery",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"environment_under_temperature_protection"] = {
        'state': (int.from_bytes(datai_bytes[88:90], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Environment Under Temperature Protection",
        'unique_id': f"{name_prefix} {battery_address} - Environment Under Temperature Protection",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"environment_under_temperature_recovery"] = {
        'state': (int.from_bytes(datai_bytes[90:92], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Environment Under Temperature Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Environment Under Temperature Recovery",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"power_high_temperature_alarm"] = {
        'state': (int.from_bytes(datai_bytes[92:94], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Power High Temperature Alarm",
        'unique_id': f"{name_prefix} {battery_address} - Power High Temperature Alarm",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"power_high_temperature_recovery"] = {
        'state': (int.from_bytes(datai_bytes[94:96], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Power High Temperature Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Power High Temperature Recovery",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"power_over_temperature_protection"] = {
        'state': (int.from_bytes(datai_bytes[96:98], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Power Over Temperature Protection",
        'unique_id': f"{name_prefix} {battery_address} - Power Over Temperature Protection",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"power_over_temperature_recovery"] = {
        'state': (int.from_bytes(datai_bytes[98:100], byteorder='big')  - 2731) / 10.0 ,
        'name': f"{name_prefix} {battery_address} - Power Over Temperature Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Power Over Temperature Recovery",
        'unit': "°C",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"charging_overcurrent_warning"] = {
        'state': int.from_bytes(datai_bytes[100:102], byteorder='big') / 100.0 ,
        'name': f"{name_prefix} {battery_address} - Charging Overcurrent Warning",
        'unique_id': f"{name_prefix} {battery_address} - Charging Overcurrent Warning",
        'unit': "A",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"charging_overcurrent_recovery"] = {
        'state': int.from_bytes(datai_bytes[102:104], byteorder='big') / 100.0 ,
        'name': f"{name_prefix} {battery_address} - Charging Overcurrent Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Charging Overcurrent Recovery",
        'unit': "A",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    overcurrent = int.from_bytes(datai_bytes[104:106], byteorder='big')
    if overcurrent > 32767:
        overcurrent -= 65536 
    sensors["bms_"+battery_address+"discharge_overcurrent_warning"] = {
        'state': overcurrent / 100.0 ,
        'name': f"{name_prefix} {battery_address} - Discharge Overcurrent Warning",
        'unique_id': f"{name_prefix} {battery_address} - Discharge Overcurrent Warning",
        'unit': "A",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    overcurrent = int.from_bytes(datai_bytes[106:108], byteorder='big')
    if overcurrent > 32767:
        overcurrent -= 65536 
    sensors["bms_"+battery_address+"discharge_overcurrent_recovery"] = {
        'state': overcurrent / 100.0 ,
        'name': f"{name_prefix} {battery_address} - Discharge Overcurrent Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Discharge Overcurrent Recovery",
        'unit': "A",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"charge_overcurrent_protection"] = {
        'state': int.from_bytes(datai_bytes[108:110], byteorder='big') / 100.0 ,
        'name': f"{name_prefix} {battery_address} - Charge Overcurrent Protection",
        'unique_id': f"{name_prefix} {battery_address} - Charge Overcurrent Protection",
        'unit': "A",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    overcurrent = int.from_bytes(datai_bytes[110:112], byteorder='big')
    if overcurrent > 32767:
        overcurrent -= 65536 
    sensors["bms_"+battery_address+"discharge_overcurrent_protection"] = {
        'state': overcurrent / 100.0 ,
        'name': f"{name_prefix} {battery_address} - Discharge Overcurrent Protection",
        'unique_id': f"{name_prefix} {battery_address} - Discharge Overcurrent Protection",
        'unit': "A",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    overcurrent = int.from_bytes(datai_bytes[112:114], byteorder='big')
    if overcurrent > 32767:
        overcurrent -= 65536 
        # Transient overcurrent protection
    sensors["bms_"+battery_address+"transient_overcurrent_protection"] = {
        'state': overcurrent / 100,
        'name': f"{name_prefix} {battery_address} - Transient Overcurrent Protection",
        'unique_id': f"{name_prefix} {battery_address} - Transient Overcurrent Protection",
        'unit': "A",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }

        # Output soft start delay
    sensors["bms_"+battery_address+"output_soft_start_delay"] = {
        'state': int.from_bytes(datai_bytes[114:116], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Output Soft Start Delay",
        'unique_id': f"{name_prefix} {battery_address} - Output Soft Start Delay",
        'unit': "ms",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Battery rated capacity
    sensors["bms_"+battery_address+"battery_rated_capacity"] = {
        'state': int.from_bytes(datai_bytes[116:118], byteorder='big') / 100.0 ,
        'name': f"{name_prefix} {battery_address} - Battery Rated Capacity",
        'unique_id': f"{name_prefix} {battery_address} - Battery Rated Capacity",
        'unit': "Ah",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }

    sensors["bms_"+battery_address+"soc_ah"] = {
        'state': int.from_bytes(datai_bytes[118:120], byteorder='big') / 100.0 ,
        'name': f"{name_prefix} {battery_address} - State of Charge - Ah",
        'unique_id': f"{name_prefix} {battery_address} - State of Charge - Ah",
        'unit': "Ah",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Cell invalidation differential pressure
    sensors["bms_"+battery_address+"cell_invalidation_differential_pressure"] = {
        'state': int.from_bytes(datai_bytes[121:122], byteorder='big') ,
        'name': f"{name_prefix} {battery_address} - Cell Invalidation Differential Pressure",
        'unique_id': f"{name_prefix} {battery_address} - Cell Invalidation Differential Pressure",
        'unit': "mV",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Cell invalidation recovery
    sensors["bms_"+battery_address+"cell_invalidation_recovery"] = {
        'state': int.from_bytes(datai_bytes[120:121], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Cell Invalidation Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Cell Invalidation Recovery",
        'unit': "mV",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Equalization opening pressure difference
    sensors["bms_"+battery_address+"equalization_opening_pressure_difference"] = {
        'state': int.from_bytes(datai_bytes[122:123], byteorder='big') ,
        'name': f"{name_prefix} {battery_address} - Equalization Opening Pressure Difference",
        'unique_id': f"{name_prefix} {battery_address} - Equalization Opening Pressure Difference",
        'unit': "mV",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Equalization closing pressure difference
    sensors["bms_"+battery_address+"equalization_closing_pressure_difference"] = {
        'state': int.from_bytes(datai_bytes[124:125], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Equalization Closing Pressure Difference",
        'unique_id': f"{name_prefix} {battery_address} - Equalization Closing Pressure Difference",
        'unit': "mV",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"static_equilibrium_time"] = {
        'state': int.from_bytes(datai_bytes[125:126], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Static Equilibrium Time",
        'unique_id': f"{name_prefix} {battery_address} - Static Equilibrium Time",
        'unit': "hours",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"battery_number_in_series"] = {
        'state': int.from_bytes(datai_bytes[126:127], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Battery Number in Series",
        'unique_id': f"{name_prefix} {battery_address} - Battery Number in Series",
        'unit': "cells",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"charge_overcurrent_delay"] = {
        'state': int.from_bytes(datai_bytes[127:128], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Charge Overcurrent Delay",
        'unique_id': f"{name_prefix} {battery_address} - Charge Overcurrent Delay",
        'unit': "s",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"discharge_overcurrent_delay"] = {
        'state': int.from_bytes(datai_bytes[128:129], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Discharge Overcurrent Delay",
        'unique_id': f"{name_prefix} {battery_address} - Discharge Overcurrent Delay",
        'unit': "s",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"transient_overcurrent_delay"] = {
        'state': int.from_bytes(datai_bytes[129:130], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Transient Overcurrent Delay",
        'unique_id': f"{name_prefix} {battery_address} - Transient Overcurrent Delay",
        'unit': "ms",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }

    sensors["bms_"+battery_address+"overcurrent_delay_recovery"] = {
        'state': int.from_bytes(datai_bytes[130:131], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Overcurrent Delay Recovery",
        'unique_id': f"{name_prefix} {battery_address} - Overcurrent Delay Recovery",
        'unit': "s",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Overcurrent recovery times
    sensors["bms_"+battery_address+"overcurrent_recovery_times"] = {
        'state': int.from_bytes(datai_bytes[131:132], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Overcurrent Recovery Times",
        'unique_id': f"{name_prefix} {battery_address} - Overcurrent Recovery Times",
        'unit': "times",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"charge_current_limit_delay"] = {
        'state': int.from_bytes(datai_bytes[132:133], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Charge Current Limit Delay",
        'unique_id': f"{name_prefix} {battery_address} - Charge Current Limit Delay",
        'unit': "minutes",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Charge activation delay
    sensors["bms_"+battery_address+"charge_activation_delay"] = {
        'state': int.from_bytes(datai_bytes[133:134], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Charge Activation Delay",
        'unique_id': f"{name_prefix} {battery_address} - Charge Activation Delay",
        'unit': "minutes",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Charging activation interval
    sensors["bms_"+battery_address+"charging_activation_interval"] = {
        'state': int.from_bytes(datai_bytes[134:135], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Charging Activation Interval",
        'unique_id': f"{name_prefix} {battery_address} - Charging Activation Interval",
        'unit': "hours",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Charge activation times
    sensors["bms_"+battery_address+"charge_activation_times"] = {
        'state': int.from_bytes(datai_bytes[135:136], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Charge Activation Times",
        'unique_id': f"{name_prefix} {battery_address} - Charge Activation Times",
        'unit': "times",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Work record interval
    sensors["bms_"+battery_address+"work_record_interval"] = {
        'state': int.from_bytes(datai_bytes[136:137], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Work Record Interval",
        'unique_id': f"{name_prefix} {battery_address} - Work Record Interval",
        'unit': "minutes",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Standby recording interval
    sensors["bms_"+battery_address+"standby_recording_interval"] = {
        'state': int.from_bytes(datai_bytes[137:138], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Standby Recording Interval",
        'unique_id': f"{name_prefix} {battery_address} - Standby Recording Interval",
        'unit': "minutes",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Standby shutdown delay
    sensors["bms_"+battery_address+"standby_shutdown_delay"] = {
        'state': int.from_bytes(datai_bytes[138:139], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Standby Shutdown Delay",
        'unique_id': f"{name_prefix} {battery_address} - Standby Shutdown Delay",
        'unit': "hours",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }


        # Remaining capacity alarm
    sensors["bms_"+battery_address+"remaining_capacity_alarm"] = {
        'state': int.from_bytes(datai_bytes[139:140], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Remaining Capacity Alarm",
        'unique_id': f"{name_prefix} {battery_address} - Remaining Capacity Alarm",
        'unit': "%",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Remaining  protection
    sensors["bms_"+battery_address+"remaining_capacity_protection"] = {
        'state': int.from_bytes(datai_bytes[140:141], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Remaining Capacity Protection",
        'unique_id': f"{name_prefix} {battery_address} - Remaining Capacity Protection",
        'unit': "%",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Interval charge capacity
    sensors["bms_"+battery_address+"interval_charge_capacity"] = {
        'state': int.from_bytes(datai_bytes[141:142], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Interval Charge Capacity",
        'unique_id': f"{name_prefix} {battery_address} - Interval Charge Capacity",
        'unit': "%",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }

        # Cycle cumulative capacity
    sensors["bms_"+battery_address+"cycle_cumulative_capacity"] = {
        'state': int.from_bytes(datai_bytes[142:143], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Cycle Cumulative Capacity",
        'unique_id': f"{name_prefix} {battery_address} - Cycle Cumulative Capacity",
        'unit': "%",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Connection fault impedance
    sensors["bms_"+battery_address+"connection_fault_impedance"] = {
        'state': int.from_bytes(datai_bytes[143:144], byteorder='big') / 10.0,
        'name': f"{name_prefix} {battery_address} - Connection Fault Impedance",
        'unique_id': f"{name_prefix} {battery_address} - Connection Fault Impedance",
        'unit': "mΩ",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Compensation point 1 position
    sensors["bms_"+battery_address+"compensation_point_1_position"] = {
        'state': int.from_bytes(datai_bytes[144:145], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Compensation Point 1 Position",
        'unique_id': f"{name_prefix} {battery_address} - Compensation Point 1 Position",
        'unit': "",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
        # Compensation point 1 impedance
    sensors["bms_"+battery_address+"compensation_point_1_impedance"] = {
        'state': int.from_bytes(datai_bytes[145:146], byteorder='big') / 10.0,
        'name': f"{name_prefix} {battery_address} - Compensation Point 1 Impedance",
        'unique_id': f"{name_prefix} {battery_address} - Compensation Point 1 Impedance",
        'unit': "mΩ",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"compensation_point_2_position"] = {
        'state': int.from_bytes(datai_bytes[146:147], byteorder='big'),
        'name': f"{name_prefix} {battery_address} - Compensation Point 2 Position",
        'unique_id': f"{name_prefix} {battery_address} - Compensation Point 2 Position",
        'unit': "",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"compensation_point_2_impedance"] = {
        'state': int.from_bytes(datai_bytes[147:148], byteorder='big') / 10.0,
        'name': f"{name_prefix} {battery_address} - Compensation Point 2 Impedance",
        'unique_id': f"{name_prefix} {battery_address} - Compensation Point 2 Impedance",
        'unit': "mΩ",  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }

    return sensors
