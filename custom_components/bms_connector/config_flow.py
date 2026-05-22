from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN, BMS_TYPE_DEFAULTS, CONNECTION_TYPES, CONF_CONNECTION_TYPE, CONF_HOST, CONF_PORT

class BMSConnectorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Skip confirmation, go straight to BMS type selection."""
        return await self.async_step_bms_type()

    async def async_step_bms_type(self, user_input=None):
        if user_input is not None:
            self.user_input = user_input
            bms_type = self.user_input.get('bms_type')
            if bms_type in BMS_TYPE_DEFAULTS:
                defaults = BMS_TYPE_DEFAULTS[bms_type]
                self.user_input['default_prefix'] = defaults['default_prefix']
                self.user_input['default_address'] = defaults['default_address']
            return await self.async_step_connection_type()

        return self.async_show_form(
            step_id="bms_type",
            data_schema=vol.Schema({
                vol.Required("bms_type", description="Please select your BMS"): vol.In(list(BMS_TYPE_DEFAULTS.keys())),
            }),
        )

    async def async_step_connection_type(self, user_input=None):
        if user_input is not None:
            self.user_input.update(user_input)
            if user_input.get(CONF_CONNECTION_TYPE) == "telnet":
                return await self.async_step_telnet_config()
            else:
                return await self.async_step_usb_config()

        return self.async_show_form(
            step_id="connection_type",
            data_schema=vol.Schema({
                vol.Required(CONF_CONNECTION_TYPE, default="usb_serial"): vol.In(CONNECTION_TYPES),
            }),
        )

    async def async_step_usb_config(self, user_input=None):
        if user_input is not None:
            self.user_input.update(user_input)
            return await self.async_step_sensor_prefix()

        return self.async_show_form(
            step_id="usb_config",
            data_schema=vol.Schema({
                vol.Required("connector_port", description="Serial port", default="/dev/ttyUSB0"): str,
            }),
        )

    async def async_step_telnet_config(self, user_input=None):
        if user_input is not None:
            self.user_input.update(user_input)
            return await self.async_step_sensor_prefix()

        return self.async_show_form(
            step_id="telnet_config",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST, description="Telnet host address"): str,
                vol.Optional(CONF_PORT, description="Telnet port", default=23): int,
            }),
        )

    async def async_step_sensor_prefix(self, user_input=None):
        if user_input is not None:
            self.user_input.update(user_input)
            title = f"{self.user_input['bms_type']} - {self.user_input.get(CONF_HOST, self.user_input.get('connector_port', 'unknown'))} - {self.user_input['battery_address']} - {self.user_input['sensor_prefix']}"
            return self.async_create_entry(title=title, data=self.user_input)

        return self.async_show_form(
            step_id="sensor_prefix",
            data_schema=vol.Schema({
                vol.Required("battery_address", description="Battery address", default=f"{self.user_input['default_address']}"): str,
                vol.Required("sensor_prefix", description="Sensor name prefix", default=f"{self.user_input['default_prefix']}"): str,
            }),
        )
