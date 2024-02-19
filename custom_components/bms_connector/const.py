# const.py
NAME = "BMS Connector"
DOMAIN = "bms_connector"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "1.1.0"
ATTRIBUTION = "Integration for BMS via serial communication."

BMS_TYPE_DEFAULTS = {
    "SEPLV2": {"bms_name": "SEP BMS V2 (SEPLV2)", "default_prefix": "Seplos BMS HA", "default_address": "0x00"},
    "SEPLV3": {"bms_name": "SEP BMS V3 (SEPLV3)", "default_prefix": "Seplos BMS V3", "default_address": "0x01"},
}

# Platforms
SENSOR = "sensor"
BINARY_SENSOR = "binary_sensor"
SELECT = "select"
NUMBER = "number"
PLATFORMS = [SENSOR, BINARY_SENSOR, SELECT, NUMBER]


HEH_REGISTER = {
    "00000": {
        "option_name": "BMS Connector Global Settings",
        "active": "1",
        "config_flow": "async_step_home_energy_hub_global_settings",
        "options_flow": "async_step_home_energy_hub_global_options",
        "init": "OctopusUKEnergyUKINIT"
    },
    "30100": {
        "option_name": "Seplos BMS",
        "active": "1",
        "submenu": {
            "30110": {
                "option_name": "Seplos BMS V2",
                "active": "1",
                "config_flow": "async_step_seplos_bms_v2_device",
                "options_flow": "async_step_seplos_options_bms_v2",
                "init": "/config/custom_components/home_energy_hub/seplos_bms_v2/init.py"

            },
            "30102": {
                "option_name": "Seplos BMS V3",
                "active": "0",
                "config_flow": "async_step_seplos_bms_v3_device",
                "options_flow": "async_step_seplos_options_bms_v3",
                "init": "/config/custom_components/home_energy_hub/seplos_bms_v2/init.py"

            }
        }
    },
    "30200": {
        "option_name": "JK BMS",
        "active": "0",
        "submenu": {
            "30201": {
                "option_name": "JK BMS 1",
                "active": "1",
                "config_flow": "/config/custom_components/home_energy_hub/config_flows/jk_bms_1.py",
                "init": "/config/custom_components/home_energy_hub/jk_bms_1/init.py"
            }
        }
    }
}
