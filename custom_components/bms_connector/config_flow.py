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
    VERSION = 2

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
                vol.Optional("baud_rate", description="Baud rate", default=19200): vol.In(
                    [9600, 19200, 38400, 57600, 115200]
                ),
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
            port = self.user_input.get(CONF_HOST) or self.user_input.get("connector_port")
            await self.async_set_unique_id(
                "{}_{}_{}_{}".format(
                    self.user_input.get("bms_type"),
                    self.user_input.get("battery_address"),
                    port,
                    self.user_input.get("connection_type", "usb_serial"),
                )
            )
            self._abort_if_unique_id_configured()
            title = "{} - {} - {} - {}".format(
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

    def _schema(self, data):
        connection_type = data.get(CONF_CONNECTION_TYPE, "usb_serial")
        fields = {
            vol.Optional(
                "battery_address", default=data.get("battery_address", "0x00")
            ): str,
            vol.Optional(
                "sensor_prefix", default=data.get("sensor_prefix", "BMS")
            ): str,
            vol.Optional(
                CONF_POLL_INTERVAL,
                default=data.get("poll_interval", 10),
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=300)),
        }
        if connection_type == "telnet":
            fields[vol.Optional(CONF_HOST, default=data.get("host", ""))] = str
            fields[vol.Optional(CONF_PORT, default=data.get("port", 23))] = int
        else:
            fields[vol.Optional(
                "connector_port", default=data.get("connector_port", "/dev/ttyUSB0")
            )] = str
            fields[vol.Optional(
                "baud_rate", default=data.get("baud_rate") or 19200
            )] = vol.In([9600, 19200, 38400, 57600, 115200])
        return vol.Schema(fields)

    async def async_step_init(self, user_input=None):
        errors = {}
        data = self._config_entry.data

        if user_input is not None:
            new_data = data.copy()
            new_data.update(user_input)
            port = new_data.get(CONF_HOST) or new_data.get("connector_port")
            unique_id = "{}_{}_{}_{}".format(
                new_data.get("bms_type"),
                new_data.get("battery_address"),
                port,
                new_data.get("connection_type", "usb_serial"),
            )

            conflict = any(
                entry.entry_id != self._config_entry.entry_id
                and entry.unique_id == unique_id
                for entry in self.hass.config_entries.async_entries(DOMAIN)
            )
            if conflict:
                errors["base"] = "unique_id_conflict"
            else:
                self.hass.config_entries.async_update_entry(
                    self._config_entry, data=new_data, unique_id=unique_id
                )
                self.hass.async_create_task(
                    self.hass.config_entries.async_reload(self._config_entry.entry_id)
                )
                return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self._schema(data),
            errors=errors,
        )
