"""Binary sensors for BMS Connector (V3 PIC alarms and SFA switch states)."""

import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .bms.seplos.v3.vendor_spec import PIC_BITS, SFA_BITS
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class SeplosV3BinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Read-only alarm bit (PIC) or switch state bit (SFA)."""

    def __init__(self, coordinator, kind, index, name, battery_address,
                 sensor_prefix, entry_id):
        super().__init__(coordinator)
        self._kind = kind
        self._index = index
        self._attr_has_entity_name = False
        self._attr_name = f"{sensor_prefix} {battery_address} {name}"
        # Index is part of the identity: PIC/SFA both contain duplicate
        # "Reservation" labels.
        self._attr_unique_id = (
            f"bms_connector_v3_{entry_id}_{kind}_{battery_address}_{index}_{name}"
        )
        settings = kind == "sfa"
        suffix = "_settings" if settings else ""
        self._attr_device_info = DeviceInfo(
            identifiers={("bms_connector", f"seplos_v3_{entry_id}{suffix}")},
            name=f"{sensor_prefix} Settings" if settings else f"{sensor_prefix}",
            manufacturer="Seplos",
            model="V3 Settings" if settings else "V3 BMS",
            sw_version="Unknown",
        )

    @property
    def is_on(self):
        data = self.coordinator.data
        offset = 4 if self._kind == "pic" else 5
        if isinstance(data, tuple) and len(data) > offset and data[offset] is not None:
            try:
                return bool(data[offset].bits[self._index])
            except (IndexError, TypeError):
                return False
        return False


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry,
                            async_add_entities: AddEntitiesCallback):
    if entry.data.get("bms_type") != "SEPLV3":
        return
    coordinator = hass.data.get(DOMAIN, {}).get("coordinators", {}).get(entry.entry_id)
    if coordinator is None:
        _LOGGER.debug("No V3 coordinator for %s; skipping binary sensors", entry.entry_id)
        return

    address = entry.data.get("battery_address", "0x00")
    prefix = entry.data.get("sensor_prefix", "Seplos V3")
    entities = []
    for index, item in enumerate(PIC_BITS):
        entities.append(SeplosV3BinarySensor(
            coordinator, "pic", index, item["name"], address, prefix, entry.entry_id))
    for index, item in enumerate(SFA_BITS):
        entities.append(SeplosV3BinarySensor(
            coordinator, "sfa", index, item["name"], address, prefix, entry.entry_id))
    async_add_entities(entities, True)
