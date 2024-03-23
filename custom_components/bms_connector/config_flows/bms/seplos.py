from homeassistant import config_entries
import voluptuous as vol
from ...const import DOMAIN
from serial.tools import list_ports

class SeplosConfigFlowMethods:
    async def async_step_seplos_bms_v2_device(self, user_input=None):
        # Query available USB ports
        ports = [port.device for port in list_ports.comports()]
        default_port = ports[0] if ports else "/dev/ttyUSB0"  # Fallback default

        if user_input is not None:
            # Store user input and create the configuration entry
            self.user_input.update(user_input)
            self.user_input["sensor_update_frequency"] = 5
            title = f"{self.user_input['name_prefix']} {self.user_input['usb_port']}"
            return self.async_create_entry(title=title, data=self.user_input)

        # Include dynamic listing of USB ports in the schema
        data_schema = vol.Schema({
            vol.Required("usb_port", default=default_port): vol.In(ports),
            vol.Required("baud_rate", default=19200): int,
            vol.Required("name_prefix", default="Seplos BMS HA - "): str,
            vol.Required("battery_pack_count", default=1): vol.All(vol.Coerce(int), vol.Range(min=1, max=16)),
        })

        return self.async_show_form(
            step_id="seplos_bms_v2_device",
            data_schema=data_schema,
        )

class SeplosOptionsFlowMethods:
    async def async_step_seplos_options_bms_v2(self, user_input=None):
        if user_input is not None:
                # Update the data
                self.config_entry.data = {**self.config_entry.data, **user_input}
                
                # Update the config entry
                self.hass.config_entries.async_update_entry(self.config_entry, data=self.config_entry.data)
                
                return self.async_create_entry(title="", data=user_input)
        battery_pack_count = self.config_entry.data.get("battery_pack_count", 1)
        #usb_port = self.config_entry.data.get("usb_port", "")
        ports = [port.device for port in list_ports.comports()]
        usb_port = self.config_entry.data.get("usb_port", ports[0] if ports else "/dev/ttyUSB0")  # Fallback or current setting
        name_prefix = self.config_entry.data.get("name_prefix", f"Seplos BMS HA - ")
        baud_rate = self.config_entry.data.get("baud_rate", 19200)
        sensor_update_frequency = self.config_entry.data.get("sensor_update_frequency", 5)

        return self.async_show_form(
            step_id="seplos_options_bms_v2",
            data_schema=vol.Schema({
                vol.Required("usb_port", default=usb_port): vol.In(ports),
                vol.Required("baud_rate", default=baud_rate): int,
                vol.Required("name_prefix", default=name_prefix): str,
                vol.Required("battery_pack_count", default=battery_pack_count): vol.All(vol.Coerce(int), vol.Range(min=1, max=16)),
                vol.Required("sensor_update_frequency", default=sensor_update_frequency): int,
            })
        )
