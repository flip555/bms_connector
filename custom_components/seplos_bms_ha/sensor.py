from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .serial_comms import send_serial_command
from .seplos_helper import extract_data_from_message
import asyncio
import logging
from datetime import timedelta
from .const import (
    LOGGER,
    NAME,
    DOMAIN,
    VERSION,
    ATTRIBUTION,
    ALARM_ATTRIBUTES,
    ALARM_MAPPINGS
)
from .v2_calc_functions import (
    battery_watts,
    remaining_watts,
    capacity_watts,
    full_charge_amps,
    full_charge_watts,
    get_cell_extremes_and_difference,
    highest_cell_voltage,
    lowest_cell_voltage,
    cell_voltage_difference,
    highest_cell_number,
    lowest_cell_number,
    highest_temp,
    lowest_temp,
    delta_temp,
    highest_temp_sensor,
    lowest_temp_sensor,
)

_LOGGER = logging.getLogger(__name__)

# Define your two commands to be sent
COMMAND_1 = "~20004642E00200FD37\r"
COMMAND_2 = "~20004644E00200FD35\r"

class SeplosBMSSensorBase(CoordinatorEntity):
    def interpret_alarm(self, event, value):
        flags = ALARM_MAPPINGS.get(event, [])

        if not flags:
            return f"Unknown event: {event}"

        # Special handling for temperatureAlarm
        if event.startswith("tempAlarm"):
            return ALARM_MAPPINGS["tempAlarm"].get(value, "Unknown value")
 
        # Special handling for cellAlarm
        if event.startswith("cellAlarm"):
            return ALARM_MAPPINGS["cellAlarm"].get(value, "Unknown value")

        if event == "alarmEvent0":
            return flags[value] if 0 <= value < len(flags) else "Unknown value"

        # For other alarm events, interpret them as bit flags
        triggered_alarms = [flag for idx, flag in enumerate(flags) if value & (1 << idx)]

        return ', '.join(triggered_alarms) if triggered_alarms else "No Alarm"
   
    def __init__(self, coordinator, port, attribute, name, unit=None, icon=None, battery_address=None):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._port = port
        self._attribute = attribute
        self._name = name
        self._unit = unit
        self._icon = icon
        self._battery_address = battery_address

    @property
    def name(self):
        """Return the name of the sensor."""
        prefix = f"Seplos BMS HA {self._battery_address} -" if self._battery_address else "Seplos BMS HA -"
        return f"{prefix} {self._name}"
        
    @property
    def unique_id(self):
        """Return a unique ID for this entity."""
        prefix = f"sep_bms_ha_{self._battery_address}_" if self._battery_address else "sep_bms_ha_"
        return f"{prefix}{self._name}"


    @property
    def state(self):
        """Return the state of the sensor."""
        if not self._attribute:  # Check if attribute is None or empty
            return super().state

        base_attribute = self._attribute.split('[')[0] if '[' in self._attribute else self._attribute

        value = None
        if isinstance(self.coordinator.data, tuple):
            telemetry_data, alarms_data, battery_address_1_data, battery_address_2_data = self.coordinator.data
            value = self.get_value(telemetry_data) or self.get_value(alarms_data)
        else:
            value = self.get_value(self.coordinator.data)

        if value is None or value == '':
            _LOGGER.warning("No data found in telemetry or alarms for %s", self._name)
            return None

        # Handle the "Current" sensor specifically
        if base_attribute == "current":
            _LOGGER.debug("Current Selected: %s", value)

            try:
                # Check if value is None or an empty string
                if value is None or value == '':
                    _LOGGER.debug("Value is None or empty string")
                    return "0"

                # Attempt to convert the value to a float
                float_value = float(value)

                # Check if the float value is close to zero (e.g., within 0.01)
                if abs(float_value) < 0.01:
                    _LOGGER.debug("Float value is very close to zero: %s", float_value)
                    return "0"
                elif float_value == 0.0:
                    _LOGGER.debug("Float value is exactly zero: %s", float_value)
                    return "0"
                else:
                    _LOGGER.debug("Float value is not zero: %s", float_value)
                    return str(float_value)
            except ValueError:
                _LOGGER.debug("Error converting value to float")
                pass  # If conversion to float fails, continue as before

        # Interpret the value for alarm sensors
        if base_attribute in ALARM_ATTRIBUTES:
            return str(self.interpret_alarm(base_attribute, value))

        return value






    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        if self._attribute in ALARM_ATTRIBUTES:
            return None  # No unit for alarms
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

async def async_setup_entry(hass, entry, async_add_entities):
    class DerivedSeplosBMSSensor(SeplosBMSSensorBase):
        def __init__(self, *args, **kwargs):
            self._calc_function = kwargs.pop("calc_function", None)
            super().__init__(*args, **kwargs)

        @property
        def state(self):
            if self._calc_function:
                result = self._calc_function(self.coordinator.data)
                _LOGGER.debug("Derived sensor '%s' calculated value: %s", self._name, result)
                return result
            return super().state
            
    port = entry.data.get("usb_port")  # Get port from the config entry

    async def async_update_data():
        # Loop for multiple battery packs should start here using TELEMETRY_COMMANDS from const.py 0-15 as COMMAND_1
        telemetry_data_str = await hass.async_add_executor_job(send_serial_command, COMMAND_1, port)
        telemetry, _, battery_address_1 = extract_data_from_message(telemetry_data_str, True, False, True)

        # Loop for multiple battery packs should use TELEDATA_CODES from const.py 0-15 as COMMAND_2
        teledata_data_str = await hass.async_add_executor_job(send_serial_command, COMMAND_2, port)
        _, alarms, battery_address_2 = extract_data_from_message(teledata_data_str, False, True, True)

        return telemetry, alarms, battery_address_1, battery_address_2

    telemetry, alarms, battery_address, battery_address_2 = await async_update_data()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="seplos_bms_sensor",
        update_method=async_update_data,
        update_interval=timedelta(seconds=5),  # Define how often to fetch data
    )

    await coordinator.async_refresh() 

    all_sensors = (
        [SeplosBMSSensorBase(coordinator, port, f"cellVoltage[{idx}]", f"Cell Voltage {idx+1}", "mV", battery_address=battery_address) for idx in range(16)] +
        [SeplosBMSSensorBase(coordinator, port, f"temperatures[{idx}]", f"Cell Temperature {idx+1}", "°C", battery_address=battery_address) for idx in range(4)] +
        [SeplosBMSSensorBase(coordinator, port, f"cellAlarm[{idx}]", f"Cell Alarm {idx+1}", unit=None, battery_address=battery_address) for idx in range(16)] +
        [SeplosBMSSensorBase(coordinator, port, f"tempAlarm[{idx}]", f"Temperature Alarm {idx+1}", unit=None, battery_address=battery_address) for idx in range(4)] +
        [
            SeplosBMSSensorBase(coordinator, port, "temperatures[4]", "Environment Temperature", "°C", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "temperatures[5]", "Power Temperature", "°C", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "current", "Current", "A", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "voltage", "Voltage", "V", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "cellsCount", "Cell Count", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "tempCount", "Temperature Count", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "resCap", "Residual Capacity", "Ah", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "capacity", "Capacity", "Ah", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "soc", "State of Charge", "%", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "ratedCapacity", "Rated Capacity", "Ah", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "cycles", "Cycles", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "soh", "State of Health", "%", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "portVoltage", "Port Voltage", "V", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "currentAlarm", "Current Alarm", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "voltageAlarm", "Voltage Alarm", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "alarmEvent0", "Alarm Event 0", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "alarmEvent1", "Alarm Event 1", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "alarmEvent2", "Alarm Event 2", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "alarmEvent3", "Alarm Event 3", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "alarmEvent4", "Alarm Event 4", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "alarmEvent5", "Alarm Event 5", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "alarmEvent6", "Alarm Event 6", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "alarmEvent7", "Alarm Event 7", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "onOffState", "On/Off State", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "equilibriumState0", "Equilibrium State 0", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "equilibriumState1", "Equilibrium State 1", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "systemState", "System State", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "disconnectionState0", "Disconnection State 0", "", battery_address=battery_address),
            SeplosBMSSensorBase(coordinator, port, "disconnectionState1", "Disconnection State 1", "", battery_address=battery_address),
        ]
    )

    # Add the derived sensors
    derived_sensors = [
        DerivedSeplosBMSSensor(coordinator, port, None, "Battery Watts", "W", calc_function=battery_watts, battery_address=battery_address),
        DerivedSeplosBMSSensor(coordinator, port, None, "Remaining Watts", "W", calc_function=remaining_watts, battery_address=battery_address),
        DerivedSeplosBMSSensor(coordinator, port, None, "Capacity - Watts", "W", calc_function=capacity_watts, battery_address=battery_address),
        DerivedSeplosBMSSensor(coordinator, port, None, "Full Charge - Amps", "Ah", calc_function=full_charge_amps, battery_address=battery_address),
        DerivedSeplosBMSSensor(coordinator, port, None, "Full Charge - Watts", "W", calc_function=full_charge_watts, battery_address=battery_address),
        DerivedSeplosBMSSensor(coordinator, port, None, "Highest Cell Voltage", "mV", calc_function=highest_cell_voltage, battery_address=battery_address),
        DerivedSeplosBMSSensor(coordinator, port, None, "Lowest Cell Voltage", "mV", calc_function=lowest_cell_voltage, battery_address=battery_address),
        DerivedSeplosBMSSensor(coordinator, port, None, "Cell Voltage Difference", "mV", calc_function=cell_voltage_difference, battery_address=battery_address),
        DerivedSeplosBMSSensor(coordinator, port, None, "Cell Number of Highest Voltage", "", calc_function=highest_cell_number, battery_address=battery_address),
        DerivedSeplosBMSSensor(coordinator, port, None, "Cell Number of Lowest Voltage", "", calc_function=lowest_cell_number, battery_address=battery_address)
    ]

    # Combine all sensor lists
    sensors = all_sensors + derived_sensors

    async_add_entities(sensors, True)