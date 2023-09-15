from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN, BMS_TYPES

class BMSConnectorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None and user_input.get("confirm"):
            # If the user checks the box, proceed to the next step
            return await self.async_step_bms_type()

        data_schema = vol.Schema({
            vol.Required("confirm", description="I confirm"): bool,
        })
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_bms_type(self, user_input=None):
        if user_input is not None:
            # Store user input and transition to the next step
            self.user_input = user_input
            return await self.async_step_connector_port()

        data_schema = vol.Schema({
            vol.Required("bms_type", description="Please select your BMS"): vol.In(BMS_TYPES),
        })

        return self.async_show_form(
            step_id="bms_type",
            data_schema=data_schema,
        )

    async def async_step_connector_port(self, user_input=None):
        if user_input is not None:
            # Store user input and transition to the next step
            self.user_input["connector_port"] = user_input["connector_port"]
            return await self.async_step_sensor_prefix()

        data_schema = vol.Schema({
            vol.Required("connector_port", description="Please enter your port", default="/dev/ttyUSB0"): str,
        })

        return self.async_show_form(
            step_id="connector_port",
            data_schema=data_schema,
        )

    async def async_step_sensor_prefix(self, user_input=None):
        if user_input is not None:
            # Store user input and transition to the additional config step
            title = f"{self.user_input['bms_type']} - {self.user_input['connector_port']}"
            return self.async_create_entry(title=title, data=self.user_input)

        data_schema = vol.Schema({
            vol.Required("sensor_prefix", description="Please enter your desired sensor prefix", default="Seplos BMS V2 0x00 - "): str,
        })

        return self.async_show_form(
            step_id="sensor_prefix",
            data_schema=data_schema,
        )
