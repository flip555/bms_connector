from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .seplos_helper import send_serial_command, extract_data_from_message, Telemetry, Alarms, parse_telemetry_info, parse_teledata_info

import logging
import time

from datetime import timedelta

_LOGGER = logging.getLogger(__name__)

from .const import DOMAIN
from .seplos_helper import send_serial_command, extract_data_from_message

# Define your two commands to be sent
COMMAND_1 = "~200046420000FDAE\r"
COMMAND_2 = "~200046440000FDAC\r"
class SeplosBMSSensorBase(CoordinatorEntity):
    """Base class for Seplos BMS sensors."""
    
    ALARM_ATTRIBUTES = [
        "cellAlarm", "tempAlarm", "currentAlarm", "voltageAlarm",
        "customAlarms", "alarmEvent0", "alarmEvent1", "alarmEvent2",
        "alarmEvent3", "alarmEvent4", "alarmEvent5", "alarmEvent6",
        "alarmEvent7", "onOffState", "equilibriumState0", "equilibriumState1",
        "systemState", "disconnectionState0", "disconnectionState1"
    ]
    
    def __init__(self, coordinator, port, attribute, name, unit=None, icon=None):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._port = port
        self._attribute = attribute
        self._name = name
        self._unit = unit
        self._icon = icon

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Seplos BMS HA - {self._name}"
        
    @property
    def unique_id(self):
        """Return a unique ID for this entity."""
        return f"sep_bms_ha_{self._name}"
        
    @property
    def state(self):
        """Return the state of the sensor."""
        # If the coordinator's data is a tuple, access both telemetry and alarms data
        if isinstance(self.coordinator.data, tuple):
            telemetry_data, alarms_data = self.coordinator.data
            # First, try to get the value from the telemetry data
            value = self.get_value(telemetry_data)
            if value is not None:
                _LOGGER.debug("For sensor %s, attribute %s has value (from telemetry): %s", self._name, self._attribute, value)
                return value
            # If the value is None, then try to get it from the alarms data
            value = self.get_value(alarms_data)
            _LOGGER.debug("For sensor %s, attribute %s has value (from alarms): %s", self._name, self._attribute, value)
            return value
        else:
            value = self.get_value(self.coordinator.data)
            _LOGGER.debug("For sensor %s, attribute %s has value: %s", self._name, self._attribute, value)
            return value



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
                    if attr in self.ALARM_ATTRIBUTES and value == 0:
                        _LOGGER.debug("Converting 0 to 'No Alarm' for attribute %s", attr)  # Debug line
                        return "No Alarm"
                    return value
        else:
            value = getattr(telemetry_data, self._attribute, None)
            if self._attribute in self.ALARM_ATTRIBUTES and value == 0:
                _LOGGER.debug("Converting 0 to 'No Alarm' for attribute %s", self._attribute)  # Debug line
                return "No Alarm"
            return value
            
    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Seplos BMS sensor platform."""

    port = entry.data.get("usb_port")  # Get port from the config entry

    async def async_update_data():
        """Fetch data from Seplos BMS."""
        response2 = await hass.async_add_executor_job(send_serial_command, COMMAND_2, port)
        _LOGGER.debug("Raw response2: %s", response2)
        
        # Removing the tilde prefix and extracting teledata information.
        teledata_data_str = response2
        alarms = extract_data_from_message(teledata_data_str, False, True, True)
        _LOGGER.debug("Raw alarms2: %s", alarms)

        response1 = await hass.async_add_executor_job(send_serial_command, COMMAND_1, port)
        _LOGGER.debug("Raw response1: %s", response1)
        
        # Removing the tilde prefix and extracting telemetry information.
        telemetry_data_str = response1
        telemetry = extract_data_from_message(telemetry_data_str, True, False, True)
        _LOGGER.debug("Raw telemetry1: %s", telemetry)

        # This assumes that the Telemetry class has been updated to accept alarms or you have another mechanism
        # to manage both telemetry and alarms.
        # telemetry.alarms = alarms
        _LOGGER.debug("Telemetry data: %s", str(telemetry[0]))
        _LOGGER.debug("Alarms data: %s", str(alarms[1]))

        return telemetry[0], alarms[1] # Returns the telemetry, if alarms are needed to be included, adjust accordingly.


    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="seplos_bms_sensor",
        update_method=async_update_data,
        update_interval=timedelta(seconds=10),  # Define how often to fetch data
    )


    await coordinator.async_refresh()  # Fetch data once before adding entities

    # First, for the cellVoltage and temperatures, we'll iterate over their length to create individual sensors:

    cell_voltage_sensors = [SeplosBMSSensorBase(coordinator, port, f"cellVoltage[{idx}]", f"Cell Voltage {idx+1}", "V") for idx in range(16)]
    cell_voltage_sensors = [SeplosBMSSensorBase(coordinator, port, f"cellVoltage[{idx}]", f"Cell Voltage {idx+1}", "V") for idx in range(16)]
    temperature_sensors = [SeplosBMSSensorBase(coordinator, port, f"temperatures[{idx}]", f"Temperature {idx+1}", "°C") for idx in range(6)]
    cell_alarm_sensors = [SeplosBMSSensorBase(coordinator, port, f"cellAlarm[{idx}]", f"Cell Alarm {idx+1}", "") for idx in range(16)]
    temp_alarm_sensors = [SeplosBMSSensorBase(coordinator, port, f"tempAlarm[{idx}]", f"Temperature Alarm {idx+1}", "") for idx in range(6)]

    # Now let's create the rest of the sensors:

    general_sensors = [
        SeplosBMSSensorBase(coordinator, port, "current", "Current", "A"),
        SeplosBMSSensorBase(coordinator, port, "voltage", "Voltage", "V"),
        SeplosBMSSensorBase(coordinator, port, "cellsCount", "Cell Count", ""),
        SeplosBMSSensorBase(coordinator, port, "tempCount", "Temperature Count", ""),
        SeplosBMSSensorBase(coordinator, port, "resCap", "Residual Capacity", "Ah"),
        SeplosBMSSensorBase(coordinator, port, "customNumber", "Custom Number", ""),
        SeplosBMSSensorBase(coordinator, port, "capacity", "Capacity", "Ah"),
        SeplosBMSSensorBase(coordinator, port, "soc", "State of Charge", "%"),
        SeplosBMSSensorBase(coordinator, port, "ratedCapacity", "Rated Capacity", "Ah"),
        SeplosBMSSensorBase(coordinator, port, "cycles", "Cycles", ""),
        SeplosBMSSensorBase(coordinator, port, "soh", "State of Health", "%"),
        SeplosBMSSensorBase(coordinator, port, "portVoltage", "Port Voltage", "V"),
        SeplosBMSSensorBase(coordinator, port, "currentAlarm", "Current Alarm", ""),
        SeplosBMSSensorBase(coordinator, port, "voltageAlarm", "Voltage Alarm", ""),
        SeplosBMSSensorBase(coordinator, port, "customAlarms", "Custom Alarms", ""),
        SeplosBMSSensorBase(coordinator, port, "alarmEvent0", "Alarm Event 0", ""),
        SeplosBMSSensorBase(coordinator, port, "alarmEvent1", "Alarm Event 1", ""),
        SeplosBMSSensorBase(coordinator, port, "alarmEvent2", "Alarm Event 2", ""),
        SeplosBMSSensorBase(coordinator, port, "alarmEvent3", "Alarm Event 3", ""),
        SeplosBMSSensorBase(coordinator, port, "alarmEvent4", "Alarm Event 4", ""),
        SeplosBMSSensorBase(coordinator, port, "alarmEvent5", "Alarm Event 5", ""),
        SeplosBMSSensorBase(coordinator, port, "alarmEvent6", "Alarm Event 6", ""),
        SeplosBMSSensorBase(coordinator, port, "alarmEvent7", "Alarm Event 7", ""),
        SeplosBMSSensorBase(coordinator, port, "onOffState", "On/Off State", ""),
        SeplosBMSSensorBase(coordinator, port, "equilibriumState0", "Equilibrium State 0", ""),
        SeplosBMSSensorBase(coordinator, port, "equilibriumState1", "Equilibrium State 1", ""),
        SeplosBMSSensorBase(coordinator, port, "systemState", "System State", ""),
        SeplosBMSSensorBase(coordinator, port, "disconnectionState0", "Disconnection State 0", ""),
        SeplosBMSSensorBase(coordinator, port, "disconnectionState1", "Disconnection State 1", ""),
    ]

    # Now, let's combine all the sensors into one list:

    sensors = cell_voltage_sensors + temperature_sensors + cell_alarm_sensors + temp_alarm_sensors + general_sensors


    async_add_entities(sensors, True)


