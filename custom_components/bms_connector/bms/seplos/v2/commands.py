"""Seplos V2 ASCII command construction."""

_V2_CID1 = ("42", "44", "47", "51")


def calc_check_sum(text):
    """Return the four-hex-digit checksum for a frame body."""
    total_sum = sum(ord(c) for c in text)
    checksum_value = (total_sum ^ 0xFFFF) + 1
    return format(checksum_value, "X").zfill(4)


def build_v2_commands(battery_address):
    """Build PIA/PIB/0x47/0x51 commands for a pack address (0x00-0x0F)."""
    try:
        addr = int(str(battery_address), 16)
    except (TypeError, ValueError) as err:
        raise ValueError(f"Invalid battery address: {battery_address!r}") from err
    if not 0 <= addr <= 0x0F:
        raise ValueError(f"Battery address out of range: {battery_address!r}")

    commands = []
    for cid1 in _V2_CID1:
        body = f"200046{cid1}E002{addr:02X}"
        commands.append("~" + body + calc_check_sum(body) + "\r")
    return commands
