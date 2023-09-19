# Telemetry Commands Packs 00-15
TELEMETRY_COMMANDS = {
    0: "~20004642E00200FD37\r",
    1: "~20004642E00201FD36\r",
    2: "~20004642E00202FD35\r",
    3: "~20004642E00203FD34\r",
    4: "~20004642E00204FD33\r",
    5: "~20004642E00205FD32\r",
    6: "~20004642E00206FD31\r",
    7: "~20004642E00207FD30\r",
    8: "~20004642E00208FD2F\r",
    9: "~20004642E00209FD2E\r",
    10: "~20004642E00210FD36\r",
    11: "~20004642E00211FD35\r",
    12: "~20004642E00212FD34\r",
    13: "~20004642E00213FD33\r",
    14: "~20004642E00214FD32\r",
    15: "~20004642E00215FD31\r"
}

# Teledata Codes Packs 00-15
TELEDATA_CODES = {
    0: "~20004644E00200FD35\r",
    1: "~20004644E00201FD34\r",
    2: "~20004644E00202FD33\r",
    3: "~20004644E00203FD32\r",
    4: "~20004644E00204FD31\r",
    5: "~20004644E00205FD30\r",
    6: "~20004644E00206FD2F\r",
    7: "~20004644E00207FD2E\r",
    8: "~20004644E00208FD2D\r",
    9: "~20004644E00209FD2C\r",
    10: "~20004644E00210FD34\r",
    11: "~20004644E00211FD33\r",
    12: "~20004644E00212FD32\r",
    13: "~20004644E00213FD31\r",
    14: "~20004644E00214FD30\r",
    15: "~20004644E00215FD2F\r"
}

ALARM_ATTRIBUTES = [
    "cellAlarm", "tempAlarm", "currentAlarm", "voltageAlarm",
    "customAlarms", "alarmEvent0", "alarmEvent1", "alarmEvent2",
    "alarmEvent3", "alarmEvent4", "alarmEvent5", "alarmEvent6",
    "alarmEvent7", "onOffState", "equilibriumState0", "equilibriumState1",
    "systemState", "disconnectionState0", "disconnectionState1"
]

SYSTEM_ATTRIBUTES = [
    "device_name", "software_version", "manufacturer_name"
]
SETTINGS_ATTRIBUTES = [
    "overcurrent_delay_recovery",
    "total_voltage_overvoltage_protection",
    "equalization_opening_voltage",
    "monomer_undervoltage_recovery",
    "monomer_low_pressure_recovery",
    "monomer_overvoltage_protection",
    "monomer_overvoltage_recovery",
    "monomer_undervoltage_protection",
    "monomer_low_pressure_alarm",
    "monomer_high_pressure_recovery",
    "battery_low_voltage_forbidden_charging",
    "total_pressure_high_pressure_alarm"
]
ALARM_MAPPINGS = {
    "alarmEvent0": [
        "No Alarm", 
        "Alarm that analog quantity reaches the lower limit", 
        "Alarm that analog quantity reaches the upper limit", 
        "Other alarms"
    ],
    "alarmEvent1": [
        "Voltage sensor fault", 
        "Temperature sensor fault", 
        "Current sensor fault", 
        "Key switch fault", 
        "Cell voltage dropout fault", 
        "Charge switch fault", 
        "Discharge switch fault", 
        "Current limit switch fault"
    ],
    "alarmEvent2": [
        "Monomer high voltage alarm", 
        "Monomer overvoltage protection", 
        "Monomer low voltage alarm", 
        "Monomer under voltage protection", 
        "High voltage alarm for total voltage", 
        "Overvoltage protection for total voltage", 
        "Low voltage alarm for total voltage", 
        "Under voltage protection for total voltage"
    ],
    "alarmEvent3": [
        "Charge high temperature alarm", 
        "Charge over temperature protection", 
        "Charge low temperature alarm", 
        "Charge under temperature protection", 
        "Discharge high temperature alarm", 
        "Discharge over temperature protection", 
        "Discharge low temperature alarm", 
        "Discharge under temperature protection"
    ],
    "alarmEvent4": [
        "Environment high temperature alarm", 
        "Environment over temperature protection", 
        "Environment low temperature alarm", 
        "Environment under temperature protection", 
        "Power over temperature protection", 
        "Power high temperature alarm", 
        "Cell low temperature heating", 
        "Reservation bit"
    ],
    "alarmEvent5": [
        "Charge over current alarm", 
        "Charge over current protection", 
        "Discharge over current alarm", 
        "Discharge over current protection", 
        "Transient over current protection", 
        "Output short circuit protection", 
        "Transient over current lockout", 
        "Output short circuit lockout"
    ],
    "alarmEvent6": [
        "Charge high voltage protection", 
        "Intermittent recharge waiting", 
        "Residual capacity alarm", 
        "Residual capacity protection", 
        "Cell low voltage charging prohibition", 
        "Output reverse polarity protection", 
        "Output connection fault", 
        "Inside bit"
    ],
    "alarmEvent7": [
        "Inside bit", 
        "Inside bit", 
        "Inside bit", 
        "Inside bit", 
        "Automatic charging waiting", 
        "Manual charging waiting", 
        "Inside bit", 
        "Inside bit"
    ],
    "alarmEvent8": [
        "EEP storage fault", 
        "RTC error", 
        "Voltage calibration not performed", 
        "Current calibration not performed", 
        "Zero calibration not performed", 
        "Inside bit", 
        "Inside bit", 
        "Inside bit"
    ],
    "cellAlarm": {
        0: "No Alarm",
        1: "Alarm"
    },
    "tempAlarm": {
        0: "No Alarm",
        1: "Alarm"
    },
    "currentAlarm": {
        1: "Charge/Discharge Current Alarm"
    },
    "voltageAlarm": {
        1: "Total Battery Voltage Alarm"
    },
    "onOffState": [
        "Discharge switch state",
        "Charge switch state",
        "Current limit switch state",
        "Heating switch state",
        "Reservation bit",
        "Reservation bit",
        "Reservation bit",
        "Reservation bit"
    ],
    "equilibriumState0": [
        "Cell 01 equilibrium",
        "Cell 02 equilibrium",
        "Cell 03 equilibrium",
        "Cell 04 equilibrium",
        "Cell 05 equilibrium",
        "Cell 06 equilibrium",
        "Cell 07 equilibrium",
        "Cell 08 equilibrium"
    ],
    "equilibriumState1": [
        "Cell 09 equilibrium",
        "Cell 10 equilibrium",
        "Cell 11 equilibrium",
        "Cell 12 equilibrium",
        "Cell 13 equilibrium",
        "Cell 14 equilibrium",
        "Cell 15 equilibrium",
        "Cell 16 equilibrium"
    ],
    "systemState": [
        "Discharge",
        "Charge",
        "Floating charge",
        "Reservation bit",
        "Standby",
        "Shutdown",
        "Reservation bit",
        "Reservation bit"
    ],
    "disconnectionState0": [
        "Cell 01 disconnection",
        "Cell 02 disconnection",
        "Cell 03 disconnection",
        "Cell 04 disconnection",
        "Cell 05 disconnection",
        "Cell 06 disconnection",
        "Cell 07 disconnection",
        "Cell 08 disconnection"
    ],
    "disconnectionState1": [
        "Cell 09 disconnection",
        "Cell 10 disconnection",
        "Cell 11 disconnection",
        "Cell 12 disconnection",
        "Cell 13 disconnection",
        "Cell 14 disconnection",
        "Cell 15 disconnection",
        "Cell 16 disconnection"
    ]
}