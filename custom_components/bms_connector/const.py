# const.py
NAME = "BMS Connector"
DOMAIN = "bms_connector"
VERSION = "1.1.0"
ATTRIBUTION = "Integration for BMS via serial communication."

BMS_TYPE_DEFAULTS = {
    "SEPLV2": {"bms_name": "SEP BMS V2 (SEPLV2)", "default_prefix": "Seplos BMS HA", "default_address": "0x00"},
    "SEPLV3": {"bms_name": "SEP BMS V3 (SEPLV3)", "default_prefix": "Seplos BMS V3", "default_address": "0x01"},
}

