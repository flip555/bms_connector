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
from homeassistant.helpers.entity_registry import async_get
from homeassistant.core import callback

from ....const import (
    NAME,
    DOMAIN,
    VERSION,
    ATTRIBUTION,
)

import serial_asyncio


_LOGGER = logging.getLogger(__name__)

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

class SeplosV2BMSDevice:
    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry
        self.reader = None
        self.writer = None
        self.ha_update_time = entry.data.get("sensor_update_frequency")
        self.usb_port = entry.data.get("usb_port")
        self.battery_pack_count = entry.data.get("battery_pack_count")
        self.name_prefix = entry.data.get("name_prefix")
        self.comm_type = "usb_serial"
        self.device_registry = dr.async_get(hass)
        self.sensors = {}
        self.bms_array = {}
        self.binary_sensors = {}
        self.data_update_coordinator = None
        self.latest_data = "" 
        self.lowest_voltage = None
        self.lowest_voltage_value = None
        self.highest_voltage_value = None
        self.forsensors = {}
        self.data_current = {}
        self.data_packvoltage = {}
        self.setup = None

    async def _async_setup(self):

        self.data_update_coordinator = DataUpdateCoordinator(
            self.hass,
            _LOGGER,
            name=f"home_energy_hub_{self.entry.entry_id}",
            update_method=self.async_update_data,
            update_interval=timedelta(seconds=self.ha_update_time),
        )
        await self.data_update_coordinator.async_refresh()

        # Store the coordinator in hass.data
        coordinator_key = f"HOME_ENERGY_HUB_SENSOR_COORDINATOR{self.entry.entry_id}"
        self.hass.data[DOMAIN][coordinator_key] = self.data_update_coordinator

        self.hass.loop.create_task(self.initialize_serial_connection())
        self.hass.loop.create_task(self.continuous_serial_listener())

    async def initialize_serial_connection(self):
        """Open serial connection and store reader and writer."""
        try:
            self.reader, self.writer = await serial_asyncio.open_serial_connection(
                url=self.usb_port, baudrate=19200)
            _LOGGER.debug(f"Serial port {self.usb_port} opened successfully.")
        except Exception as e:
            _LOGGER.error(f"Failed to open serial port {self.usb_port}: {e}")

    async def continuous_serial_listener(self):
        """Continuously listen to the serial port, and optionally send commands."""
        if not self.reader:
            _LOGGER.error("Serial reader is not initialized.")
            return
        try:
            while True:
                line = await self.reader.readuntil(separator=b'\r')
                decoded_line = line.decode('utf-8').rstrip('\r')
                self.latest_data = decoded_line
                _LOGGER.debug(f"Received from serial: {self.latest_data}")

                if decoded_line.startswith("~"):
                    buffer = decoded_line[1:]
                    buffer_battery_address = buffer[2:4]
                    cid2 = await self.check_response_cid(buffer, buffer_battery_address)
                    _LOGGER.debug(f"Received from serial CID2: {cid2}")
                else:
                    buffer = decoded_line
                    buffer_battery_address = "ERROR"



        except asyncio.IncompleteReadError:
            _LOGGER.error("Serial connection was closed.")
        except Exception as e:
            _LOGGER.error(f"Error in serial listener: {e}")
        # Consider adding reconnection logic here

    async def send_command(self, command):
        """Send a command to the serial device, using the stored writer."""
        if self.writer is None:
            _LOGGER.error("Serial connection is not initialized.")
            #await self.initialize_serial_connection()
            return
        _LOGGER.debug(f"Sending command to serial: {command}")
        self.writer.write(command.encode())
        await self.writer.drain()  # Ensure the command is fully sent

    async def check_response_cid(self, response, battery_address):
        _LOGGER.debug(f"Checking response CID for battery address {battery_address} with response length {len(response)}")
        if len(response) > 50:
            if battery_address not in self.bms_array:
                _LOGGER.debug(f"Initializing bms_array entry for battery address {battery_address}")
                self.bms_array[battery_address] = {"47": {}, "42": {}, "44": {}, "51": {}}

            current_timestamp = datetime.now().isoformat()

            if len(response) > 300:
                _LOGGER.debug(f"Updating '47' response for battery address {battery_address}")
                self.bms_array[battery_address]["47"] = {"response": response, "timestamp": current_timestamp}
                return "47"
            elif len(response) > 150:
                _LOGGER.debug(f"Updating '42' response for battery address {battery_address}")
                self.bms_array[battery_address]["42"] = {"response": response, "timestamp": current_timestamp}
                return "42"
            elif len(response) > 100:
                _LOGGER.debug(f"Updating '44' response for battery address {battery_address}")
                self.bms_array[battery_address]["44"] = {"response": response, "timestamp": current_timestamp}
                return "44"
            elif len(response) > 60:
                _LOGGER.debug(f"Updating '51' response for battery address {battery_address}")
                self.bms_array[battery_address]["51"] = {"response": response, "timestamp": current_timestamp}
                return "51"
            else:
                _LOGGER.debug(f"No CID match for response length {len(response)} for battery address {battery_address}")
                return "99"
        else:
            return "98"


    async def async_update_data(self):
        """Method called by DataUpdateCoordinator to fetch the latest data."""
        _LOGGER.debug("Latest data being processed...")
        current_address = 0


        # Poll all addresses
        while current_address <= self.battery_pack_count:
            if (current_address >= 10):
                battery_address = f"0x{current_address}"
                current_address_two = current_address
            else:
                battery_address = f"0x0{current_address}"
                current_address_two = f"0{current_address}"

            current_address += 1

            commands = V2_COMMAND_ARRAY[battery_address]
            for command in commands:
                await self.send_command(command)
                await asyncio.sleep(0.5) 

        _LOGGER.debug(f"Latest Modbus Data: {self.bms_array}")
        sensors = {}
        for battery_pack in self.bms_array:

            battery_number = "0x"+battery_pack

            if '42' in self.bms_array[battery_pack]:
                _LOGGER.debug(f"{battery_pack} - Latest Modbus 42 Data: {self.bms_array[battery_pack]['42']}")
                CID_42_SENSORS, lowest_voltage_value, highest_voltage_value, cellsCount, cellVoltage = await process_cid_42(self.bms_array[battery_pack]['42']['response'], '0x'+battery_pack, self.name_prefix, self.entry)
                self.sensors.update(CID_42_SENSORS)

            if '44' in self.bms_array[battery_pack]:
                _LOGGER.debug(f"{battery_pack} - Latest Modbus 44 Data: {self.bms_array[battery_pack]['44']}")
                CID_44_SENSORS, CID_44_BINARY_SENSORS = await process_cid_44(self.bms_array[battery_pack]['44']['response'], '0x'+battery_pack, self.name_prefix, self.entry, lowest_voltage_value, highest_voltage_value, cellsCount, cellVoltage)
                self.sensors.update(CID_44_SENSORS)
                self.binary_sensors.update(CID_44_BINARY_SENSORS)

            if '47' in self.bms_array[battery_pack]:
                _LOGGER.debug(f"{battery_pack} - Latest Modbus 47 Data: {self.bms_array[battery_pack]['47']}")
                CID_47_SENSORS = await process_cid_47(self.bms_array[battery_pack]['47']['response'], '0x'+battery_pack, self.name_prefix, self.entry)
                self.sensors.update(CID_47_SENSORS)

            if '51' in self.bms_array[battery_pack]:
                _LOGGER.debug(f"{battery_pack} - Latest Modbus 51 Data: {self.bms_array[battery_pack]['51']}")
                CID_51_SENSORS, manufacturer_name, software_version, device_name = await process_cid_51(self.bms_array[battery_pack]['51']['response'], '0x'+battery_pack, self.name_prefix, self.entry)
                if manufacturer_name:
                    self.device_registry.async_get_or_create(
                        config_entry_id=self.entry.entry_id,
                        identifiers={("bms_connector", self.entry.entry_id, battery_number)},
                        manufacturer="Seplos BMS",
                        name=f"Seplos V2: {battery_number}",
                        model="Seplos V2 | "+manufacturer_name,
                        sw_version=software_version,
                        serial_number=device_name
                    )
                self.sensors.update(CID_51_SENSORS)

        ##########################################################################################################################################
        #
        # Initialization phase: At this point, Modbus data hasn't been received yet, so we need to create placeholder entities in Home Assistant. 
        # The ideal approach would be to dynamically adjust (add, recreate, or reinitialize) entities with each update to reflect the latest data. 
        # However, it's important to consider Home Assistant's architecture to ensure compatibility with dynamic entity management. 
        # This setup block ensures that the initial setup process runs only once.
        #
        # Alternative approach: Consider enhancing the initial setup process by polling serial data during the configuration flow or options flow. 
        # This strategy could allow for the generation of entities based on actual data, minimizing the creation of "junk" entities that might never receive data. 
        # Implementing this approach during the setup phase could ensure that entities are created with meaningful data from the start, improving the overall
        # integration experience and alignment with Home Assistant's design principles.
        #
        ##########################################################################################################################################


        if self.setup == None:
            self.setup = 1

            current_battery_pack = 0
            while current_battery_pack < self.battery_pack_count:
                if (current_battery_pack >= 10):
                    battery_number = f"0x{current_battery_pack}"
                    current_address_two = current_battery_pack
                else:
                    battery_number = f"0x0{current_battery_pack}"
                    current_address_two = f"0{current_battery_pack}"

                current_battery_pack += 1
 
                # 42H Sensor Setup
                self.sensors[battery_number+"current"] = {
                    'state': 0,
                    'name': f"{self.name_prefix} {battery_number} - Current",
                    'unique_id': f"{self.name_prefix} {battery_number} - Current",
                    'unit': "A",
                    'icon': "",
                    'device_class': "",
                    'state_class': "",
                    'availability': False,
                    'attributes': {},
                    'device_register': DeviceInfo(
                                identifiers={("bms_connector", self.entry.entry_id, battery_number)},
                            )                   
                }
                self.sensors[battery_number+"voltage"] = {
                    'state': 0,
                    'name': f"{self.name_prefix} {battery_number} - Voltage",
                    'unique_id': f"{self.name_prefix} {battery_number} - Voltage",
                    'unit': "v",
                    'icon': "",
                    'device_class': "",
                    'state_class': "",
                    'availability': False,
                    'attributes': {},
                    'device_register': DeviceInfo(
                                identifiers={("bms_connector", self.entry.entry_id, battery_number)},
                            ) 
                }

                # 44H Sensor Setup
                self.sensors["bms_"+battery_number+"systemState"] = {
                    'state': 0,
                    'name': f"{self.name_prefix} {battery_number} - System State",
                    'unique_id': f"{self.name_prefix} {battery_number} - System State",
                    'unit': None,
                    'icon': "",
                    'device_class': "",
                    'state_class': "",
                    'availability': False,
                    'attributes': {},
                    'device_register': DeviceInfo(
                                identifiers={("bms_connector", self.entry.entry_id, battery_number)},
                            ) 
                }

                # 47H Sensor Setup
                self.sensors["bms_"+battery_number+"monomer_high_voltage_alarm"] = {
                    'state': 0,
                    'name': f"{self.name_prefix} {battery_number} - Monomer High Voltage Alarm",
                    'unique_id': f"{self.name_prefix} {battery_number} - Monomer High Voltage Alarm",
                    'unit': "v",
                    'icon': "",
                    'device_class': "",
                    'state_class': "",
                    'availability': False,
                    'attributes': {},
                    'device_register': DeviceInfo(
                                identifiers={("bms_connector", self.entry.entry_id, battery_number)},
                            ) 
                }

                # 51H Sensor Setup
                self.sensors["bms_"+battery_number+"device_name"] = {
                    'state': 0,
                    'name': f"{self.name_prefix} {battery_number} - Device Name",
                    'unique_id': f"{self.name_prefix} {battery_number} - Device Name",
                    'unit': None,
                    'icon': "",
                    'device_class': "",
                    'state_class': "",
                    'availability': False,
                    'attributes': {},
                    'device_register': DeviceInfo(
                                identifiers={("bms_connector", self.entry.entry_id, battery_number)},
                            ) 
                }


                self.device_registry.async_get_or_create(
                    config_entry_id=self.entry.entry_id,
                    identifiers={("bms_connector", self.entry.entry_id, battery_number)},
                    manufacturer="Seplos BMS",
                    name=f"Seplos V2: {battery_number}"
                )

        _LOGGER.debug(f"self.sensors: {self.sensors}")

        return {
            'binary_sensors': self.binary_sensors,
            'sensors': self.sensors
        }

    

    @classmethod
    async def create_and_setup(cls, hass, entry):
        instance = cls(hass, entry)
        await instance._async_setup()
        return instance

