import asyncio
import logging
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant import config_entries  # Add this import

#################################################
############## BMS Routing Imports ##############
#################################################
from .bms.seplos.v2.sensors import generate_sensors as SEPLOS_V2_START
from .bms.seplos.v3.sensors import generate_sensors as SEPLOS_V3_START

_LOGGER = logging.getLogger(__name__)
coordinator = None  # Define coordinator at a higher scope

async def initialize_bms_component(hass, config_entry):
    pass

async def async_setup_entry(hass: HomeAssistantType, config_entry: config_entries.ConfigEntry, async_add_entities: AddEntitiesCallback):
    try:
        sensor_prefix = config_entry.data.get("sensor_prefix")
        bms_type = config_entry.data.get("bms_type")
        port = config_entry.data.get("connector_port")
        battery_address = config_entry.data.get("battery_address")
        entry = config_entry.data

        _LOGGER.debug("Sensor Prefix: %s", sensor_prefix)
        _LOGGER.debug("BMS Type: %s", bms_type)
        _LOGGER.debug("Port: %s", port)
        _LOGGER.debug("Battery Address: %s", battery_address)

        #################################################
        ############### BMS Routing Logic ###############
        #################################################

        # For SEPLV2 BMS's
        if bms_type == "SEPLV2":
            _LOGGER.debug("%s selected. Routing now..", bms_type)
            await SEPLOS_V2_START(hass, bms_type, port, battery_address, sensor_prefix, entry, async_add_entities)

        # For SEPLV3 BMS's
        elif bms_type == "SEPLV3":
            _LOGGER.debug("%s selected. Routing now..", bms_type)
            await SEPLOS_V3_START(hass, bms_type, port, battery_address, sensor_prefix, entry, async_add_entities)

        else:
            _LOGGER.error("Unsupported BMS type")

    except Exception as e:
        _LOGGER.error("Error setting up BMS sensors: %s", e)
