from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, HEH_REGISTER
import logging
import importlib
import sys
from homeassistant.core import callback

# ---------------------------------------------
# ------------- CONFIG IMPORTS START ----------
# ---------------------------------------------
# Add your module imports here. 
# If you're adding a new module, import it in this section.
from .config_flows.bms.seplos import SeplosConfigFlowMethods, SeplosOptionsFlowMethods
# Example: 
# from .config_flows.category.file import YourMethodName
# ---------------------------------------------
# ---------------------------------------------

_LOGGER = logging.getLogger(__name__)
class BMSConnectorOptionsFlow(config_entries.OptionsFlow,                                
                                # ---------------------------------------------
                                # ---------- ADD NEW METHODS HERE -------------
                                # ---------------------------------------------
                                # This is where you add method references 
                                # for new modules you've imported.
                                SeplosOptionsFlowMethods, 
                                # Example:
                                # YourMethodName,
                                # ---------------------------------------------
                                # ---------------------------------------------
                                ):
    # This is a stub. Here you would define the options schema and the logic for updating options.
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):        
        options_flow = self.config_entry.data.get("options_flow", "")

        method_to_call = getattr(self, options_flow, None)
        if callable(method_to_call):
            return await method_to_call()

    async def async_step_home_energy_hub_global_options(self, user_input=None):
        if user_input is not None:
                # Update the data
                self.config_entry.data = {**self.config_entry.data, **user_input}
                
                # Update the config entry
                self.hass.config_entries.async_update_entry(self.config_entry, data=self.config_entry.data)
                
                return self.async_create_entry(title="", data=user_input)

        disclaimer = self.config_entry.data.get("disclaimer")
        anon_reporting_confirm = self.config_entry.data.get("anon_reporting_confirm", False)
        return self.async_show_form(
            step_id="home_energy_hub_global_options",
            data_schema=vol.Schema({
                vol.Optional("anon_reporting_confirm", default=anon_reporting_confirm): bool,

            })
        )

class BMSConnectorConfigFlow(config_entries.ConfigFlow,
                                # ---------------------------------------------
                                # ---------- ADD NEW METHODS HERE -------------
                                # ---------------------------------------------
                                # This is where you add method references 
                                # for new modules you've imported.
                                SeplosConfigFlowMethods, 
                                # Example:
                                # YourMethodName,
                                # ---------------------------------------------
                                # ---------------------------------------------
                            domain=DOMAIN):
    VERSION = 1


    def __init__(self):
        # Initialize the user_input and submenu_stack attributes
        self.user_input = {}
        self.submenu_stack = []

    async def async_step_user(self, user_input=None):
        errors = {}

        # Check if an entry with "first_run" set to 1 already exists for this DOMAIN
        existing_entry = next((entry for entry in self.hass.config_entries.async_entries(DOMAIN) 
                               if entry.data.get("disclaimer") == 1), None)
        if existing_entry:
            if user_input is not None:
                # Proceed to the next step
                return await self.async_step_submenu_selection(user_input)

            main_menu_options = [
                v['option_name']
                for k, v in HEH_REGISTER.items()
                if v.get('active') == '1' and k != "00000"
            ]

            data_schema = vol.Schema({
                vol.Required("submenu_selection", description="Select a submenu"): vol.In(main_menu_options),
            })

            return self.async_show_form(
                step_id="submenu_selection",
                data_schema=data_schema,
                errors=errors,
            )
        else:
            # Handle the error or any logic you want to do if the entry exists
            return await self.async_step_home_energy_hub_global_settings()


    async def async_step_submenu_selection(self, user_input=None):
        if user_input is not None:
            submenu_name = user_input.get('submenu_selection')
            self.submenu_stack.append(submenu_name)
            submenu, config_flow_dir, init_dir, options_flow, heh_registry = self.get_submenu()

            if submenu and submenu != "config_flow":
                submenu_options = [
                    v['option_name']
                    for k, v in submenu.items()
                    if v.get('active') == '1'
                ]

                data_schema = vol.Schema({
                    vol.Required("submenu_selection", description="Select a submenu"): vol.In(submenu_options),
                })

                return self.async_show_form(
                    step_id="submenu_selection",
                    data_schema=data_schema,
                )
            else:
                # Handle the selected submenu here
                self.user_input["options_flow"] = options_flow
                self.user_input["init"] = init_dir
                self.user_input["home_energy_hub_registry"] = heh_registry
                method_to_call = getattr(self, config_flow_dir, None)
                if callable(method_to_call):
                    return await method_to_call()

        # Return to the main menu if there are no more submenus to select
        return await self.async_step_user()

    def get_submenu(self):
        submenu_data = HEH_REGISTER
        config_flow_dir = None
        init_dir = None
        options_flow = None
        heh_registry = None

        for submenu_name in self.submenu_stack:
            try:
                submenu_data = next((v['submenu'] for k, v in submenu_data.items() if v['option_name'] == submenu_name), None)
            except KeyError:
                try:
                    heh_registry, matching_submenu = next(((k, v) for k, v in submenu_data.items() if v['option_name'] == submenu_name), (None, None))
                    if matching_submenu:
                        config_flow_dir = matching_submenu.get('config_flow', None)
                        options_flow = matching_submenu.get('options_flow', None)
                        init_dir = matching_submenu.get('init', None)
                        submenu_data = "config_flow"

                    else:
                        submenu_data = {}
                except KeyError:
                        submenu_data = {}

        return submenu_data, config_flow_dir, init_dir, options_flow, heh_registry

    async def async_step_home_energy_hub_global_settings(self, user_input=None):
        errors = {}

        if user_input is not None:
            if not user_input.get("disclaimer"):
                errors["disclaimer"] = "You must accept the disclaimer to proceed!"
            else:
                user_input["bms_connector_first_run"] = 1
                user_input["options_flow"] = "async_step_home_energy_hub_global_options"

                # Check if the entry already exists
                existing_entry = None
                for entry in self._async_current_entries():
                    if entry.data.get("bms_connector_first_run") == 1:
                        existing_entry = entry
                        break

                # Update existing entry if found; otherwise create a new entry
                if existing_entry:
                    self.hass.config_entries.async_update_entry(existing_entry, data={**existing_entry.data, **user_input})
                    return self.async_abort(reason="entry_updated")
                else:
                    return self.async_create_entry(title="BMS Connector Global Settings", data=user_input)

        data_schema = vol.Schema({
            vol.Required("disclaimer"): bool,
            vol.Optional("anon_reporting_confirm"): bool,
        })
        return self.async_show_form(
            step_id="home_energy_hub_global_settings",
            data_schema=data_schema,
            errors=errors,
        )


    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BMSConnectorOptionsFlow(config_entry)
