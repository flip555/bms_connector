from homeassistant.helpers.entity import Entity, DeviceInfo

async def process_cid_51(CID_51_RESPONSE, battery_address, name_prefix, entry):
    sensors = {}
    data_coll = {}
    # PROCESS 42H CODES
    info_str = CID_51_RESPONSE

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

    sensors["bms_"+battery_address+"device_name"] = {
        'state': device_name,
        'name': f"{name_prefix} {battery_address} - Device Name",
        'unique_id': f"{name_prefix} {battery_address} - Device Name",
        'unit': None,  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'availability': True,
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"software_version"] = {
        'state': software_version,
        'name': f"{name_prefix} {battery_address} - Software Version",
        'unique_id': f"{name_prefix} {battery_address} - Software Version",
        'unit': None,  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }
    sensors["bms_"+battery_address+"manufacturer_name"] = {
        'state': manufacturer_name,
        'name': f"{name_prefix} {battery_address} - Inverter Manufacturer Name",
        'unique_id': f"{name_prefix} {battery_address} - Inverter Manufacturer Name",
        'unit': None,  # Assuming the unit is Celsius
        'icon': "",  # Example icon, you can change it
        'device_class': "",
        'state_class': "",
        'attributes': {},
        'device_register': DeviceInfo(
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                )
    }

    return sensors, manufacturer_name, software_version, device_name
