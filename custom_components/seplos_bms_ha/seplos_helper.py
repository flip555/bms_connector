import logging
from .serial_comms import send_serial_command
from .telemetry import Telemetry, parse_telemetry_info
from .alarms_teledata import Alarms, parse_teledata_info

_LOGGER = logging.getLogger(__name__)

def calc_check_sum(s):
    total_sum = sum(ord(c) for c in s)  # Sum up ASCII values directly
    checksum_value = (total_sum ^ 0xFFFF) + 1
    return format(checksum_value, 'X').zfill(4)  # Convert to uppercase hexadecimal and ensure it's 4 chars long

def form_battery_id_str(address):
    return format(address, '02x')
    
def extract_data_from_message(msg, telemetry_requested=True, teledata_requested=True, debug=True):
    if msg.startswith("~"):
        msg = msg[1:]  # remove the tilde at the beginning

    check_sum = msg[-4:]
    msg_wo_chk_sum = msg[:-4]
    calculated_check_sum = calc_check_sum(msg_wo_chk_sum)
    
    if debug:
        print(calculated_check_sum)
        
    if check_sum != calculated_check_sum:
        if debug:
            print("Checksum mismatch!")
        return None, None

    address = int(msg_wo_chk_sum[2:4], 16)
    address_string = '0x' + form_battery_id_str(address)
    info = msg_wo_chk_sum[12:]
    
    telemetry_result = None
    teledata_result = None

    if telemetry_requested and not teledata_requested:
        try:
            telemetry_result = parse_telemetry_info(info)
            if telemetry_result is not None and debug:
                print(address_string, telemetry_result.__dict__)
        except Exception as e:
            if debug:
                print(f"Telemetry parsing error: {e}")
        _LOGGER.debug("About to return from extract_data_from_message. Telemetry: %s", telemetry_result)

    elif teledata_requested and not telemetry_requested:
        try:
            teledata_result = parse_teledata_info(info)
            if teledata_result is not None and debug:
                print(address_string, teledata_result.__dict__)
        except Exception as e:
            if debug:
                print(f"Teledata parsing error: {e}")
        _LOGGER.debug("About to return from extract_data_from_message. Teledata: %s", teledata_result)
        
    return telemetry_result, teledata_result, address_string
