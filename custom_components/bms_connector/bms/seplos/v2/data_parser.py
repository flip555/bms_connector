import logging
from .settings_protection import decode_fourseven
from .management_info import decode_fiveone
from .telemetry import parse_telemetry_info
from .alarms_teledata import parse_teledata_info

_LOGGER = logging.getLogger(__name__)

def calc_check_sum(s):
    total_sum = sum(ord(c) for c in s)  # Sum up ASCII values directly
    checksum_value = (total_sum ^ 0xFFFF) + 1
    return format(checksum_value, 'X').zfill(4)  # Convert to uppercase hexadecimal and ensure it's 4 chars long

def form_battery_id_str(address):
    return format(address, '02x')

def get_cid2(message_hex_str):
    # Convert bytes to a hex string
    #message_hex_str = encoded_data.hex()
    if message_hex_str.startswith("~"):
        message_hex_str = message_hex_str[1:]

    CID2 = message_hex_str[8:10]

    # Check the first byte for command identification
    return CID2

def extract_data_from_message(msg, telemetry_requested=True, teledata_requested=True, debug=True):
    processed_data = None
    processed_data1 = None
    processed_data2 = None
    processed_data3 = None
    address_string = None
    address_string1 = None
    address_string2 = None
    address_string3 = None

    for response in msg:
        if response.startswith("~"):
            response = response[1:]

        check_sum = response[-4:]
        msg_wo_chk_sum = response[:-4]
        calculated_check_sum = calc_check_sum(msg_wo_chk_sum)
        if debug:
            _LOGGER.debug("Calculated Checksum: %s", calculated_check_sum)

        if check_sum != calculated_check_sum:
            if debug:
                _LOGGER.debug("Checksum mismatch!")
            return None, None

        cid2 = get_cid2(response)

        if cid2 == "10":
            address = int(msg_wo_chk_sum[2:4], 16)
            address_string = '0x' + form_battery_id_str(address)
            info = msg_wo_chk_sum[12:]
            try:
                processed_data = parse_telemetry_info(info)
                if processed_data is not None and debug:
                    _LOGGER.debug("Telemetry Result for %s: %s", address_string, processed_data.__dict__)
            except Exception as e:
                if debug:
                    _LOGGER.debug("Telemetry parsing error: %s", e)
            if debug:
                _LOGGER.debug("About to return from extract_data_from_message. Telemetry: %s", processed_data)


        elif cid2 == "80":
            address1 = int(msg_wo_chk_sum[2:4], 16)
            address_string1 = '0x' + form_battery_id_str(address1)
            info = msg_wo_chk_sum[12:]
            try:
                processed_data1 = parse_teledata_info(info)
                if processed_data1 is not None and debug:
                    _LOGGER.debug("Teledata Result for %s: %s", address_string1, processed_data1.__dict__)
            except Exception as e:
                if debug:
                    _LOGGER.debug("Teledata parsing error: %s", e)
            if debug:
                _LOGGER.debug("About to return from extract_data_from_message. Teledata: %s", processed_data1)



        elif cid2 == "81":
            #infoflag, datai_values, decoded_data = decode_fourseven(response)
            address2 = int(msg_wo_chk_sum[2:4], 16)
            address_string2 = '0x' + form_battery_id_str(address2)
            info = msg_wo_chk_sum[12:]
            try:
                processed_data2 = decode_fourseven(info)
                if processed_data2 is not None and debug:
                    _LOGGER.debug("Setting Details for %s: %s", address_string2, processed_data2.__dict__)
            except Exception as e:
                if debug:
                    _LOGGER.debug("Setting Details parsing error: %s", e)
            if debug:
                _LOGGER.debug("About to return from extract_data_from_message. Setting Details: %s", processed_data2)



        elif cid2 == "C0":
            address3 = int(msg_wo_chk_sum[2:4], 16)
            address_string3 = '0x' + form_battery_id_str(address3)
            info = msg_wo_chk_sum[12:]
            try:
                processed_data3 = decode_fiveone(info)
                if processed_data3 is not None and debug:
                    _LOGGER.debug("Device Details for %s: %s", address_string3, processed_data3.__dict__)
            except Exception as e:
                if debug:
                    _LOGGER.debug("Device Details parsing error: %s", e)
            if debug:
                _LOGGER.debug("About to return from extract_data_from_message. Device Details: %s", processed_data3)



        else:
            if debug:
                _LOGGER.debug("UNKNOWN CID2: %s", cid2)

    return address_string, processed_data, processed_data1, processed_data3, processed_data2
