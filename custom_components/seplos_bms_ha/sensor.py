
            

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
    # Define the mappings for each alarm event
    ALARM_MAPPINGS = {
        "alarmEvent0": [
            "No Alarm", 
            "Alarm that analog quantity reaches the lower limit", 
            "Alarm that analog quantity reaches the upper limit", 
            "Other alarms"
        ],
        "alarmEvent1": [
            "Voltage sensor fault", 
            "Temperature sensor fault", 
            "Current sensor fault", 
            "Key switch fault", 
            "Cell voltage dropout fault", 
            "Charge switch fault", 
            "Discharge switch fault", 
            "Current limit switch fault"
        ],
        "alarmEvent2": [
            "Monomer high voltage alarm", 
            "Monomer overvoltage protection", 
            "Monomer low voltage alarm", 
            "Monomer under voltage protection", 
            "High voltage alarm for total voltage", 
            "Overvoltage protection for total voltage", 
            "Low voltage alarm for total voltage", 
            "Under voltage protection for total voltage"
        ],
        "alarmEvent3": [
            "Charge high temperature alarm", 
            "Charge over temperature protection", 
            "Charge low temperature alarm", 
            "Charge under temperature protection", 
            "Discharge high temperature alarm", 
            "Discharge over temperature protection", 
            "Discharge low temperature alarm", 
            "Discharge under temperature protection"
        ],
        "alarmEvent4": [
            "Environment high temperature alarm", 
            "Environment over temperature protection", 
            "Environment low temperature alarm", 
            "Environment under temperature protection", 
            "Power over temperature protection", 
            "Power high temperature alarm", 
            "Cell low temperature heating", 
            "Reservation bit"
        ],
        "alarmEvent5": [
            "Charge over current alarm", 
            "Charge over current protection", 
            "Discharge over current alarm", 
            "Discharge over current protection", 
            "Transient over current protection", 
            "Output short circuit protection", 
            "Transient over current lockout", 
            "Output short circuit lockout"
        ],
        "alarmEvent6": [
            "Charge high voltage protection", 
            "Intermittent recharge waiting", 
            "Residual capacity alarm", 
            "Residual capacity protection", 
            "Cell low voltage charging prohibition", 
            "Output reverse polarity protection", 
            "Output connection fault", 
            "Inside bit"
        ],
        "alarmEvent7": [
            "Inside bit", 
            "Inside bit", 
            "Inside bit", 
            "Inside bit", 
            "Automatic charging waiting", 
            "Manual charging waiting", 
            "Inside bit", 
            "Inside bit"
        ],
        "alarmEvent8": [
            "EEP storage fault", 
            "RTC error", 
            "Voltage calibration not performed", 
            "Current calibration not performed", 
            "Zero calibration not performed", 
            "Inside bit", 
            "Inside bit", 
            "Inside bit"
        ],
        "cellAlarm": {
            0: "No Alarm",
            1: "Alarm"
        },
        "tempAlarm": {
            0: "No Alarm",
            1: "Alarm"
        },
        "currentAlarm": {
            1: "Charge/Discharge Current Alarm"
        },
        "voltageAlarm": {
            1: "Total Battery Voltage Alarm"
        }
    }
    ALARM_MAPPINGS.update({
        "onOffState": [
            "Discharge switch state",
            "Charge switch state",
            "Current limit switch state",
            "Heating switch state",
            "Reservation bit",
            "Reservation bit",
            "Reservation bit",
            "Reservation bit"
        ],
        "equilibriumState0": [
            "Cell 01 equilibrium",
            "Cell 02 equilibrium",
            "Cell 03 equilibrium",
            "Cell 04 equilibrium",
            "Cell 05 equilibrium",
            "Cell 06 equilibrium",
            "Cell 07 equilibrium",
            "Cell 08 equilibrium"
        ],
        "equilibriumState1": [
            "Cell 09 equilibrium",
            "Cell 10 equilibrium",
            "Cell 11 equilibrium",
            "Cell 12 equilibrium",
            "Cell 13 equilibrium",
            "Cell 14 equilibrium",
            "Cell 15 equilibrium",
            "Cell 16 equilibrium"
        ],
        "systemState": [
            "Discharge",
            "Charge",
            "Floating charge",
            "Reservation bit",
            "Standby",
            "Shutdown",
            "Reservation bit",
            "Reservation bit"
        ],
        "disconnectionState0": [
            "Cell 01 disconnection",
            "Cell 02 disconnection",
            "Cell 03 disconnection",
            "Cell 04 disconnection",
            "Cell 05 disconnection",
            "Cell 06 disconnection",
            "Cell 07 disconnection",
            "Cell 08 disconnection"
        ],
        "disconnectionState1": [
            "Cell 09 disconnection",
            "Cell 10 disconnection",
            "Cell 11 disconnection",
            "Cell 12 disconnection",
            "Cell 13 disconnection",
            "Cell 14 disconnection",
            "Cell 15 disconnection",
            "Cell 16 disconnection"
        ]
    })

    def interpret_alarm(self, event, value):
        flags = self.ALARM_MAPPINGS.get(event, [])

        if not flags:
            return f"Unknown event: {event}"

        # Special handling for temperatureAlarm
        if event.startswith("tempAlarm"):
            return self.ALARM_MAPPINGS["tempAlarm"].get(value, "Unknown value")
 
        # Special handling for cellAlarm
        if event.startswith("cellAlarm"):
            return self.ALARM_MAPPINGS["cellAlarm"].get(value, "Unknown value")

        if event == "alarmEvent0":
            return flags[value] if 0 <= value < len(flags) else "Unknown value"

        # For other alarm events, interpret them as bit flags
        triggered_alarms = [flag for idx, flag in enumerate(flags) if value & (1 << idx)]

        return ', '.join(triggered_alarms) if triggered_alarms else "No Alarm"
   
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
        base_attribute = self._attribute.split('[')[0] if '[' in self._attribute else self._attribute

        if isinstance(self.coordinator.data, tuple):
            telemetry_data, alarms_data = self.coordinator.data
            value = self.get_value(telemetry_data)
            if value is not None and value is not '':
                _LOGGER.debug("Value from telemetry for %s: %s", self._name, value)
                if base_attribute in self.ALARM_ATTRIBUTES:
                    interpreted_value = self.interpret_alarm(base_attribute, value)
                    return interpreted_value
                return value
            value = self.get_value(alarms_data)
            if value is not None and value is not '':
                _LOGGER.debug("Value from alarms for %s: %s", self._name, value)
                if base_attribute in self.ALARM_ATTRIBUTES:
                    interpreted_value = self.interpret_alarm(base_attribute, value)
                    return interpreted_value
                return value
            _LOGGER.warning("No data found in telemetry or alarms for %s", self._name)
        else:
            value = self.get_value(self.coordinator.data)
            if value is not None and value is not '':
                _LOGGER.debug("Value from coordinator for %s: %s", self._name, value)
                if base_attribute in self.ALARM_ATTRIBUTES:
                    interpreted_value = self.interpret_alarm(base_attribute, value)
                    return interpreted_value
                return value
            _LOGGER.warning("No data found in coordinator for %s", self._name)

    
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
                    _LOGGER.debug("Returning list data value for %s[%d]: %s", attr, index, value)
                    return value
        else:
            value = getattr(telemetry_data, self._attribute, None)
            _LOGGER.debug("Returning attribute value for %s: %s", self._attribute, value)
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
        update_interval=timedelta(seconds=5),  # Define how often to fetch data
    )

    await coordinator.async_refresh()  # Fetch data once before adding entities

    # First, for the cellVoltage and temperatures, we'll iterate over their length to create individual sensors:

    cell_voltage_sensors = [SeplosBMSSensorBase(coordinator, port, f"cellVoltage[{idx}]", f"Cell Voltage {idx+1}", "mV") for idx in range(16)]
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


