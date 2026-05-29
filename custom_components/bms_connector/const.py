# const.py
NAME = "BMS Connector"
DOMAIN = "bms_connector"
VERSION = "1.4.0"
ATTRIBUTION = "Integration for BMS via serial communication."

CONF_CONNECTION_TYPE = "connection_type"
CONF_POLL_INTERVAL = "poll_interval"
CONF_HOST = "host"
CONF_PORT = "port"

CONNECTION_TYPES = {
    "usb_serial": "USB-RS485 Serial",
    "telnet": "Telnet (RS485-to-Ethernet)",
}

BMS_TYPE_DEFAULTS = {
    "SEPLV2": {"bms_name": "SEP BMS V2 (SEPLV2)", "default_prefix": "Seplos BMS HA", "default_address": "0x00"},
    "SEPLV3": {"bms_name": "SEP BMS V3 (SEPLV3)", "default_prefix": "Seplos BMS V3", "default_address": "0x00"},
}

