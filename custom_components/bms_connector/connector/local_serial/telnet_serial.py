"""Telnet/RS485-to-Ethernet connector for Seplos V2 - Ported from Home Energy Hub"""

import contextlib
import logging
import socket
import time

_LOGGER = logging.getLogger(__name__)

# End-of-message heuristic for bridges that do not preserve Modbus framing.
_SILENCE = 0.9


def _read_until_silence(
    sock: socket.socket, timeout: float, silence: float = _SILENCE
) -> str:
    """Collect ASCII text until the link goes quiet or the deadline expires."""
    chunks: list[str] = []
    deadline = time.monotonic() + timeout
    last_data = time.monotonic()

    while True:
        now = time.monotonic()
        if now - last_data > silence or now >= deadline:
            break

        sock.settimeout(min(silence, max(0.01, deadline - now)))
        try:
            chunk = sock.recv(4096)
        except TimeoutError:
            continue
        except OSError:
            break

        if not chunk:
            break

        chunks.append(chunk.decode("ascii", errors="ignore"))
        last_data = time.monotonic()

    return "".join(chunks)


def send_telnet_command(
    commands: list[str], host: str, port: int = 23, timeout: int = 8
) -> list[str]:
    """Send commands over TCP and return the '~'-delimited BMS messages."""
    responses: list[str] = []
    _LOGGER.debug("Connecting to %s:%s", host, port)

    sock = None
    try:
        sock = socket.create_connection((host, port), timeout=5)

        for raw_cmd in commands:
            sock.sendall(raw_cmd.encode("ascii"))
            time.sleep(0.1)

            full = _read_until_silence(sock, timeout)
            full = full.replace("\r", "").replace("\n", "")
            responses.extend(f"~{part}" for part in full.split("~") if part)

    except OSError as err:
        _LOGGER.error("TCP error on %s:%s - %s", host, port, err)
        return responses
    finally:
        if sock is not None:
            with contextlib.suppress(OSError):
                sock.close()

    return responses
