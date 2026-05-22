"""Connector resolution for BMS communication."""

import logging

_LOGGER = logging.getLogger(__name__)


def get_serial_send_function(connector_info: dict):
    """Return the appropriate send function and its args based on connector type."""
    conn_type = connector_info.get("type", "usb_serial")

    if conn_type == "telnet":
        from .local_serial.telnet_serial import send_telnet_command
        return send_telnet_command, {
            "host": connector_info["host"],
            "port": connector_info.get("port", 23),
            "timeout": connector_info.get("timeout", 8),
        }
    else:
        from .local_serial.local_serial import send_serial_command
        return send_serial_command, {
            "port": connector_info["port"],
            "baudrate": connector_info.get("baudrate", 19200),
            "timeout": connector_info.get("timeout", 2),
        }
