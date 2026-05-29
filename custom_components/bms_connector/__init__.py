"""BMS Connector custom component."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

# Import the initialize_bms_component function from sensor.py
from .sensor import initialize_bms_component

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

PLATFORMS = ["sensor"]


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate config entry from old version to new version."""
    _LOGGER.info(
        "Migrating config entry %s from version %s to %s",
        config_entry.entry_id, config_entry.version, config_entry.version + 1,
    )

    if config_entry.version == 1:
        bms_type = config_entry.data.get("bms_type")
        sensor_prefix = config_entry.data.get("sensor_prefix", "")
        battery_address = config_entry.data.get("battery_address", "0x00")

        entity_registry = er.async_get(hass)

        if bms_type == "SEPLV2":
            # Old unique_id: {sensor_prefix}_{battery_address}_{name}
            old_prefix = f"{sensor_prefix.lower().replace(' ', '_')}_{battery_address}_"

            for entity in list(entity_registry.entities.values()):
                if entity.config_entry_id != config_entry.entry_id:
                    continue
                if entity.unique_id and entity.unique_id.startswith(old_prefix):
                    entity_name = entity.unique_id[len(old_prefix):]
                    new_unique_id = f"bms_connector_v2_{config_entry.entry_id}_{entity_name}"

                    _LOGGER.info(
                        "Migrating entity %s: unique_id %s -> %s",
                        entity.entity_id, entity.unique_id, new_unique_id,
                    )
                    entity_registry.async_update_entity(
                        entity.entity_id,
                        new_unique_id=new_unique_id,
                    )

        elif bms_type == "SEPLV3":
            # Old unique_id was: sep_bms_ha_v3_{battery_address}_{name}
            # or sep_bms_ha_v3_{name} if battery_address was empty
            old_prefix_with_addr = f"sep_bms_ha_v3_{battery_address}_"
            old_prefix_no_addr = "sep_bms_ha_v3_"

            for entity in list(entity_registry.entities.values()):
                if entity.config_entry_id != config_entry.entry_id:
                    continue
                if entity.unique_id:
                    if entity.unique_id.startswith(old_prefix_with_addr):
                        entity_name = entity.unique_id[len(old_prefix_with_addr):]
                    elif entity.unique_id.startswith(old_prefix_no_addr):
                        entity_name = entity.unique_id[len(old_prefix_no_addr):]
                    else:
                        continue

                    new_unique_id = f"bms_connector_v3_{config_entry.entry_id}_{entity_name}"

                    _LOGGER.info(
                        "Migrating entity %s: unique_id %s -> %s",
                        entity.entity_id, entity.unique_id, new_unique_id,
                    )
                    entity_registry.async_update_entity(
                        entity.entity_id,
                        new_unique_id=new_unique_id,
                    )

    _LOGGER.info("Migration to version 2 complete for entry %s", config_entry.entry_id)
    return True


async def async_setup(hass, config):
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await initialize_bms_component(hass, entry)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
