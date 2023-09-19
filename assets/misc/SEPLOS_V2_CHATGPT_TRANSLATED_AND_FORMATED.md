# I. Communication Instructions

The EMU11XX series of BMS products communicate with FSU, PC, or other upper controllers via RS485, using the MODBUS ASCII communication protocol as per the YD/T1363.3 specification.

## 1.1 Interface Setting

- EMU11XX series of BMS products use asynchronous serial communication interfaces.
- Start bit: 1
- Data bit: 8
- Stop bit: 1
- Check bit: None
- Default data transmission rate: 9600 BPS.

## 1.2 Interface Connection

Note: A 120Ω terminal matching resistor should be added to the starting and final points of the communication connection respectively.

## 1.3 Connection Mode

The communication between the supervision unit (SU) and the supervision module (SM) is a point-to-multipoint master-slave mode. SU calls SM using BMS DIP addresses:

- BMS DIP address 1
- BMS DIP address 2
- BMS DIP address 3
- ...
- BMS DIP address 15

SU issues commands to the called SM at the corresponding address, and the SM receives the command and returns the response information. If SU does not receive the response information from SM within 500ms or receives the wrong response information, the communication process is considered to have failed.

# II. Information Structure

Information is organized in a structured manner for correct transmission between SU and SM. Refer to Table 1 for information structure. Information is composed of multiple bytes, where one or more bytes form a unit, each having a name that represents its defined meaning. Additional details about the units in Table 1 can be found in Table 2. Furthermore, Table 3 provides comments on CID1 in Table 2, while Table 4 and Table 5 offer further comments on CID2 in Table 2.

## Table 1: List of Information Structures

| Items | SOI | VER | ADR | CID1 | CID2 | LENGTH | INFO | CHKSUM | EOI |
| ----- | --- | --- | --- | ---- | ---- | ------ | ---- | ------ | --- |
| ASCII byte | 1 | 2   | 2   | 2    | 2    | 4      | LENID | 4      | 1   |

## Table 2: Comments on Information Structures

| Items | Meaning | Remarks |
| ----- | ------- | ------- |
| Start code | Start code SOI: Starting of a data frame | SOI = 7EH (~) |
| Version code (high) | Version code VER: A communication protocol version code is composed of 2 ASCII codes | Protocol version V2.0 = 32H 30H |
| Version code (low) | - | - |
| Address code (high) | Address code ADR: A device address identification code is composed of 2 ASCII codes | 00-15 valid, Address 1 = 30H, Address 31H |
| Address code (low) | - | - |
| Device code (high) | Device code CID1: Battery | A device type identification code is composed of 2 ASCII codes | ID = 34H 36H |
| Device code (low) | - | - |
| Function code (high) | Function code CID2: The command code CMD sent by SU to SM or the return code RTN returned by SM to SU is composed of 2 ASCII codes | See CMD in "Table 4" for details, See RTN in "Table 5" for details |
| Function code (low) | - | - |
| Length code MSB | Length code LENGTH: Data information INFO length, including LENID and LCHKSUM | It is composed of 4 ASCII codes | See "3.2" for details |
| Length code 3 | - | - |
| Length code 2 | - | - |
| Length code LSB | - | - |
| Data code | Data*LEND | Data code INFO: Including Command data information COMMAND INFO sent by SU to SM, Response data information RTNDATA INFO returned by SM to SU | It is composed of "LENID" ASCII codes |
| Check code MSB | Check code CHKSUM: | It is composed of 4 ASCII codes | See "3.3" for details |
| Check code 3 | - | - |
| Check code 2 | - | - |
| Check code LSB | - | - |
| End code | End code EOI: Ending of a data frame | EOI = 0DH (CR) |

## Table 3: Device code CID1

| S/N | CID1 (HEX) | Device code Meaning                   |
| --- | ---------- | ------------------------------------ |
| 1   | 46H        | Lithium iron phosphate battery BMS  |
| ... | ...        | ...                                  |

## Table 4: Command code CID2

| S/N | CID2 (HEX) | Command code Meaning                     |
| --- | ---------- | ---------------------------------------- |
| 1   | 42H        | Acquisition of telemetering information |
| 2   | 44H        | Acquisition of telecommand information  |
| 3   | 45H        | Telecontrol command                       |
| 4   | 47H        | Acquisition of teleregulation information |
| 5   | 49H        | Setting of teleregulation information     |
| 6   | 4FH        | Acquisition of the communication protocol version number |
| 7   | 51H        | Acquisition of device vendor information |
| 8   | 4BH        | Acquisition of historical data            |
| 9   | 4DH        | Acquisition time                           |
| 10  | 4EH        | Synchronization time                      |
| 11  | A0H        | Production calibration                     |
| 12  | A1H        | Production setting                         |
| 13  | A2H        | Regular recording                          |

## Table 5: Return code CID2

| S/N | CID2 (HEX) | Command code Meaning                  |
| --- | ---------- | ------------------------------------- |
| 1   | 00H        | Normal                                |
| 2   | 01H        | VER error                             |
| 3   | 02H        | CHKSUM error                          |
| 4   | 03H        | LCHKSUM error                         |
| 5   | 04H        | CID2 invalid                          |
| 6   | 05H        | Command format error                  |
| 7   | 06H        | Data invalid (parameter setting)     |
| 8   | 07H        | No data (history)                     |
| 9   | E1H        | CID1 invalid                          |
| 10  | E2H        | Command execution failure             |
| 11  | E3H        | Device fault                          |
| 12  | E4H        | Invalid permissions                   |

# III. Data Format

## 3.1 Data Transmission Format

SOI and EOI are explained and transmitted in HEX. Other items are explained in HEX, transmitted in HEX-ASCII code, and each byte contains 2 ASCII codes. For example, CID2=4BH is transmitted in 2 bytes: 34H ('4' in ASCII code) and 42H ('B' in ASCII code).

## 3.2 LENGTH Format

### Table 6: LENGTH Format

| Length check code LCHKSUM | LENID (number of bytes of ASCII code in INFO) |
| ------------------------ | ---------------------------------------------- |
| D15 D14 D13 D12 D11 D10 D9 D8 D7 D6 D5 D4 D3 D2 D1 D0                        |

- LENID represents the number of bytes of ASCII code in INFO. When LENID is equal to 0, INFO is null, meaning this item does not exist. LENID has only 12 bits, so the data package cannot exceed 4,095 bytes.

- To calculate LCHKSUM: D11D10D9D8+D7D6D5D4+D3D2D1D0, sum them up, mod 16, take the remainder, do a bitwise invert, and then add 1. For example, if the number of bytes of ASCII code in INFO is 18, then LENID=0000 0001 0010B. D11D10D9D8+D7D6D5D4+D3D2D1D0=0000B+0001B+0010B=0011B, mod 16, remainder=0011B, do a bitwise invert, and add 1=1101B, then LCHKSUM=1101B.

- LENGTH (in 3.2.2): 1101 0000 0001 0010B = D012H. For LENGTH transmission, HIGH byte first, then LOW byte, and it is divided into 4 ASCII codes.

## 3.3 CHKSUM Format

To calculate CHKSUM, except for SOI, EOI, and CHKSUM, add values to get the sum of other characters in ASCII code, then mod 65536, take the remainder, do a bitwise invert, and then add 1. For example, in the information frame “~1203400456ABCEFEFC72CR”, CHKSUM=‘1’+‘2’+‘0’+...+‘F’+‘E’=31H+32H+30H+...+46H+45H=038EH, mod 65536, remainder=038EH, do a bitwise invert, and add 1= FC72H. For CHKSUM transmission, HIGH byte first, then LOW byte, and it is divided into 4 ASCII codes.

# IV. Communication Commands

## 4.1 Telemetry Commands

### 4.1.1 Telemetry Command Frame

- CID2=42H
- INFO is 1 byte COMMAND_GROUP.

Example COMMAND_GROUP values:
- COMMAND_GROUP=0x01, acquire data of battery group 1
- COMMAND_GROUP=0x02, acquire data of battery group 2
- ...
- COMMAND_GROUP=0xFF, acquire data of all battery groups

Note: GROUP=0xFF is only for RS232, not for RS485. In RS485 communication, SM checks whether the received COMMAND_GROUP matches the DIP address. In RS232 communication, COMMAND_GROUP is used to identify the number of SU addressing multi-group parallel batteries.

Example: VER=20H and CID1=46H. Telemetry commands for different addresses are shown in Table 7.

### Table 7: Telemetry Command Examples

| Address | Telemetry Command Info Frame (ASCII)                        |
| ------- | -------------------------------------------------------- |
| 00      | 7E 32 30 30 30 34 36 34 32 45 30 30 32 30 30 46 44 33 37 0D |
| 01      | 7E 32 30 30 31 34 36 34 32 45 30 00 32 30 31 46 44 33 35 0D |
| 02      | 7E 32 30 30 32 34 36 34 32 45 30 00 32 30 32 46 44 33 33 0D |
| 03      | 7E 32 30 30 33 34 36 34 32 45 30 00 32 30 33 46 44 33 31 0D |
| 04      | 7E 32 30 30 34 34 36 34 32 45 30 00 32 30 34 46 44 32 46 0D |
| 05      | 7E 32 30 30 35 34 36 34 32 45 30 00 32 30 35 46 44 32 44 0D |
| 06      | 7E 32 30 30 36 34 36 34 32 45 30 00 32 30 36 46 44 32 42 0D |
| 07      | 7E 32 30 30 37 34 36 34 32 45 30 00 32 30 37 46 44 32 39 0D |
| 08      | 7E 32 30 30 38 34 36 34 32 45 30 00 32 30 38 46 44 32 37 0D |
| 09      | 7E 32 30 30 39 34 36 34 32 45 30 00 32 30 39 46 44 32 35 0D |
| 10      | 7E 32 30 30 41 34 36 34 32 45 30 00 32 30 41 46 44 31 35 0D |
| 11      | 7E 32 30 30 42 34 36 34 32 45 30 00 32 30 42 46 44 31 33 0D |
| 12      | 7E 32 30 30 43 34 36 34 32 45 30 00 32 30 43 46 44 31 31 0D |
| 13      | 7E 32 30 30 44 34 36 34 32 45 30 00 32 30 44 46 44 30 46 0D |
| 14      | 7E 32 30 30 45 34 36 34 32 45 30 00 32 30 45 46 44 30 44 0D |
| 15      | 7E 32 30 30 46 34 36 34 32 45 30 00 32 30 46 46 44 30 42 0D |

### 4.1.2 Telemetry Return Frame

- CID2=00H, INFO is 75 bytes. See Table 8 and Table 9 for data content and conversion respectively.

#### Table 8: Comments on Telemetry Return

(For brevity, only a few columns are shown here.)

| S/N | Content                             | Number of bytes (HEX) |
| --- | ----------------------------------- | --------------------- |
| 1   | DATA FLAG                           | 1                     |
| 2   | COMMAND GROUP                       | 1                     |
| 3   | Number of cells M=16                | 1                     |
| ... | Voltage of Cell 1 (mV)              | 2                     |
| ... | Voltage of Cell M (mV)              | 2                     |
| 4   | Number of temperatures N=6          | 1                     |
| ... | Cell temperature 1 (0.1℃)           | 2                     |
| ... | Cell temperature 2 (0.1℃)           | 2                     |
| ... | Environment temperature (0.1℃)      | 2                     |
| ... | Power temperature (0.1℃)            | 2                     |
| 5   | Charge/discharge current (0.01A)    | 2                     |
| 6   | Total battery voltage (0.01V)       | 2                     |
| ... | Residual capacity (0.01Ah)          | 2                     |
| 7   | Custom number P=10                  | 1                     |
| ... | Battery capacity (0.01Ah)           | 2                     |
| ... | SOC (1‰)                            | 2                     |
| ... | Rated capacity (0.01Ah)             | 2                     |
| ... | Number of cycles                    | 2                     |
| ... | SOH (1‰)                            | 2                     |
| ... | Port voltage (0.01V)                | 2                     |
| ... | Reservation                          | 2                     |

#### Table 9: Methods of Data Conversion

(For brevity, only a few data conversions are shown here.)

| Temperature    | Unsigned integer, in 0.1K. Actual value = (transmission value - 2731) / 10(℃). E.g., 3032 means (3032 - 2731) / 10(℃) = 30.1℃ |
| Total current  | Signed integer, in A. Actual value = transmission value / 100(A). E.g., 4500 means 45.00 A                                     |
| Total voltage  | Unsigned integer, in V. Actual value = transmission value / 100(V). E.g., 5400 means 54.00 V                                 |
| Capacity       | Unsigned integer, in Ah. Actual value = transmission value / 100(Ah). E.g., 4830 means 48.30 Ah                               |

### 4.2 Telecommands

#### 4.2.1 Telecommand Frame

- CID2=44H, INFO is 1 byte COMMAND_GROUP.
- COMMAND_GROUP=0x01: Acquire data of battery group 1
- COMMAND_GROUP=0x02: Acquire data of battery group 2
- ...
- COMMAND_GROUP=0xFF: Acquire data of all battery groups (only for RS232, not for RS485).

#### Table 10: Telecommand Examples

| Address | Telecommand Info Frame (ASCII)                        |
| ------- | ---------------------------------------------------- |
| 00      | 7E 32 30 30 30 34 36 34 34 45 30 30 32 30 30 46 44 33 35 0D |
| 01      | 7E 32 30 30 31 34 36 34 34 45 30 30 32 30 31 46 44 33 33 0D |
| 02      | 7E 32 30 30 02 34 36 34 34 45 30 30 32 30 32 46 44 33 31 0D |
| 03      | 7E 32 30 30 03 34 36 34 34 45 30 30 32 30 33 46 44 32 46 0D |
| 04      | 7E 32 30 30 04 34 36 34 34 45 30 30 32 30 34 46 44 32 44 0D |
| 05      | 7E 32 30 30 05 34 36 34 34 45 30 30 32 30 35 46 44 32 42 0D |
| 06      | 7E 32 30 30 06 34 36 34 34 45 30 30 32 30 36 46 44 32 39 0D |
| 07      | 7E 32 30 30 07 34 36 34 34 45 30 30 32 30 37 46 44 32 37 0D |
| 08      | 7E 32 30 30 08 34 36 34 34 45 30 30 32 30 38 46 44 32 35 0D |
| 09      | 7E 32 30 30 09 34 36 34 34 45 30 30 32 30 39 46 44 32 33 0D |
| 10      | 7E 32 30 30 0A 34 36 34 34 45 30 30 32 30 41 46 44 31 33 0D |
| 11      | 7E 32 30 30 0B 34 36 34 34 45 30 30 32 30 42 46 44 31 31 0D |
| 12      | 7E 32 30 30 0C 34 36 34 34 45 30 30 32 30 43 46 44 30 46 0D |
| 13      | 7E 32 30 30 0D 34 36 34 34 45 30 30 32 30 44 46 44 30 44 0D |
| 14      | 7E 32 30 30 0E 34 36 34 34 45 30 30 32 30 45 46 44 30 42 0D |
| 15      | 7E 32 30 30 0F 34 36 34 34 45 30 30 32 30 46 46 44 30 39 0D |

### 4.2.2 Telecommand Return Frame

- CID2=00H, INFO is 49 bytes. Please refer to Table 11 for INFO data, Table 12 for the meaning of 24-byte alarms, and Table 13 for the meaning of 20-bit alarms.

#### Table 11: Comments on Telecommand Return

| S/N | Content                    | Number of bytes (HEX) |
| --- | -------------------------- | --------------------- |
| 1   | DATA FLAG                  | 1                     |
| 2   | COMMAND GROUP              | 1                     |
| 3   | Number of cells M=16       | 1                     |
| ... | Cell 1 alarm 1             | 1                     |
| ... | Cell 2 alarm 1             | 1                     |
| ... | Cell M alarm 1             | 1                     |
| 4   | Number of temperatures N=6 | 1                     |
| ... | Cell temperature alarm 1   | 1                     |
| ... | Cell temperature alarm 2   | 1                     |
| ... | Cell temperature alarm 3   | 1                     |
| ... | Cell temperature alarm 4   | 1                     |
| ... | Environment temperature alarm 1 | 1                |
| ... | Power temperature alarm 1  | 1                     |
| 5   | Charge/discharge current alarm 1 | 1                |
| 6   | Total battery voltage alarm 1 | 1                   |
| 7   | Number of custom alarms P=20 | 1                    |
| ... | Alarm event 1              | 1                     |
| ... | Alarm event 2              | 1                     |
| ... | Alarm event 3              | 1                     |
| ... | Alarm event 4              | 1                     |
| ... | Alarm event 5              | 1                     |
| ... | Alarm event 6              | 1                     |
| ... | On-off state               | 1                     |
| ... | Equilibrium state 1        | 1                     |
| ... | Equilibrium state 2        | 1                     |
| ... | System state               | 1                     |
| ... | Disconnection state 1      | 1                     |
| ... | Disconnection state 2      | 1                     |
| ... | Alarm event 7              | 1                     |
| ... | Alarm event 8              | 1                     |
| ... | Reservation extension 1    | 1                     |
| ... | Reservation extension 2    | 1                     |
| ... | Reservation extension 3    | 1                     |
| ... | Reservation extension 4    | 1                     |
| ... | Reservation extension 5    | 1                     |
| ... | Reservation extension 6    | 1                     |
| ... | Reservation extension 7    | 1                     |
| ... | Reservation extension 8    | 1                     |
| ... | Reservation extension 9    | 1                     |
| ... | Reservation extension 10   | 1                     |
| ... | Reservation extension 11   | 1                     |
| ... | Reservation extension 12   | 1                     |
| ... | Reservation extension 13   | 1                     |
| ... | Reservation extension 14   | 1                     |
| ... | Reservation extension 15   | 1                     |
| ... | Reservation extension 16   | 1                     |
| ... | Reservation extension 17   | 1                     |
| ... | Reservation extension 18   | 1                     |
| ... | Reservation extension 19   | 1                     |
| ... | Reservation extension 20   | 1                     |

#### Table 12: Comments on Byte Alarms

| S/N | Alarm Value | Meaning                 |
| --- | ----------- | ----------------------- |
| 1   | 0x00        | Normal, no alarm        |
| 2   | 0x01        | Alarm at lower limit    |
| 3   | 0x02        | Alarm at upper limit    |
| 4   | 0xF0        | Other alarms            |

#### Table 13: Comments on Bit Alarms

| Alarm Event | Flag Bit Information (1: Trigger, 0: Normal) |
| ----------- | -------------------------------------------- |
| 1           | Voltage sensor fault                          |
| 2           | Temperature sensor fault                      |
| 3           | Current sensor fault                          |
| 4           | Key switch fault                              |
| 5           | Cell voltage dropout fault                    |
| 6           | Charge switch fault                           |
| 7           | Discharge switch fault                        |
| 8           | Current limit switch fault                    |
| 9           | Monomer high voltage alarm                    |
| 10          | Monomer overvoltage protection                |
| 11          | Monomer low voltage alarm                     |
| 12          | Monomer under voltage protection              |
| 13          | High voltage alarm for total voltage          |
| 14          | Overvoltage protection for total voltage      |
| 15          | Low voltage alarm for total voltage           |
| 16          | Under voltage protection for total voltage    |
| 17          | Charge high temperature alarm                 |
| 18          | Charge over temperature protection             |
| 19          | Charge low temperature alarm                  |
| 20          | Charge under temperature protection           |
| 21          | Discharge high temperature alarm               |
| 22          | Discharge over temperature protection           |
| 23          | Discharge low temperature alarm                |
| 24          | Discharge under temperature protection         |
| 25          | Environment high temperature alarm            |
| 26          | Environment over temperature protection        |
| 27          | Environment low temperature alarm             |
| 28          | Environment under temperature protection      |
| 29          | Power over temperature protection              |
| 30          | Power high temperature alarm                   |
| 31          | Cell low temperature heating                  |
| 32          | Charge over current alarm                     |
| 33          | Charge over current protection                 |
| 34          | Discharge over current alarm                   |
| 35          | Discharge over current protection               |
| 36          | Transient over current protection               |
| 37          | Output short circuit protection                |
| 38          | Transient over current lockout                 |
| 39          | Output short circuit lockout                   |
| 40          | Charge high voltage protection                 |
| 41          | Intermittent recharge waiting                 |
| 42          | Residual capacity alarm                       |
| 43          | Residual capacity protection                   |
| 44          | Cell low voltage charging prohibition          |
| 45          | Output reverse polarity protection             |
| 46          | Output connection fault                        |
| 47          | Inside bit                                    |
| 48          | Inside bit                                    |
| 49          | Inside bit                                    |
| 50          | Inside bit                                    |
| 51          | Automatic charging waiting                   |
| 52          | Manual charging waiting                       |
| 53          | Inside bit                                    |
| 54          | Inside bit                                    |
| 55          | EEP storage fault                            |
| 56          | RTC error                                    |
| 57          | Voltage calibration not performed            |
| 58          | Current calibration not performed            |
| 59          | Zero calibration not performed               |
| 60          | Inside bit                                    |
| 61          | Inside bit                                    |
| 62          | Inside bit                                    |
| 63          | Inside bit                                    |
| 64          | Reservation extension 1                      |
| 65          | Reservation extension 2                      |
| 66          | Reservation extension 3                      |
| 67          | Reservation extension 4                      |
| 68          | Reservation extension 5                      |
| 69          | Reservation extension 6                      |
| 70          | Reservation extension 7                      |
| 71          | Reservation extension 8                      |
| 72          | Reservation extension 9                      |
| 73          | Reservation extension 10                     |
| 74          | Reservation extension 11                     |
| 75          | Reservation extension 12                     |
| 76          | Reservation extension 13                     |
| 77          | Reservation extension 14                     |
| 78          | Reservation extension 15                     |
| 79          | Reservation extension 16                     |
| 80          | Reservation extension 17                     |
| 81          | Reservation extension 18                     |
| 82          | Reservation extension 19                     |
| 83          | Reservation extension 20                     |

