import asyncio
import logging
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.core import HomeAssistant
from homeassistant import config_entries

#################################################
############## BMS Routing Imports ##############
#################################################
from .bms.seplos.v2.sensors import generate_sensors as SEPLOS_V2_START
from .bms.seplos.v3.sensors import generate_sensors as SEPLOS_V3_START

_LOGGER = logging.getLogger(__name__)

async def initialize_bms_component(hass, config_entry):
    pass

async def async_setup_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry, async_add_entities: AddEntitiesCallback):
    try:
        sensor_prefix = config_entry.data.get("sensor_prefix")
        bms_type = config_entry.data.get("bms_type")
        battery_address = config_entry.data.get("battery_address")
        connection_type = config_entry.data.get("connection_type", "usb_serial")
        entry_id = config_entry.entry_id

        # Build connector info for the sensors
        connector_info = {
            "type": connection_type,
        }
        if connection_type == "telnet":
            connector_info["host"] = config_entry.data.get("host")
            connector_info["port"] = config_entry.data.get("port", 23)
            connector_info["timeout"] = 8
        else:
            connector_info["port"] = config_entry.data.get("connector_port")
            connector_info["baudrate"] = 19200

        _LOGGER.debug("Sensor Prefix: %s", sensor_prefix)
        _LOGGER.debug("BMS Type: %s", bms_type)
        _LOGGER.debug("Connection: %s", connection_type)
        _LOGGER.debug("Battery Address: %s", battery_address)

        #################################################
        ############### BMS Routing Logic ###############
        #################################################

        if bms_type == "SEPLV2":
            _LOGGER.debug("%s selected. Routing now..", bms_type)
            await SEPLOS_V2_START(hass, bms_type, connector_info, battery_address, sensor_prefix, entry_id, async_add_entities)

        elif bms_type == "SEPLV3":
            _LOGGER.debug("%s selected. Routing now..", bms_type)
            await SEPLOS_V3_START(hass, bms_type, connector_info, battery_address, sensor_prefix, entry_id, async_add_entities)

        else:
            _LOGGER.error("Unsupported BMS type")

    except Exception as e:
        _LOGGER.error("Error setting up BMS sensors: %s", e)
