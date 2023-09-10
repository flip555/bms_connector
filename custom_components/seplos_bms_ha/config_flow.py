"""Adds config flow for Seplos BMS."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, LOGGER

class SeplosBMSFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def is_valid_port(self, port: str) -> bool:
        """Validate if the provided port exists and has permissions."""
        # You can expand on this logic, e.g., by checking the file system or trying to open the port.
        if port.startswith("/dev/ttyUSB") and 0 <= int(port[-1]) <= 9:  # This checks if port ends with a single digit after "/dev/ttyUSB"
            return True
        return False
        
    async def async_step_user(self, user_input: dict | None = None) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}

        if user_input is not None:
            # If RS485-USB is selected, validate the USB port
            if user_input.get("source") == "RS485-USB":
                if not self.is_valid_port(user_input.get("usb_port")):
                    _errors["usb_port"] = "invalid_port"
                else:
                    return self.async_create_entry(title="Seplos BMS", data=user_input)

            # For ESPHome device, create an entry (assuming no validation needed)
            elif user_input.get("source") == "ESPHome device":
                return self.async_create_entry(title="Seplos BMS", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("source"): vol.In(["ESPHome device", "RS485-USB"]),
                vol.Optional("usb_port", default=""): str,  # This field will be visible regardless. Advanced UI tweaks might be required to make this dynamic.
            }),
            errors=_errors,
        )
