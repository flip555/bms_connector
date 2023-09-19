from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from ....connector.local_serial.seplos_v3_local_serial import send_serial_command
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.entity_component import EntityComponent

from .data_parser import extract_data_from_message
import asyncio
import logging
from datetime import timedelta
from ....const import (
    NAME,
    DOMAIN,
    VERSION,
    ATTRIBUTION,
)
from .const import (
    ALARM_ATTRIBUTES,
    ALARM_MAPPINGS,
    SYSTEM_ATTRIBUTES,
    SETTINGS_ATTRIBUTES,
)

_LOGGER = logging.getLogger(__name__)

# Define the generate_sensors function
async def generate_sensors(hass, bms_type, port, config_battery_address, sensor_prefix, entry, async_add_entities):
    class DerivedSeplosBMSSensor(SeplosBMSSensorBase):
        def __init__(self, *args, **kwargs):
            self._calc_function = kwargs.pop("calc_function", None)
            super().__init__(*args, **kwargs)
            self._config_battery_address = config_battery_address

        @property
        def state(self):
            if self._calc_function:
                result = self._calc_function(self.coordinator.data)
                _LOGGER.debug("Derived sensor '%s' calculated value: %s", self._name, result)
                return result
            return super().state
            


    async def async_update_data():

        #Need to add battery address like v2 and generate
        commands = ["0004100000127516", "00041100001274ea"]
        #test_responses = ['0004241499fe6338d63a98005d03ca03e700070cdf0b940ce50cda0b940b9400000096009603e84f7c', '0004240cdd0ce50cdf0cdd0ce40cdc0cda0ce10ce20ce20ce40cde0ce10cde0cdd0ce20b940b94e3e4']

        # Loop for multiple battery packs should start here using TELEMETRY_COMMANDS from const.py 0-15 as COMMAND_1
        #telemetry_data_str = test_responses #await hass.async_add_executor_job(send_serial_command, commands, port)
        # Loop for multiple battery packs should start here using TELEMETRY_COMMANDS from const.py 0-15 as COMMAND_1
        telemetry_data_str = await hass.async_add_executor_job(send_serial_command, commands, port)
        battery_address, telemetry, alarms, system_details, protection_settings = extract_data_from_message(telemetry_data_str, True, True, True, config_battery_address)

        return battery_address, telemetry, alarms, system_details, protection_settings

    battery_address, telemetry, alarms, system_details, protection_settings = await async_update_data()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="seplos_bms_sensor",
        update_method=async_update_data,
        update_interval=timedelta(seconds=5),  # Define how often to fetch data
    )
    _LOGGER.debug("async_refresh data generate_sensors called")
    await coordinator.async_refresh() 

    pia_sensors = [
        SeplosBMSSensorBase(coordinator, port, "pack_voltage", "Pack Voltage", "V", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "current", "Current", "A", "mdi:current-ac", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "remaining_capacity", "Remaining Capacity", "Ah", "mdi:battery-charging-wireless", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "total_capacity", "Total Capacity", "Ah", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "total_discharge_capacity", "Total Discharge Capacity", "Ah", "mdi:battery-discharging", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "soc", "State of Charge", "%", "mdi:gauge", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "soh", "State of Health", "%", "mdi:gauge", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cycle", "Cycle", "", "mdi:numeric", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "avg_cell_voltage", "Avg Cell Voltage", "V", "mdi:battery-20", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "avg_cell_temperature", "Avg Cell Temperature", "°C", "mdi:thermometer", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "max_cell_voltage", "Max Cell Voltage", "V", "mdi:battery-high", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "min_cell_voltage", "Min Cell Voltage", "V", "mdi:battery-low", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "max_cell_temperature", "Max Cell Temperature", "°C", "mdi:thermometer-chevron-up", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "min_cell_temperature", "Min Cell Temperature", "°C", "mdi:thermometer-chevron-down", battery_address=battery_address, sensor_prefix=sensor_prefix),
    ]

    pib_sensors = [
        SeplosBMSSensorBase(coordinator, port, "cell1_voltage", "Cell 1 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cell2_voltage", "Cell 2 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cell3_voltage", "Cell 3 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cell4_voltage", "Cell 4 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cell5_voltage", "Cell 5 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cell6_voltage", "Cell 6 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cell7_voltage", "Cell 7 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cell8_voltage", "Cell 8 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cell9_voltage", "Cell 9 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cell10_voltage", "Cell 10 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cell11_voltage", "Cell 11 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cell12_voltage", "Cell 12 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cell13_voltage", "Cell 13 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cell14_voltage", "Cell 14 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cell15_voltage", "Cell 15 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        SeplosBMSSensorBase(coordinator, port, "cell16_voltage", "Cell 16 Voltage", "V", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix),
        # Add other sensors for PIB as needed
    ]
    # Combine all sensor lists
    sensors = pia_sensors + pib_sensors 

    async_add_entities(sensors, True)

class SeplosBMSSensorBase(CoordinatorEntity):
    def interpret_alarm(self, event, value):
        flags = ALARM_MAPPINGS.get(event, [])

        if not flags:
            return f"Unknown event: {event}"

        # For other alarm events, interpret them as bit flags
        triggered_alarms = [flag for idx, flag in enumerate(flags) if value is not None and value & (1 << idx)]
        return ', '.join(triggered_alarms) if triggered_alarms else "No Alarm"
   
    def __init__(self, coordinator, port, attribute, name, unit=None, icon=None, battery_address=None, sensor_prefix=None):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._port = port
        self._attribute = attribute
        self._name = name
        self._unit = unit
        self._icon = icon
        self._battery_address = battery_address
        self._sensor_prefix = sensor_prefix


    @property
    def name(self):
        """Return the name of the sensor."""
        prefix = f"{self._sensor_prefix} - {self._battery_address} -"
        return f"{prefix} {self._name}"
        
    @property
    def unique_id(self):
        """Return a unique ID for this entity."""
        prefix = f"{self._sensor_prefix}_{self._battery_address}_"
        return f"{prefix}{self._name}"

    @property
    def state(self):
        """Return the state of the sensor."""
        if not self._attribute:  # Check if attribute is None or empty
            return super().state

        base_attribute = self._attribute.split('[')[0] if '[' in self._attribute else self._attribute

        value = None
        if isinstance(self.coordinator.data, tuple):
            battery_address_data, telemetry_data, alarms_data, system_details_data, protection_settings_data = self.coordinator.data
            value = self.get_value(telemetry_data) or self.get_value(alarms_data) or self.get_value(system_details_data) or self.get_value(protection_settings_data)
        else:
            value = self.get_value(self.coordinator.data)

        if value is None or value == '':
            if base_attribute == 'current':
                _LOGGER.debug("Current seems to be None, setting to 0.00 to fix HA reporting as unknown")
                return 0.00
            else:
                _LOGGER.warning("No data found in telemetry or alarms for %s", self._name)
                return None
                


        _LOGGER.debug("Sensor state for %s: %s", self._name, value)
        return value


    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    def get_value(self, telemetry_data):
        """Retrieve the value based on the attribute."""
        # If the attribute name contains a bracket, it's trying to access a list
        if '[' in self._attribute and ']' in self._attribute:
            attr, index = self._attribute.split('[')
            index = int(index.rstrip(']'))
            # Check if the attribute exists in telemetry_data
            if hasattr(telemetry_data, attr):
                list_data = getattr(telemetry_data, attr)
                if index < len(list_data):
                    value = list_data[index]
                    return value
        else:
            value = getattr(telemetry_data, self._attribute, None)
            return value

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon