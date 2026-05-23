from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.entity import DeviceInfo

from .data_parser import extract_data_from_message
from ....connector import get_serial_send_function
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
from .calc_functions import (
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
    balancer_cell_1,
    balancer_cell_2,
    balancer_cell_3,
    balancer_cell_4,
    balancer_cell_5,
    balancer_cell_6,
    balancer_cell_7,
    balancer_cell_8,
    balancer_cell_9,
    balancer_cell_10,
    balancer_cell_11,
    balancer_cell_12,
    balancer_cell_13,
    balancer_cell_14,
    balancer_cell_15,
    balancer_cell_16

)

_LOGGER = logging.getLogger(__name__)

# Define the generate_sensors function
async def generate_sensors(hass, bms_type, connector_info, config_battery_address, sensor_prefix, entry_id, async_add_entities, poll_interval=10):
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
            
        @property
        def unit_of_measurement(self):
            if self._calc_function:
                result = self._calc_function(self.coordinator.data)
                if isinstance(result, bool):
                    return None  # No unit for boolean states
                else:
                    return ''
        
    async def async_update_data():
        #Need to generate these, they're all for 0x00 atm .... 42H, 44H, 47H, 51H
        V2_COMMAND_ARRAY = {
            "0x00": ["~20004642E00200FD37\r", "~20004644E00200FD35\r", "~20004647E00200FD32\r", "~20004651E00200FD37\r"],
            "0x01": ["~20004642E00215FD31\r", "~20004644E00200FD35\r", "~20004647E00200FD32\r", "~20004651E00200FD37\r"],
            "0x02": ["~20004642E00200FD37\r", "~20004644E00200FD35\r", "~20004647E00200FD32\r", "~20004651E00200FD37\r"],
            "0x03": ["~20004642E00200FD37\r", "~20004644E00200FD35\r", "~20004647E00200FD32\r", "~20004651E00200FD37\r"],
        }
        _LOGGER.debug("BATTERY PACK SELECTED: %s", config_battery_address)
        commands = V2_COMMAND_ARRAY[config_battery_address]

        send_func = get_serial_send_function(connector_info)
        telemetry_data_str = await hass.async_add_executor_job(send_func, commands)
        battery_address, telemetry, alarms, system_details, protection_settings = extract_data_from_message(telemetry_data_str, True, True, True)
        if battery_address != config_battery_address: 
            _LOGGER.debug("Battery Pack: %s was not found. %s found instead. Skipping", config_battery_address, battery_address)
            pass
        else:
            return battery_address, telemetry, alarms, system_details, protection_settings

    battery_address, telemetry, alarms, system_details, protection_settings = await async_update_data()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="seplos_bms_sensor",
        update_method=async_update_data,
        update_interval=timedelta(seconds=poll_interval),
    )
    _LOGGER.debug("async_refresh data generate_sensors called")
    await coordinator.async_refresh() 

    all_sensors = (
        [SeplosBMSSensorBase(coordinator, connector_info, f"cellVoltage[{idx}]", f"Cell Voltage {idx+1}", "mV", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id) for idx in range(16)] +
        [SeplosBMSSensorBase(coordinator, connector_info, f"temperatures[{idx}]", f"Cell Temperature {idx+1}", "°C", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id) for idx in range(4)] +
        [SeplosBMSSensorBase(coordinator, connector_info, f"cellAlarm[{idx}]", f"Cell Alarm {idx+1}", unit=None, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id) for idx in range(16)] +
        [SeplosBMSSensorBase(coordinator, connector_info, f"tempAlarm[{idx}]", f"Temperature Alarm {idx+1}", unit=None, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id) for idx in range(4)] +
        [
            SeplosBMSSensorBase(coordinator, connector_info, "temperatures[4]", "Environment Temperature", "°C", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "temperatures[5]", "Power Temperature", "°C", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "current", "Current", "A", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "voltage", "Voltage", "V", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "cellsCount", "Cell Count", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "tempCount", "Temperature Count", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "resCap", "Residual Capacity", "Ah", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "capacity", "Capacity", "Ah", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "soc", "State of Charge", "%", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "ratedCapacity", "Rated Capacity", "Ah", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "cycles", "Cycles", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "soh", "State of Health", "%", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "portVoltage", "Port Voltage", "V", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "currentAlarm", "Current Alarm", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "voltageAlarm", "Voltage Alarm", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "alarmEvent1", "Alarm Event 1", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "alarmEvent2", "Alarm Event 2", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "alarmEvent3", "Alarm Event 3", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "alarmEvent4", "Alarm Event 4", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "alarmEvent5", "Alarm Event 5", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "alarmEvent6", "Alarm Event 6", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "alarmEvent7", "Alarm Event 7", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "alarmEvent8", "Alarm Event 8", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "onOffState", "On/Off State", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "equilibriumState0", "Equilibrium State 0", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "equilibriumState1", "Equilibrium State 1", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "systemState", "System State", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "disconnectionState0", "Disconnection State 0", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "disconnectionState1", "Disconnection State 1", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "device_name", "BMS Name", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "software_version", "BMS Software Version", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
            SeplosBMSSensorBase(coordinator, connector_info, "manufacturer_name", "Inverter Manufacturer", "", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),

        ]
    )
    setting_sensors = [
        SeplosBMSSensorBase(coordinator, connector_info, "soc_ah", "SOC", "Ah", "mdi:gauge", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "monomer_high_voltage_alarm", "Monomer High Voltage Alarm", "mV", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "overcurrent_delay_recovery", "Overcurrent Delay Recovery", "s", "mdi:timer-sand", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "total_voltage_overvoltage_protection", "Total Voltage Overvoltage Protection", "mV", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "equalization_opening_voltage", "Equalization Opening Voltage", "mV", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "monomer_undervoltage_recovery", "Monomer Undervoltage Recovery", "mV", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "monomer_low_pressure_recovery", "Monomer Low Pressure Recovery", "mV", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "monomer_overvoltage_protection", "Monomer Overvoltage Protection", "mV", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "monomer_overvoltage_recovery", "Monomer Overvoltage Recovery", "mV", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "monomer_undervoltage_protection", "Monomer Undervoltage Protection", "mV", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "monomer_low_pressure_alarm", "Monomer Low Pressure Alarm", "mV", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "monomer_high_pressure_recovery", "Monomer High Pressure Recovery", "mV", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "battery_low_voltage_forbidden_charging", "Battery Low Voltage Forbidden Charging", "mV", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "total_pressure_high_pressure_alarm", "Total Pressure High Pressure Alarm", "V", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "total_pressure_high_pressure_recovery", "Total Pressure and High Pressure Recovery", "V", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "total_pressure_low_pressure_alarm", "Total Pressure Low Pressure Alarm", "V", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "total_pressure_low_pressure_recovery", "Total Pressure and Low Pressure Recovery", "V", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "total_voltage_overvoltage_protection", "Total Voltage Overvoltage Protection", "V", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "total_pressure_overpressure_recovery", "Total Pressure Overpressure Recovery", "V", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "total_voltage_undervoltage_protection", "Total Voltage Undervoltage Protection", "V", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "total_pressure_undervoltage_recovery", "Total Pressure Undervoltage Recovery", "V", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charging_overvoltage_protection", "Charging Overvoltage Protection", "V", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charging_overvoltage_recovery", "Charging Overvoltage Recovery", "V", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charging_high_temperature_warning", "Charging High Temperature Warning", "°C", "mdi:thermometer-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charging_high_temperature_recovery", "Charging High Temperature Recovery", "°C", "mdi:thermometer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charging_low_temperature_warning", "Charging Low Temperature Warning", "°C", "mdi:thermometer-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charging_low_temperature_recovery", "Charging Low Temperature Recovery", "°C", "mdi:thermometer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charging_over_temperature_protection", "Charging Over Temperature Protection", "°C", "mdi:thermometer-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charging_over_temperature_recovery", "Charging Over Temperature Recovery", "°C", "mdi:thermometer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charging_under_temperature_protection", "Charging Under Temperature Protection", "°C", "mdi:thermometer-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charging_under_temperature_recovery", "Charging Under Temperature Recovery", "°C", "mdi:thermometer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "discharge_high_temperature_warning", "Discharge High Temperature Warning", "°C", "mdi:thermometer-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "discharge_high_temperature_recovery", "Discharge High Temperature Recovery", "°C", "mdi:thermometer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "discharge_low_temperature_warning", "Discharge Low Temperature Warning", "°C", "mdi:thermometer-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "discharge_low_temperature_recovery", "Discharge Low Temperature Recovery", "°C", "mdi:thermometer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "discharge_over_temperature_protection", "Discharge Over Temperature Protection", "°C", "mdi:thermometer-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "discharge_over_temperature_recovery", "Discharge Over Temperature Recovery", "°C", "mdi:thermometer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "discharge_under_temperature_protection", "Discharge Under Temperature Protection", "°C", "mdi:thermometer-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "discharge_under_temperature_recovery", "Discharge Under Temperature Recovery", "°C", "mdi:thermometer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "cell_low_temperature_heating", "Cell Low Temperature Heating", "°C", "mdi:thermometer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "cell_heating_recovery", "Cell Heating Recovery", "°C", "mdi:thermometer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "ambient_high_temperature_alarm", "Ambient High Temperature Alarm", "°C", "mdi:thermometer-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "ambient_high_temperature_recovery", "Ambient High Temperature Recovery", "°C", "mdi:thermometer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "ambient_low_temperature_alarm", "Ambient Low Temperature Warning", "°C", "mdi:thermometer-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "ambient_low_temperature_recovery", "Ambient Low Temperature Recovery", "°C", "mdi:thermometer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "power_high_temperature_recovery", "Power High Temperature Recovery", "°C", "mdi:thermometer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "power_over_temperature_protection", "Power Over Temperature Protection", "°C", "mdi:thermometer-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "power_over_temperature_recovery", "Power Over Temperature Recovery", "°C", "mdi:thermometer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charging_overcurrent_warning", "Charging Overcurrent Warning", "A", "mdi:current-ac", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charging_overcurrent_recovery", "Charging Overcurrent Recovery", "A", "mdi:current-ac", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "discharge_overcurrent_warning", "Discharge Overcurrent Warning", "A", "mdi:current-dc", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "discharge_overcurrent_recovery", "Discharge Overcurrent Recovery", "A", "mdi:current-dc", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charge_overcurrent_protection", "Charge Overcurrent Protection", "A", "mdi:current-ac", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "discharge_overcurrent_protection", "Discharge Overcurrent Protection", "A", "mdi:current-dc", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "transient_overcurrent_protection", "Transient Overcurrent Protection", "A", "mdi:flash-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "output_soft_start_delay", "Output Soft Start Delay", "ms", "mdi:timer-sand", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "battery_rated_capacity", "Battery Rated Capacity", "Ah", "mdi:flash-circle", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "cell_invalidation_differential_pressure", "Cell Invalidation Differential Pressure", "V", "mdi:flash-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "cell_invalidation_recovery", "Cell Invalidation Recovery", "V", "mdi:flash", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "equalization_opening_pressure_difference", "Equalization Opening Pressure Difference", "V", "mdi:flash-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "equalization_closing_pressure_difference", "Equalization Closing Pressure Difference", "V", "mdi:flash-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "static_equilibrium_time", "Static Equilibrium Time", "When", "mdi:timer-sand", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "battery_number_in_series", "Battery Number in Series", "String", "mdi:battery", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charge_overcurrent_delay", "Charge Overcurrent Delay", "S", "mdi:timer-sand", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "discharge_overcurrent_delay", "Discharge Overcurrent Delay", "S", "mdi:timer-sand", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "transient_overcurrent_delay", "Transient Overcurrent Delay", "ms", "mdi:timer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "overcurrent_recovery_times", "Overcurrent Delay Recovery Times", "times", "mdi:timer-sand", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charge_current_limit_delay", "Charge Current Limit Delay", "Minutes", "mdi:timer-sand", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charge_activation_delay", "Charge Activation Delay", "Minutes", "mdi:timer-sand", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charging_activation_interval", "Charging Activation Interval", "When", "mdi:timer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "charge_activation_times", "Charge Activation Times", "times", "mdi:timer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "work_record_interval", "Work Record Interval", "Minutes", "mdi:timer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "standby_recording_interval", "Standby Recording Interval", "Minutes", "mdi:timer", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "standby_shutdown_delay", "Standby Shutdown Delay", "When", "mdi:timer-sand", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "remaining_capacity_alarm", "Remaining Capacity Alarm", "%", "mdi:flash-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "remaining_capacity_protection", "Remaining Capacity Protection", "%", "mdi:flash-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "interval_charge_capacity", "Interval Charge Capacity", "%", "mdi:flash", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "cycle_cumulative_capacity", "Cycle Cumulative Capacity", "%", "mdi:flash", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "connection_fault_impedance", "Connection Fault Impedance", "mΩ", "mdi:flash-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "compensation_point_1_position", "Compensation Point 1 Position", "String", "mdi:flash", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "compensation_point_1_impedance", "Compensation Point 1 Impedance", "mΩ", "mdi:flash-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "compensation_point_2_position", "Compensation Point 2 Position", "String", "mdi:flash", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
        SeplosBMSSensorBase(coordinator, connector_info, "compensation_point_2_impedance", "Compensation Point 2 Impedance", "mΩ", "mdi:flash-alert", battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id, is_settings=True),
    ]


    # Add the derived sensors
    derived_sensors = [
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Battery Watts", "W", calc_function=battery_watts, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Remaining Watts", "W", calc_function=remaining_watts, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Capacity - Watts", "W", calc_function=capacity_watts, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Full Charge - Amps", "Ah", calc_function=full_charge_amps, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Full Charge - Watts", "W", calc_function=full_charge_watts, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Highest Cell Voltage", "mV", calc_function=highest_cell_voltage, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Lowest Cell Voltage", "mV", calc_function=lowest_cell_voltage, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Cell Voltage Difference", "mV", calc_function=cell_voltage_difference, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Cell Number of Highest Voltage", "", calc_function=highest_cell_number, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Cell Number of Lowest Voltage", "", calc_function=lowest_cell_number, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 1", "", calc_function=balancer_cell_1, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 2", "", calc_function=balancer_cell_2, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 3", "", calc_function=balancer_cell_3, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 4", "", calc_function=balancer_cell_4, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 5", "", calc_function=balancer_cell_5, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 6", "", calc_function=balancer_cell_6, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 7", "", calc_function=balancer_cell_7, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 8", "", calc_function=balancer_cell_8, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 9", "", calc_function=balancer_cell_9, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 10", "", calc_function=balancer_cell_10, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 11", "", calc_function=balancer_cell_11, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 12", "", calc_function=balancer_cell_12, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 13", "", calc_function=balancer_cell_13, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 14", "", calc_function=balancer_cell_14, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 15", "", calc_function=balancer_cell_15, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id),
        DerivedSeplosBMSSensor(coordinator, connector_info, None, "Balancer Active Cell 16", "", calc_function=balancer_cell_16, battery_address=battery_address, sensor_prefix=sensor_prefix, entry_id=entry_id)
    ]

    # Combine all sensor lists
    sensors = all_sensors + derived_sensors + setting_sensors

    async_add_entities(sensors, True)

class SeplosBMSSensorBase(CoordinatorEntity):
    def interpret_alarm(self, event, value):
        flags = ALARM_MAPPINGS.get(event, [])

        if not flags:
            return f"Unknown event: {event}"

        # For other alarm events, interpret them as bit flags
        triggered_alarms = [flag for idx, flag in enumerate(flags) if value is not None and value & (1 << idx)]
        #return ', '.join(str(triggered_alarms)) if triggered_alarms else "No Alarm"

        return ', '.join(str(alarm) for alarm in triggered_alarms) if triggered_alarms else "No Alarm"

    def __init__(self, coordinator, port, attribute, name, unit=None, icon=None, battery_address=None, sensor_prefix=None, entry_id=None, is_settings=False):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._port = port
        self._attribute = attribute
        self._name = name
        self._unit = unit
        self._icon = icon
        self._battery_address = battery_address
        self._sensor_prefix = sensor_prefix
        self._entry_id = entry_id
        self._is_settings = is_settings
        
        # Set device info — split BMS and Settings into separate devices like HEH
        if is_settings:
            self._attr_device_info = DeviceInfo(
                identifiers={("bms_connector", f"seplos_v2_{entry_id}_settings")},
                name=f"{sensor_prefix} Settings",
                manufacturer="Seplos",
                model="V2 Settings",
                sw_version="Unknown",
            )
        else:
            self._attr_device_info = DeviceInfo(
                identifiers={("bms_connector", f"seplos_v2_{entry_id}")},
                name=f"{sensor_prefix}",
                manufacturer="Seplos",
                model="V2 BMS",
                sw_version="Unknown",
            )

    @property
    def name(self):
        """Return the name of the sensor."""
        prefix = f"{self._sensor_prefix} - {self._battery_address} -"
        return f"{prefix} {self._name}"
        
    @property
    def unique_id(self):
        """Return a stable unique ID for this entity."""
        return f"bms_connector_v2_{self._entry_id}_{self._name}"

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
            
        # Interpret the value for alarm sensors
        if base_attribute in ALARM_ATTRIBUTES:
            interpreted_value = str(self.interpret_alarm(base_attribute, value))
            _LOGGER.debug("Interpreted value for %s: %s", base_attribute, interpreted_value)
            return interpreted_value   
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
        if self._attribute in ALARM_ATTRIBUTES:
            return None  # No unit for alarms
        if self._attribute in SYSTEM_ATTRIBUTES:
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