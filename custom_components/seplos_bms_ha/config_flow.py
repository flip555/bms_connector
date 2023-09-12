from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries, exceptions
from .const import DOMAIN, LOGGER
import serial.tools.list_ports
import serial

class SeplosBMSFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def is_valid_port(self, port: str) -> bool:
        """Validate if the provided port exists and has permissions."""
        try:
            with serial.Serial(port, baudrate=9600, timeout=1):
                return True
        except (OSError, serial.SerialException):
            return False

    async def async_step_user(self, user_input: dict | None = None) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}

        if user_input is not None:
            custom_port = user_input.get("usb_port")
            if not self.is_valid_port(custom_port):
                _errors["usb_port"] = "invalid_port"
            else:
                battery_pack = user_input.get("battery_pack")
                if await self.async_batterypack_exists(battery_pack):
                    _errors["battery_pack"] = "duplicate_battery_pack"
                else:
                    title = f"Seplos BMS - {user_input['bms_version']} - {user_input['battery_pack']} ({user_input['usb_port']})"
                    return self.async_create_entry(title=title, data=user_input)

        # Enumerate available USB ports dynamically
        usb_ports = [(port.device, port.description) for port in serial.tools.list_ports.comports()]

        data_schema = vol.Schema({
            vol.Required("usb_port", description="USB Port (e.g., /dev/ttyUSB0)", default="/dev/ttyUSB0"): str,
            vol.Required("battery_pack", description="Battery Pack (e.g., 0x00)", default="0x00"): str,
            vol.Optional("bms_version", description="BMS Version (Coming Soon)", default="V2"): vol.In(["V2", "V3 (Coming Soon)"]),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=_errors,
        )

    async def async_batterypack_exists(self, battery_pack: str):
        """Check if sensors with the specified battery pack ID already exist."""
        entities = await self.hass.async_add_executor_job(lambda: self.hass.states.async_entity_ids("sensor"))
        for entity_id in entities:
            entity = self.hass.states.get(entity_id)
            if entity and entity.attributes.get("unique_id") == f"battery_pack_{battery_pack}":
                return True
        return False
