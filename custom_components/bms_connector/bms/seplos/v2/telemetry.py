
# telemetry.py
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
    if result.current > 32767:
        result.current -= 65536 
    result.current /= 100 
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

