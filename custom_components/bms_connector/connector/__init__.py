"""Connector resolution for BMS communication."""

import logging

_LOGGER = logging.getLogger(__name__)


def get_serial_send_function(connector_info: dict):
    """Return a callable that sends commands via the configured connection type.

    The returned callable has the signature: fn(commands) -> list[str]
    and is designed to be passed to hass.async_add_executor_job().
    """
    conn_type = connector_info.get("type", "usb_serial")

    if conn_type == "telnet":
        from .local_serial.telnet_serial import send_telnet_command
        host = connector_info["host"]
        port = connector_info.get("port", 23)
        timeout = connector_info.get("timeout", 8)
        return lambda cmds: send_telnet_command(cmds, host=host, port=port, timeout=timeout)
    else:
        from .local_serial.local_serial import send_serial_command
        port = connector_info["port"]
        baudrate = connector_info.get("baudrate", 19200)
        timeout = connector_info.get("timeout", 2)
        return lambda cmds: send_serial_command(cmds, port=port, baudrate=baudrate, timeout=timeout)
