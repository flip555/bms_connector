from homeassistant import config_entries
import voluptuous as vol
from ..const import DOMAIN, SEPLOS_BMS_TYPE_DEFAULTS

class BMSConfigFlowMethods:
    async def async_step_bms_type(self, user_input=None):
        if user_input is not None:
            # Store user input and transition to the next step
            self.user_input = user_input
            bms_type = self.user_input.get('bms_type')
            if bms_type in SEPLOS_BMS_TYPE_DEFAULTS:
                defaults = SEPLOS_BMS_TYPE_DEFAULTS[bms_type]
                self.user_input['default_prefix'] = defaults['default_prefix']
                self.user_input['default_address'] = defaults['default_address']
            return await self.async_step_connector_port()

        data_schema = vol.Schema({
            vol.Required("bms_type", description="Please select your BMS"): vol.In(list(SEPLOS_BMS_TYPE_DEFAULTS.keys())),
        })

        return self.async_show_form(
            step_id="bms_type",
            data_schema=data_schema,
        )

    async def async_step_connector_port(self, user_input=None):
        if user_input is not None:
            # Store user input and transition to the next step
            self.user_input.update(user_input)
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
            # Store user input and create the configuration entry
            self.user_input.update(user_input)
            title = f"{self.user_input['bms_type']} - {self.user_input['connector_port']} - {self.user_input['battery_address']} - {self.user_input['sensor_prefix']}"
            return self.async_create_entry(title=title, data=self.user_input)

        data_schema = vol.Schema({
            vol.Required("battery_address", description="Please enter the battery address", default=f"{self.user_input['default_address']}"): str,
            vol.Required("sensor_prefix", description="Please enter your desired sensor prefix", default=f"{self.user_input['default_prefix']}"): str,
        })

        return self.async_show_form(
            step_id="sensor_prefix",
            data_schema=data_schema,
        )
