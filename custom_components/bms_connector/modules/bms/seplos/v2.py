from homeassistant.helpers.entity import Entity, DeviceInfo
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
import socket
from datetime import datetime, timezone, timedelta
from homeassistant.helpers import device_registry as dr
from .v2_cid_42 import process_cid_42
from .v2_cid_44 import process_cid_44
from .v2_cid_47 import process_cid_47
from .v2_cid_51 import process_cid_51

from ....const import (
    NAME,
    DOMAIN,
    VERSION,
    ATTRIBUTION,
)

_LOGGER = logging.getLogger(__name__)

async def send_serial_command(command, ser):
    ser.write(command.encode())
    await asyncio.sleep(0.3)
    response = ser.read(ser.in_waiting).decode().replace('\r', '').replace('\n', '')
    return response

async def send_network_command(command, host, port):
    try:
        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to the server
            sock.connect((host, port))
            # Send the command
            sock.sendall(command.encode())
            # Receive the response
            response = sock.recv(1024)
            return response.decode()
    except Exception as e:
        # Handle exceptions
        _LOGGER.debug(e)
        return None

async def make_async_post_request(url, data, config_entry):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            current_time = datetime.utcnow().timestamp()                
            hass.data[DOMAIN]["HEH_SEP_UPDATE_TIME_" + config_entry] = current_time
            return await response.text()

async def listen_serial_port(usb_port, baudrate=19200, timeout=2):
    while True:
        try:
            with serial.Serial(usb_port, baudrate=baudrate, timeout=timeout) as ser:
                while True:
                    data = ser.readline().decode().strip()
                    if data:
                        # Process the received data here
                        _LOGGER.debug(data)  # For debugging purposes
                        # Handle the received data here as needed
                        # Example: You may want to send commands based on received data
                        # command = construct_command(data)  # Some function to determine command based on data
                        # response = await send_serial_command(command, ser)
        except serial.SerialException:
            # Reconnect on failure
            await asyncio.sleep(5)  # Wait for 5 seconds before reconnecting

async def start_network_server(host, port):
    try:
        # Create a TCP/IP server
        server = await asyncio.start_server(handle_network_client, host, port)
        async with server:
            await server.serve_forever()
    except Exception as e:
        # Handle exceptions
        _LOGGER.error(f"Error starting network server: {e}")

async def handle_network_client(reader, writer):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            message = data.decode()
            # Process the received data here
            _LOGGER.debug(f"Network Data: {message}")  # For debugging purposes
    except Exception as e:
        # Handle exceptions
        _LOGGER.error(f"Error handling network client: {e}")
    finally:
        writer.close()

async def get_battery_pack_identifier_if_normal(response):
    # Clean up the response to remove spaces and tildes
    response = ''.join(filter(str.isalnum, response))
    
    # Extract the battery pack identifier (third and fourth characters)
    if (response[2:3] == "0"):
        battery_pack_identifier_hex = response[3:4]
    else:
        battery_pack_identifier_hex = response[2:4]

    # Extract the CID2 (fifth and sixth characters) to determine the response status
    cid2_hex = response[4:6]
    
    # Define the meanings of various CID2 return codes
    cid2_meanings = {
        "00": "Normal",
        "01": "VER error",
        "02": "CHKSUM error",
        "03": "LCHKSUM error",
        "04": "CID2 invalid",
        "05": "Command format error",
        "06": "Data invalid (parameter setting)",
        "07": "No data (history)",
        "E1": "CID1 invalid",
        "E2": "Command execution failure",
        "E3": "Device fault",
        "E4": "Invalid permissions"
    }
    
    
    # Determine the meaning of the CID2 return code
    cid2_status = cid2_meanings.get(cid2_hex.upper(), "Unknown CID2 code")
    
    # Return the battery pack identifier only if CID2 indicates "Normal" operation
    if battery_pack_identifier_hex:
        return battery_pack_identifier_hex
    else:
        return 999


async def SeplosV2BMSDevice(hass, entry):
    async def send_serial_commands(commands, port, baudrate=19200, timeout=2):
        responses = []
        _LOGGER.debug(commands)

        with serial.Serial(port, baudrate=baudrate, timeout=timeout) as ser:
            for command in commands:
                _LOGGER.debug(command)
                ser.write(command.encode())
                await asyncio.sleep(0.5)
                responses.append(ser.read(ser.in_waiting).decode().replace('\r', '').replace('\n', ''))
        _LOGGER.debug(responses)

        return responses

        

    ha_update_time = entry.data.get("sensor_update_frequency")
    usb_port = entry.data.get("usb_port")
    battery_pack_count = entry.data.get("battery_pack_count")
    name_prefix = entry.data.get("name_prefix")
    comm_type = "usb_serial"
    device_registry = dr.async_get(hass)
    sensors = {}
    binary_sensors = {}

    if comm_type == "usb_serial":
        #asyncio.create_task(listen_serial_port(entry.data.get("usb_port")))
        send_command_function = send_serial_command
    elif comm_type == "network":
        #asyncio.create_task(start_network_server(entry.data.get("host"), entry.data.get("port")))
        send_command_function = send_network_command
    else:
        raise ValueError("Invalid communication interface specified")

    async def async_update_data():

        data_coll = {}
        data_coll['seplos'] = 'ok'
        data_coll['id'] = entry.entry_id
        current_address = 0
        device_registry = dr.async_get(hass)  
        V2_COMMAND_ARRAY = {
            "0x00": ["~20004642E00200FD37\r", "~20004644E00200FD35\r", "~20004647E00200FD32\r", "~20004651E00200FD37\r"],
            "0x01": ["~20014642E00201FD35\r", "~20014644E00201FD33\r", "~20014647E00201FD30\r", "~20014651E00201FD36\r"],
            "0x02": ["~20024642E00202FD33\r", "~20024644E00202FD31\r", "~20024647E00202FD2E\r", "~20024651E00202FD35\r"],
            "0x03": ["~20034642E00203FD31\r", "~20034644E00203FD2F\r", "~20034647E00203FD2C\r", "~20034651E00203FD34\r"],
            "0x04": ["~20044642E00204FD2F\r", "~20044644E00204FD2D\r", "~20044647E00204FD2A\r", "~20044651E00204FD33\r"],
            "0x05": ["~20054642E00205FD2D\r", "~20054644E00205FD2B\r", "~20054647E00205FD28\r", "~20054651E00205FD32\r"],
            "0x06": ["~20064642E00206FD2B\r", "~20064644E00206FD29\r", "~20064647E00206FD26\r", "~20064651E00206FD31\r"],
            "0x07": ["~20074642E00207FD29\r", "~20074644E00207FD27\r", "~20074647E00207FD24\r", "~20074651E00207FD30\r"],
            "0x08": ["~20084642E00208FD27\r", "~20084644E00208FD25\r", "~20084647E00208FD22\r", "~20084651E00208FD2F\r"],
            "0x09": ["~20094642E00209FD25\r", "~20094644E00209FD23\r", "~20094647E00209FD20\r", "~20094651E00209FD2E\r"],
            "0x0A": ["~200A4642E0020AFD15\r", "~200A4644E0020AFD13\r", "~200A4647E0020AFD10\r", "~200A4651E0020AFD15\r"],
            "0x0B": ["~200B4642E0020BFD13\r", "~200B4644E0020BFD11\r", "~200B4647E0020BFD0E\r", "~200B4651E0020BFD13\r"],
            "0x0C": ["~200C4642E0020CFD11\r", "~200C4644E0020CFD0F\r", "~200C4647E0020CFD0C\r", "~200C4651E0020CFD11\r"],
            "0x0D": ["~200D4642E0020DFD0F\r", "~200D4644E0020DFD0D\r", "~200D4647E0020DFD0A\r", "~200D4651E0020DFD0F\r"],
            "0x0E": ["~200E4642E0020EFD0D\r", "~200E4644E0020EFD0B\r", "~200E4647E0020EFD08\r", "~200E4651E0020EFD0D\r"],
            "0x0F": ["~200F4642E0020FFD0B\r", "~200F4644E0020FFD09\r", "~200F4647E0020FFD06\r", "~200F4651E0020FFD0B\r"],
            "0x10": ["~20104642E00210FD35\r", "~20104644E00210FD33\r", "~20104647E00200FD31\r", "~20104651E00200FD36\r"],
            "0x11": ["~20114642E00211FD33\r", "~20114644E00211FD31\r", "~20114647E00200FD30\r", "~20114651E00200FD35\r"],
            "0x12": ["~20124642E00212FD31\r", "~20124644E00212FD2F\r", "~20124647E00200FD2F\r", "~20124651E00200FD34\r"],
            "0x13": ["~20134642E00213FD2F\r", "~20134644E00213FD2D\r", "~20134647E00200FD2E\r", "~20134651E00200FD33\r"],
            "0x14": ["~20144642E00214FD2D\r", "~20144644E00214FD2B\r", "~20144647E00200FD2D\r", "~20144651E00200FD32\r"],
            "0x15": ["~20154642E00215FD2B\r", "~20154644E00215FD29\r", "~20154647E00200FD2C\r", "~20154651E00200FD31\r"],
            "0x16": ["~20164642E00216FD29\r", "~20164644E00216FD27\r", "~20164647E00200FD2B\r", "~20164651E00200FD30\r"]
        }

        # Poll all addresses
        while current_address <= battery_pack_count:
            if (current_address >= 10):
                battery_address = f"0x{current_address}"
            else:
                battery_address = f"0x0{current_address}"

            commands = V2_COMMAND_ARRAY[battery_address]
            data = await send_serial_commands(commands, usb_port, baudrate=19200, timeout=2)

            CID_42_RESPONSE = data[0]
            CID_44_RESPONSE = data[1]
            CID_47_RESPONSE = data[2]
            CID_51_RESPONSE = data[3]

            if (battery_address == "0x03"):
                CID_42_RESPONSE = "~2003460010960003100CE40CE10CE40CE20CE40CE10CE30CE30CE30CE50CE20CE50CE40CE50CE20CE5060B360B320B340B310B6B0B44F8EE149F6F140A76C003A776C0000603E8149F00380000029B021ADC9E"
                CID_44_RESPONSE = "~20034600806200001000000000000000000000000000000000060000000000000000140000000000000300000100000000000000000001EB33"
                CID_47_RESPONSE = "~200346008152003C0DAC0D480B540BB80E420E100A8C0B540DE805DC16761644122012C016801676104011F816F816A80C9F0C810ABF0ADD0CD10C9F0A470AAB0CB30C810A470AC90CD10C9F0A150AAB0AAB0B0F0C9F0C810AAB0AC90D030CD10A470AAB0E2F0DFD0E930DFD4E204C2CAFECB0B45208ADF88AD007D059D859D81B321E1E140A100A0A1E3C0505010A0A1EF0300F0560506409000D0008FFFEFF3FBF819F1E313130312D5350373620B2A0"
                CID_51_RESPONSE = "~20034600C040313130312D5350373620100443414E3A56696374726F6E202020202020202020F098"

            battery_pack_from_response = await get_battery_pack_identifier_if_normal(CID_42_RESPONSE)

            if (int(battery_pack_from_response) == int(current_address)):

                CID_42_SENSORS, lowest_voltage_value, highest_voltage_value, cellsCount, cellVoltage = await process_cid_42(CID_42_RESPONSE, battery_address, name_prefix, entry)
                sensors.update(CID_42_SENSORS)

                CID_51_SENSORS, manufacturer_name, software_version, device_name = await process_cid_51(CID_51_RESPONSE, battery_address, name_prefix, entry)
                sensors.update(CID_51_SENSORS)

                CID_44_SENSORS, CID_44_BINARY_SENSORS = await process_cid_44(CID_44_RESPONSE, battery_address, name_prefix, entry, lowest_voltage_value, highest_voltage_value, cellsCount, cellVoltage)
                sensors.update(CID_44_SENSORS)
                binary_sensors.update(CID_44_BINARY_SENSORS)

                CID_47_SENSORS = await process_cid_47(CID_47_RESPONSE, battery_address, name_prefix, entry)
                sensors.update(CID_47_SENSORS)

                device_registry.async_get_or_create(
                    config_entry_id=entry.entry_id,
                    identifiers={("bms_connector", entry.entry_id, battery_address)},
                    manufacturer="Seplos BMS",
                    name=f"Seplos V2: {battery_address}",
                    model="Seplos V2 | "+manufacturer_name,
                    sw_version=software_version,
                    serial_number=device_name
                )



            current_address += 1

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
