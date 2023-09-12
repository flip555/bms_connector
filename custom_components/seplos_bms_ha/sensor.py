from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .seplos_helper import send_serial_command, extract_data_from_message, Telemetry, Alarms, parse_telemetry_info, parse_teledata_info
import asyncio
import logging
import time

from datetime import timedelta

_LOGGER = logging.getLogger(__name__)

from .const import DOMAIN
from .seplos_helper import send_serial_command, extract_data_from_message

# Define your two commands to be sent
COMMAND_1 = "~20004642E00200FD37\r"
COMMAND_2 = "~20004644E00200FD35\r"



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
            value = self.get_value(telemetry_data)
            
            if value is None or value == '':
                value = self.get_value(alarms_data)

        else:
            value = self.get_value(self.coordinator.data)
        
        if value is None or value == '':
            _LOGGER.warning("No data found in telemetry or alarms for %s", self._name)
            return None

        # Interpret the value for alarm sensors
        if base_attribute in self.ALARM_ATTRIBUTES:
            return str(self.interpret_alarm(base_attribute, value))
        
        return value


    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        if self._attribute in self.ALARM_ATTRIBUTES:
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
    """Set up the Seplos BMS sensor platform."""

    port = entry.data.get("usb_port")  # Get port from the config entry

    async def async_update_data():
        """Fetch data from Seplos BMS."""
        response1 = await hass.async_add_executor_job(send_serial_command, COMMAND_1, port)
        telemetry_data_str = response1
        telemetry, _, battery_address_1 = extract_data_from_message(telemetry_data_str, True, False, True)
        teledata_data_str = await hass.async_add_executor_job(send_serial_command, COMMAND_2, port)
        _, alarms, battery_address_2 = extract_data_from_message(teledata_data_str, False, True, True)
        return telemetry, alarms, battery_address_1, battery_address_2

    telemetry, alarms, battery_address_1, battery_address_2 = await async_update_data()


    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="seplos_bms_sensor",
        update_method=async_update_data,
        update_interval=timedelta(seconds=5),  # Define how often to fetch data
    )

    await coordinator.async_refresh()  # Fetch data once before adding entities


    # When creating sensor entities, pass the battery address (assuming telemetry's address is suitable for all)
    battery_address = battery_address_1

    cell_voltage_sensors = [SeplosBMSSensorBase(coordinator, port, f"cellVoltage[{idx}]", f"Cell Voltage {idx+1}", "mV", battery_address=battery_address) for idx in range(16)]
    temperature_sensors = [SeplosBMSSensorBase(coordinator, port, f"temperatures[{idx}]", f"Cell Temperature {idx+1}", "°C", battery_address=battery_address) for idx in range(4)]
    cell_alarm_sensors = [SeplosBMSSensorBase(coordinator, port, f"cellAlarm[{idx}]", f"Cell Alarm {idx+1}", unit=None, battery_address=battery_address) for idx in range(16)]
    temp_alarm_sensors = [SeplosBMSSensorBase(coordinator, port, f"tempAlarm[{idx}]", f"Temperature Alarm {idx+1}", unit=None, battery_address=battery_address) for idx in range(4)]

    # Now let's create the rest of the sensors:

    general_sensors = [
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
    
    await coordinator.async_refresh()  # Fetch data again before adding entities

    class DerivedSeplosBMSSensor(SeplosBMSSensorBase):
        """Derived class for sensors that are calculated from other sensors."""

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

            
    def battery_watts(data):
        telemetry, alarms, battery_address_1, battery_address_2 = data
        volts = getattr(telemetry, 'portVoltage', 0.0)
        amps = getattr(telemetry, 'current', 0.0)
        return volts * amps

    def remaining_watts(data):
        telemetry, alarms, battery_address_1, battery_address_2 = data
        volts = getattr(telemetry, 'voltage', 0.0)
        amps = getattr(telemetry, 'resCap', 0.0)
        return volts * amps

    def capacity_watts(data):
        telemetry, alarms, battery_address_1, battery_address_2 = data
        volts = getattr(telemetry, 'voltage', 0.0)
        amps = getattr(telemetry, 'capacity', 0.0)
        return volts * amps

    def full_charge_amps(data):
        telemetry, alarms, battery_address_1, battery_address_2 = data
        remaining = getattr(telemetry, 'resCap', 0.0)
        capacity = getattr(telemetry, 'capacity', 0.0)
        return capacity - remaining

    def full_charge_watts(data):
        telemetry, alarms, battery_address_1, battery_address_2 = data
        voltage = getattr(telemetry, 'voltage', 0.0)
        resCap = getattr(telemetry, 'resCap', 0.0)
        capacity = getattr(telemetry, 'capacity', 0.0)
        remaining_w = voltage * resCap
        cap_w = voltage * capacity
        return cap_w - remaining_w
    
    def get_cell_extremes_and_difference(data):
        telemetry, alarms, battery_address_1, battery_address_2 = data
        # Extract cell voltages into a list
        cell_voltages = getattr(telemetry, f"cellVoltage", 0.0)
        # Find the highest and lowest cell voltages and their indices
        highest_cell_voltage = max(cell_voltages)
        lowest_cell_voltage = min(cell_voltages)

        highest_cell_number = cell_voltages.index(highest_cell_voltage) + 1  # +1 because cells start from 1, not 0
        lowest_cell_number = cell_voltages.index(lowest_cell_voltage) + 1

        # Calculate the difference
        difference = highest_cell_voltage - lowest_cell_voltage

        return highest_cell_voltage, lowest_cell_voltage, difference, highest_cell_number, lowest_cell_number

    def highest_cell_voltage(data):
        telemetry, alarms, battery_address_1, battery_address_2 = data
        return get_cell_extremes_and_difference(data)[0]

    def lowest_cell_voltage(data):
        telemetry, alarms, battery_address_1, battery_address_2 = data
        return get_cell_extremes_and_difference(data)[1]

    def cell_voltage_difference(data):
        telemetry, alarms, battery_address_1, battery_address_2 = data
        return get_cell_extremes_and_difference(data)[2]

    def highest_cell_number(data):
        telemetry, alarms, battery_address_1, battery_address_2 = data
        return get_cell_extremes_and_difference(data)[3]

    def lowest_cell_number(data):
        telemetry, alarms, battery_address_1, battery_address_2 = data
        return get_cell_extremes_and_difference(data)[4]
        
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

    # Now, let's combine all the sensors into one list:
    sensors = cell_voltage_sensors + temperature_sensors + cell_alarm_sensors + temp_alarm_sensors + general_sensors + derived_sensors


    async_add_entities(sensors, True)





