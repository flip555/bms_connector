"""Config flow for BMS Connector."""
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import (
    DOMAIN,
    BMS_TYPE_DEFAULTS,
    CONNECTION_TYPES,
    CONF_CONNECTION_TYPE,
    CONF_HOST,
    CONF_PORT,
    CONF_POLL_INTERVAL,
)


class BMSConnectorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        return await self.async_step_bms_type()

    async def async_step_bms_type(self, user_input=None):
        if user_input is not None:
            self.user_input = user_input
            bms_type = self.user_input.get("bms_type")
            if bms_type in BMS_TYPE_DEFAULTS:
                defaults = BMS_TYPE_DEFAULTS[bms_type]
                self.user_input["default_prefix"] = defaults["default_prefix"]
                self.user_input["default_address"] = defaults["default_address"]
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
            title = "{0} - {1} - {2} - {3}".format(
                self.user_input["bms_type"],
                self.user_input.get(CONF_HOST, self.user_input.get("connector_port", "unknown")),
                self.user_input["battery_address"],
                self.user_input["sensor_prefix"]
            )
            return self.async_create_entry(title=title, data=self.user_input)
        return self.async_show_form(
            step_id="sensor_prefix",
            data_schema=vol.Schema({
                vol.Required("battery_address", description="Battery address", default="{}".format(self.user_input["default_address"])): str,
                vol.Required("sensor_prefix", description="Sensor name prefix", default="{}".format(self.user_input["default_prefix"])): str,
                vol.Optional(CONF_POLL_INTERVAL, description="Poll interval (seconds)", default=10): vol.All(vol.Coerce(int), vol.Range(min=1, max=300)),
            }),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BMSConnectorOptionsFlowHandler(config_entry)


class BMSConnectorOptionsFlowHandler(config_entries.OptionsFlow):

    def __init__(self, config_entry):
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            new_data = self._config_entry.data.copy()
            new_data.update(user_input)
            self.hass.config_entries.async_update_entry(self._config_entry, data=new_data)
            self.hass.async_create_task(
                self.hass.config_entries.async_reload(self._config_entry.entry_id)
            )
            return self.async_create_entry(title="", data=user_input)

        connection_type = self._config_entry.data.get(CONF_CONNECTION_TYPE, "usb_serial")
        schema_fields = {
            vol.Optional(
                CONF_POLL_INTERVAL,
                description="Poll interval (seconds)",
                default=self._config_entry.data.get("poll_interval", 10),
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=300)),
        }

        if connection_type == "telnet":
            schema_fields[vol.Optional(
                CONF_HOST,
                description="Telnet host address",
                default=self._config_entry.data.get("host", ""),
            )] = str
            schema_fields[vol.Optional(
                CONF_PORT,
                description="Telnet port",
                default=self._config_entry.data.get("port", 23),
            )] = int
        else:
            schema_fields[vol.Optional(
                "connector_port",
                description="Serial port",
                default=self._config_entry.data.get("connector_port", "/dev/ttyUSB0"),
            )] = str

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema_fields),
        )
