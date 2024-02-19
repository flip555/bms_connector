import asyncio
import logging
from datetime import timedelta
from homeassistant.helpers.entity import Entity, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant import config_entries  # Add this import
from .const import (
    NAME,
    DOMAIN,
    VERSION,
    ATTRIBUTION,
)
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.components.binary_sensor import BinarySensorEntity

_LOGGER = logging.getLogger(__name__)
async def async_setup_entry(hass: HomeAssistantType, config_entry: config_entries.ConfigEntry, async_add_entities: AddEntitiesCallback):
    entry_id = config_entry.entry_id 
    await hass.data[DOMAIN]["HOME_ENERGY_HUB_SENSOR_COORDINATOR"+entry_id].async_refresh() 
    coordinator = hass.data[DOMAIN]["HOME_ENERGY_HUB_SENSOR_COORDINATOR"+entry_id]
    _LOGGER.debug("Binary Sensor data: %s", coordinator.data['binary_sensors'])
    if coordinator.data is not None and 'binary_sensors' in coordinator.data:
        sensors = [CreateBinarySensor(coordinator, key) for key in coordinator.data['binary_sensors']]
    else:
        sensors = []
    all_sensors = sensors
    async_add_entities(all_sensors, True)

class CreateBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator, coordinator_key):
        super().__init__(coordinator)
        self._coordinator_key = coordinator_key

    @property
    def device_class(self):
        return self.coordinator.data['binary_sensors'][self._coordinator_key]['device_class']

    @property
    def name(self):
        return self.coordinator.data['binary_sensors'][self._coordinator_key]['name']

    @property
    def unique_id(self):
        return self.coordinator.data['binary_sensors'][self._coordinator_key]['unique_id']

    @property
    def icon(self):
        return self.coordinator.data['binary_sensors'][self._coordinator_key]['icon']

    @property
    def is_on(self):
        # Return the state of the binary sensor.
        # Typically, you would access the coordinator data for the current state like:
        # return self.coordinator.data.get(self._coordinator_key)
        return self.coordinator.data['binary_sensors'][self._coordinator_key]['state']

    @property
    def extra_state_attributes(self):
        return self.coordinator.data['binary_sensors'][self._coordinator_key]['attributes']

    # Add methods for updating, etc.

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        try:
            if self.coordinator.data['binary_sensors'][self._coordinator_key]['device_register']:
                return self.coordinator.data['binary_sensors'][self._coordinator_key]['device_register']       
        except Exception as ex:
            return None