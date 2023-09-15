import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, BMS_TYPES

class BMSConnectorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def is_valid_port(self, port: str) -> bool:
        """Validate if the provided port exists and has permissions."""
        try:
            with serial.Serial(port, baudrate=9600, timeout=1):
                return True
        except (OSError, serial.SerialException):
            return False

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Validate user input here
            title = f"{user_input['bms_type']} - {user_input['battery_address']}"
            return self.async_create_entry(title=title, data=user_input)

        data_schema = vol.Schema({
            vol.Required("bms_type", description="BMS Type"): vol.In(BMS_TYPES),
            vol.Required("connector_port", description="Connector Port (e.g., /dev/ttyUSB0 or esp@ip:port)", default="/dev/ttyUSB0"): str,
            vol.Required("battery_address", description="Battery Address [e.g., 0x00]", default="0x00"): str,
            vol.Required("sensor_prefix", description="Sensor Prefix [e.g., Seplos BMS 0x00 -]", default="Seplos BMS V2 0x00 - "): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
