from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, LOGGER

class SeplosBMSFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def is_valid_port(self, port: str) -> bool:
        """Validate if the provided port exists and has permissions."""
        # Validate if it's a valid /dev/ path or the longer /dev/serial/by-id/ path
        if port.startswith("/dev/ttyUSB") or port.startswith("/dev/serial/by-id/"):
            return True
        return False

    async def async_step_user(self, user_input: dict | None = None) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}

        # Predefined set of USB ports for the dropdown
        predefined_ports = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2", "/dev/ttyUSB3"]

        if user_input is not None:
            # If RS485-USB is selected, validate the USB port
            if user_input.get("source") == "RS485-USB":
                if not self.is_valid_port(user_input.get("usb_port")):
                    _errors["usb_port"] = "invalid_port"
                else:
                    return self.async_create_entry(title="Seplos BMS", data=user_input)

        data_schema = vol.Schema({
            vol.Required("source"): vol.In(["RS485-USB"]),
            vol.Optional("usb_port", default=predefined_ports[0] if predefined_ports else ""): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=_errors,
        )
