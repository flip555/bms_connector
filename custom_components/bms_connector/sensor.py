import asyncio
import logging
from datetime import timedelta
from homeassistant.helpers.entity import Entity, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.entity_registry import (
    RegistryEntryDisabler,
    async_entries_for_config_entry,
    async_get,
)
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
    if coordinator.data is not None and 'sensors' in coordinator.data:
        sensors = [CreateSensor(coordinator, key) for key in coordinator.data['sensors']]
    else:
        sensors = []
    all_sensors = sensors
    async_add_entities(all_sensors, True)


class CreateSensor(CoordinatorEntity):
    def __init__(self, coordinator, coordinator_key):
        super().__init__(coordinator)
        self._coordinator_key = coordinator_key
    @property
    def device_class(self):
        return self.coordinator.data['sensors'][self._coordinator_key]['device_class']

    @property
    def state_class(self):
        return self.coordinator.data['sensors'][self._coordinator_key]['state_class']

    @property
    def name(self):
        return f"{self.coordinator.data['sensors'][self._coordinator_key]['name']}"

    @property
    def unique_id(self):
        return f"{self.coordinator.data['sensors'][self._coordinator_key]['unique_id']}"

    @property
    def icon(self):
        return self.coordinator.data['sensors'][self._coordinator_key]['icon']

    @property
    def state(self):
        return self.coordinator.data['sensors'][self._coordinator_key]['state']

    @property
    def unit_of_measurement(self):
        return self.coordinator.data['sensors'][self._coordinator_key]['unit']

    @property
    def extra_state_attributes(self):
        return self.coordinator.data['sensors'][self._coordinator_key]['attributes']

    @property
    def force_update(self):
        return True

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.data['sensors'][self._coordinator_key]['availability']

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        try:
            if self.coordinator.data['sensors'][self._coordinator_key]['device_register']:
                return self.coordinator.data['sensors'][self._coordinator_key]['device_register']       
        except Exception as ex:
            return None

