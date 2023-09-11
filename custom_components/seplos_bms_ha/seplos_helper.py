import serial
import time
import logging
_LOGGER = logging.getLogger(__name__)

def send_serial_command(command: str, port: str, baudrate: int = 19200, timeout: int = 2) -> str:
    """
    Send a serial command and receive the response.
    """
    with serial.Serial(port, baudrate=baudrate, timeout=timeout) as ser:
        ser.write(command.encode())
        time.sleep(0.5)
        return ser.read(ser.in_waiting).decode().replace('\r', '').replace('\n', '')
        
        
class Telemetry:
    def __init__(self):
        self.cellsCount = 0
        self.cellVoltage = []
        self.tempCount = 0
        self.temperatures = []
        self.current = 0
        self.voltage = 0
        self.resCap = 0
        self.customNumber = 0
        self.capacity = 0
        self.soc = 0
        self.ratedCapacity = 0
        self.cycles = 0
        self.soh = 0
        self.portVoltage = 0
        
    def __str__(self):
        return (
            f"cellsCount: {self.cellsCount}, "
            f"cellVoltage: {self.cellVoltage}, "
            f"tempCount: {self.tempCount}, "
            f"temperatures: {self.temperatures}, "
            f"current: {self.current}, "
            f"voltage: {self.voltage}, "
            f"resCap: {self.resCap}, "
            f"customNumber: {self.customNumber}, "
            f"capacity: {self.capacity}, "
            f"soc: {self.soc}, "
            f"ratedCapacity: {self.ratedCapacity}, "
            f"cycles: {self.cycles}, "
            f"soh: {self.soh}, "
            f"portVoltage: {self.portVoltage}"
        )
 

def parse_telemetry_info(info_str):
    result = Telemetry()
    cursor = 4

    result.cellsCount = int(info_str[cursor:cursor+2], 16)
    cursor += 2
    for i in range(result.cellsCount):
        result.cellVoltage.append(int(info_str[cursor:cursor+4], 16))
        cursor += 4

    result.tempCount = int(info_str[cursor:cursor+2], 16)
    cursor += 2
    for i in range(result.tempCount):
        temperature = (int(info_str[cursor:cursor+4], 16) - 2731) / 10

        result.temperatures.append(temperature)
        cursor += 4

    result.current = int(info_str[cursor:cursor+4], 16)
    # Adjust the current value for integer underflow
    if result.current > 32767:  # Or another reasonable threshold
        result.current -= 65536  # Correct the value for a 16-bit integer underflow
    result.current /= 100  # Convert to the actual value

    cursor += 4
    result.voltage = int(info_str[cursor:cursor+4], 16) / 100
    cursor += 4
    result.resCap = int(info_str[cursor:cursor+4], 16) / 100
    cursor += 4
    result.customNumber = int(info_str[cursor:cursor+2], 16)
    cursor += 2
    result.capacity = int(info_str[cursor:cursor+4], 16) / 100
    cursor += 4
    result.soc = int(info_str[cursor:cursor+4], 16) / 10
    cursor += 4
    result.ratedCapacity = int(info_str[cursor:cursor+4], 16) / 100
    cursor += 4
    result.cycles = int(info_str[cursor:cursor+4], 16)
    cursor += 4
    result.soh = int(info_str[cursor:cursor+4], 16) / 10
    cursor += 4
    result.portVoltage = int(info_str[cursor:cursor+4], 16) / 100

    return result
    
    
       
class Alarms:
    def __init__(self):
        self.cellsCount = 0
        self.cellAlarm = []
        self.tempCount = 0
        self.tempAlarm = []
        self.currentAlarm = 0
        self.voltageAlarm = 0
        self.customAlarms = 0
        self.alarmEvent0 = 0
        self.alarmEvent1 = 0
        self.alarmEvent2 = 0
        self.alarmEvent3 = 0
        self.alarmEvent4 = 0
        self.alarmEvent5 = 0
        self.onOffState = 0
        self.equilibriumState0 = 0
        self.equilibriumState1 = 0
        self.systemState = 0
        self.disconnectionState0 = 0
        self.disconnectionState1 = 0
        self.alarmEvent6 = 0
        self.alarmEvent7 = 0
        
    def __str__(self):
        return (
            f"cellsCount: {self.cellsCount}, "
            f"cellAlarm: {self.cellAlarm}, "
            f"tempCount: {self.tempCount}, "
            f"tempAlarm: {self.tempAlarm}, "
            f"currentAlarm: {self.currentAlarm}, "
            f"voltageAlarm: {self.voltageAlarm}, "
            f"customAlarms: {self.customAlarms}, "
            f"alarmEvent0: {self.alarmEvent0}, "
            f"alarmEvent1: {self.alarmEvent1}, "
            f"alarmEvent2: {self.alarmEvent2}, "
            f"alarmEvent3: {self.alarmEvent3}, "
            f"alarmEvent4: {self.alarmEvent4}, "
            f"alarmEvent5: {self.alarmEvent5}, "
            f"onOffState: {self.onOffState}, "
            f"equilibriumState0: {self.equilibriumState0}, "
            f"equilibriumState1: {self.equilibriumState1}, "
            f"systemState: {self.systemState}, "
            f"disconnectionState0: {self.disconnectionState0}, "
            f"disconnectionState1: {self.disconnectionState1}, "
            f"alarmEvent6: {self.alarmEvent6}, "
            f"alarmEvent7: {self.alarmEvent7}"
        )
              
def parse_teledata_info(info_str):
    result = Alarms()
    cursor = 4

    # Helper function to check if there are enough characters left
    def remaining_length():
        return len(info_str) - cursor

    # Extracting cellsCount and looping for each cell
    result.cellsCount = int(info_str[cursor:cursor+2], 16)
    cursor += 2
    for i in range(result.cellsCount):
        if remaining_length() < 2:
            return result
        result.cellAlarm.append(int(info_str[cursor:cursor+2], 16))
        cursor += 2

    # Extracting tempCount and looping for each temperature alarm
    result.tempCount = int(info_str[cursor:cursor+2], 16)
    cursor += 2
    for i in range(result.tempCount):
        if remaining_length() < 2:
            return result
        result.tempAlarm.append(int(info_str[cursor:cursor+2], 16))
        cursor += 2

    # Extracting all remaining fields in the Alarms class. This assumes the order in the class is the same as in the message
    for attribute in ['currentAlarm', 'voltageAlarm', 'customAlarms', 'alarmEvent0', 'alarmEvent1', 'alarmEvent2', 'alarmEvent3', 'alarmEvent4', 'alarmEvent5', 'onOffState', 'equilibriumState0', 'equilibriumState1', 'systemState', 'disconnectionState0', 'disconnectionState1', 'alarmEvent6', 'alarmEvent7']:
        if remaining_length() < 2:
            return result
        setattr(result, attribute, int(info_str[cursor:cursor+2], 16))
        cursor += 2

    return result

def calc_check_sum(s):
    total_sum = sum(ord(c) for c in s)  # Sum up ASCII values directly
    checksum_value = (total_sum ^ 0xFFFF) + 1
    return format(checksum_value, 'X').zfill(4)  # Convert to uppercase hexadecimal and ensure it's 4 chars long

def form_battery_id_str(address):
    return format(address, '02x')

def extract_data_from_message(msg, telemetry_requested=True, teledata_requested=True, debug=False):
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
    
    if telemetry_requested:
        try:
            telemetry_result = parse_telemetry_info(info)
            if telemetry_result is not None and debug:
                print(address_string, telemetry_result.__dict__)
        except Exception as e:
            if debug:
                print(f"Telemetry parsing error: {e}")
        
    if teledata_requested:
        try:
            teledata_result = parse_teledata_info(info)
            if teledata_result is not None and debug:
                print(address_string, teledata_result.__dict__)
        except Exception as e:
            if debug:
                print(f"Teledata parsing error: {e}")

    return telemetry_result, teledata_result