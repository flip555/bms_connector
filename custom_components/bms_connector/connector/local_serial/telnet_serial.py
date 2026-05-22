"""Telnet Serial connector for Seplos V2 - Ported from Home Energy Hub"""

import asyncio
import logging
import telnetlib
import time
from typing import List

_LOGGER = logging.getLogger(__name__)

# Synchronous send function (called via executor_job)
def send_telnet_command(commands: List[str], host: str, port: int = 23, timeout: int = 8) -> List[str]:
    """Send commands via telnet and collect responses."""
    responses = []
    _LOGGER.debug("Connecting to %s:%s", host, port)

    tn = telnetlib.Telnet(host, port, timeout=5)

    try:
        for raw_cmd in commands:
            tn.write(raw_cmd.encode('ascii'))
            time.sleep(0.1)

            # Receive response with silence detection
            messages = []
            last_data = time.perf_counter()

            while True:
                try:
                    chunk = tn.read_very_eager()
                    if chunk:
                        messages.append(chunk.decode('ascii', errors='ignore'))
                        last_data = time.perf_counter()
                    else:
                        if time.perf_counter() - last_data > 0.9:
                            break

                    if time.perf_counter() - last_data > timeout:
                        break
                except EOFError:
                    break

                time.sleep(0.03)

            full = ''.join(messages).replace('\r', '').replace('\n', '')
            parts = [p for p in full.split('~') if p]
            responses.extend(['~' + p for p in parts])

    finally:
        tn.close()

    return responses
