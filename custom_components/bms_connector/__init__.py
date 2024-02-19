from __future__ import annotations
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er, config_validation as cv

from .const import DOMAIN, PLATFORMS
import voluptuous as vol

# === CONTRIBUTING-ADDON-MARKER:IMPORTS-START ===
# Add your module imports here. 
# If you're adding a new module, import it in this section.
from .modules.global_settings import HomeEnergyHubGlobalSettings
from .modules.bms.seplos.v2old import SeplosV2BMS
from .modules.bms.seplos.v2 import SeplosV2BMSDevice

# Example: 
# from .modules.category.your_module import YourClass
# === CONTRIBUTING-ADDON-MARKER:IMPORTS-END ===
import logging
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    
    # Use options if they exist, otherwise default to entry data
    config_data = entry.data
    hass.data[DOMAIN][entry.entry_id] = config_data
    try:
        # Check the disclaimer value and proceed accordingly
        if config_data.get("home_enery_hub_first_run") == 1:
            _LOGGER.debug("Home Energy Hub Global Settings Loading...")
            await HomeEnergyHubGlobalSettings(hass, entry)

        # === CONTRIBUTING-ADDON-MARKER:LOGIC-START ===
        # Logical Checks and coordinators should be set here!
        elif config_data.get("home_energy_hub_registry") in ["30101"]:
            _LOGGER.debug("Seplos V2 BMS Selected..")
            await SeplosV2BMS(hass, entry)

        elif config_data.get("home_energy_hub_registry") in ["30110"]:
            _LOGGER.debug("Seplos V2 BMS Device Selected..")
            await SeplosV2BMSDevice(hass, entry)
        

        # === CONTRIBUTING-ADDON-MARKER:LOGIC-END ===
        else:
            _LOGGER.error("Error Setting up Entry")

    except Exception as e:
        _LOGGER.error("Error setting up BMS Connector: %s", e)

    #await HomeEnergyHubINIT(hass, entry)


    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    if entry.data.get("home_energy_hub_registry") in ["20191"] or entry.data.get("home_energy_hub_registry") in ["20101"]:
        # Unload and setup entry again
        await async_unload_entry(hass, entry)
        await async_setup_entry(hass, entry)

        # Update stored data with the new configuration
        hass.data[DOMAIN][entry.entry_id] = entry.data
    else:
        await async_unload_entry(hass, entry)
        await async_setup_entry(hass, entry)


