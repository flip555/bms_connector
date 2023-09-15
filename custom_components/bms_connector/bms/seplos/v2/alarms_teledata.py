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

    def remaining_length():
        return len(info_str) - cursor

    result.cellsCount = int(info_str[cursor:cursor+2], 16)

    cursor += 2
    for i in range(result.cellsCount):
        if remaining_length() < 2:
            return result
        result.cellAlarm.append(int(info_str[cursor:cursor+2], 16))
        cursor += 2

    result.tempCount = int(info_str[cursor:cursor+2], 16)
    cursor += 2
    for i in range(result.tempCount):
        if remaining_length() < 2:
            return result
        result.tempAlarm.append(int(info_str[cursor:cursor+2], 16))
        cursor += 2

    for attribute in ['currentAlarm', 'voltageAlarm', 'customAlarms', 'alarmEvent0', 'alarmEvent1', 'alarmEvent2', 'alarmEvent3', 'alarmEvent4', 'alarmEvent5', 'onOffState', 'equilibriumState0', 'equilibriumState1', 'systemState', 'disconnectionState0', 'disconnectionState1', 'alarmEvent6', 'alarmEvent7']:
        if remaining_length() < 2:
            return result
        setattr(result, attribute, int(info_str[cursor:cursor+2], 16))
        cursor += 2

    return result
