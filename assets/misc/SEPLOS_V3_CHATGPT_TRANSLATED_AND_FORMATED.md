# SEPLOS-3.0RS485BMS ModbusRTUProtocol

---

## BMS Modbus RTU Protocol
- Port Support: RS485
- Hardware BMS: BMS48100/48200
- Version: V0.1
- Date: 2023/02/09

---

## Revision History
- 0 Document created V0.1 2023-02-09

---

## 1. Communication Parameters
### 1.1 Configuration:
- Baud Rate: 19200
- Parity bit: No
- Data Bits: 8
- Stop Bit: 1

### 1.2 Port features:
- RS485: BMS response which is self address only.

---

## 2. Frame Format of Communication Data
### 2.1.1 List of function code supported:
| Function code | Meaning          | Notes              |
|---------------|------------------|--------------------|
| 0X01          | Read Coil status | Supported data block PIC/EIC |
| 0X0F          | Write Coil status | Supported data block PIA/PIB/EIA/EIB/PCT |
| 0X10          | Write command    |                     |

### 2.1.2 Device supported:
| Device Name | Device Id   | Supported data block |
|-------------|-------------|-----------------------|
| BMS         | 0X00~0X7F   | PIA/PIB/PIC           |
| EMS         | 0XB0~0XBF   |                       |
| ECU         | 0XC0        | EIA/EIB/EIC           |
| 2.4’or 5’or7’ TFT/LCD | 0XE0 | PIA/PIB/PIC   |
| Bluetooth   | 0XE0/0X00~0X10/0XC0 | PIA/PIB/PIC/EIA/EIB/EIC/PCT |

### 2.2 0X04 Command
#### 2.2.1 Host node sending
| Item | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|------|---|---|---|---|---|---|---|---|
| Field definition | ADDR | CMD | MSB | LSB | MSB | LSB | LSB | MSB |
| Explanation | BMS address | Type of command(0x04) | Beginning register number | CRC |

#### 2.2.2 Slave node Normal response
| Item | 0 | 1 | 2 | 3 | 4... | 3+2n | 4+2n |
|------|---|---|---|---|------|------|------|
| Field definition | ADDR | CMD | Length | ... | LSB | MSB |
| Explanation | BMS address | Type of command | 2n register value... | CRC |

### 2.3 0X10 Command
#### 2.3.1 Host node sending
| Item | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8... | 7+2n | 8+2n |
|------|---|---|---|---|---|---|---|---|------|------|------|
| Field definition | ADDR | CMD | MSB | LSB | MSB | LSB | Length | ... | LSB | MSB |
| Explanation | BMS address | Type of command(0x10) | Beginning register address | Resister number n | 2n Resister Value ... | CRC |

#### 2.3.2 Slave node Normal response
| Item | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|------|---|---|---|---|---|---|---|---|
| Field definition | ADDR | CMD | MSB | LSB | MSB | LSB | LSB | MSB |
| Explanation | BMS address | Type of command | Beginning register address | Resister number n | CRC |

### 2.4 0X01 Command
#### 2.4.1 Host node sending
| Item | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|------|---|---|---|---|---|---|---|---|
| Field definition | ADDR | CMD | MSB | LSB | MSB | LSB | LSB | MSB |
| Explanation | BMS address | Type of command(0x01) | Beginning coil address | Bits number n | CRC |

#### 2.4.2 Slave node Normal response
| Item | 0 | 1 | 2 | 3... | 4+N | 5+N |
|------|---|---|---|------|------|------|
| Field definition | ADDR | CMD | Length | ... | LSB | MSB |
| Explanation | BMS address | Type of Bytes | Coil value... | Byte length N: For requests, it indicates the number of bits, while for responses, it represents the number of bytes, with any extra space filled with zeros. | Coil CRC |

### 2.5 0X0F Command
#### 2.5.1 Host node sending
| Item | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8+N | 9+N |
|------|---|---|---|---|---|---|---|---|------|------|
| Field definition | ADDR | CMD | MSB | LSB | MSB | LSB | Length | ... | LSB | MSB |
| Explanation | BMS address | Type of command(0x0F) | Beginning coil address | Bits number n | Bytes number N | Coil Value... | CRC |

#### 2.5.2 Slave node Normal response
| Item | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|------|---|---|---|---|---|---|---|---|
| Field definition | ADDR | CMD | MSB | LSB | MSB | LSB | LSB | MSB |
| Explanation | BMS address | Type of command | Beginning coil address | Bits number n | CRC |

### 2.6 Error Code
#### 2.6.1 Abnormal response of format from slave node
| Item | 0 | 1 | 2 | 3 | 4 |
|------|---|---|---|---|---|
| Field definition | ADDR | CMD+128 | Err Code | LSB | MSB |
| Explanation | Controller address | Type of command +128 | Error Code | CRC parity |

#### 2.6.2 Error code defined
| Error Code | Defined | Notes |
|------------|---------|-------|
| 0x01 | Illegal function | Function that does not supported |
| 0x02 | Illegal data address | Register address that does not supported |
| 0x03 | Illegal data value | Data value is not allowed |
| 0x04 | Slave device failure | Device failure |
| 0x05 | Acknowledge | Processing is taking too long |
| 0x06 | Slave device busy | Device is busy |
| 0x08 | Memory Parity Error | Memory check error |
| 0x0A | Gateway Path Unavailable | Gateway path error |

---

TA01: Relative Address Name R/W Data type Bytes Unit
| Relative Address | Name                        | R/W | Data Type | Bytes | Unit   |
|------------------|-----------------------------|-----|-----------|-------|--------|
| 1000             | Pack Voltage                | R   | UINT16    | 2     | 10mV   |
| 1001             | Current                     | R   | INT16     | 2     | 10mA   |
| 1002             | Remaining capacity          | R   | UINT16    | 2     | 10mAH  |
| 1003             | Total Capacity              | R   | UINT16    | 2     | 10mAH  |
| 1004             | Total Discharge Capacity    | R   | UINT16    | 2     | 10AH   |
| 1005             | SOC                         | R   | UINT16    | 2     | 0.1%   |
| 1006             | SOH                         | R   | UINT16    | 2     | 0.1%   |
| 1007             | Cycle                       | R   | UINT16    | 2     | 1      |
| 1008             | Average of Cell Voltage     | R   | UINT16    | 2     | 1mV    |
| 1009             | Average of Cell Temperature | R   | UINT16    | 2     | 0.1K   |
| 100A             | Max Cell Voltage            | R   | UINT16    | 2     | 1mV    |
| 100B             | Min Cell Voltage            | R   | UINT16    | 2     | 1mV    |
| 100C             | Max Cell Temperature        | R   | UINT16    | 2     | 0.1K   |
| 100D             | Min Cell Temperature        | R   | UINT16    | 2     | 0.1K   |
| 100E             | Reserved                    |     |           |       |        |
| 100F             | Max Discharge Current       | R   | UINT16    | 2     | 1A     |
| 1010             | Max Charge Current          | R   | UINT16    | 2     | 1A     |

| Pack Info. B(电池信息 PIB)                 |                      |     |         |       |        |
|-----------------------------------------|----------------------|-----|---------|-------|--------|
| 1100                                    | Cell1 Voltage         | R   | UINT16  | 2     | 1mV    |
| 1101                                    | Cell2 Voltage         | R   | UINT16  | 2     | 1mV    |
| 1102                                    | Cell3 Voltage         | R   | UINT16  | 2     | 1mV    |
| 1103                                    | Cell4 Voltage         | R   | UINT16  | 2     | 1mV    |
| 1104                                    | Cell5 Voltage         | R   | UINT16  | 2     | 1mV    |
| 1105                                    | Cell6 Voltage         | R   | UINT16  | 2     | 1mV    |
| 1106                                    | Cell7 Voltage         | R   | UINT16  | 2     | 1mV    |
| 1107                                    | Cell8 Voltage         | R   | UINT16  | 2     | 1mV    |
| 1108                                    | Cell9 Voltage         | R   | UINT16  | 2     | 1mV    |
| 1109                                    | Cell10 Voltage        | R   | UINT16  | 2     | 1mV    |
| 110A                                    | Cell11 Voltage        | R   | UINT16  | 2     | 1mV    |
| 110B                                    | Cell12 Voltage        | R   | UINT16  | 2     | 1mV    |
| 110C                                    | Cell13 Voltage        | R   | UINT16  | 2     | 1mV    |
| 110D                                    | Cell14 Voltage        | R   | UINT16  | 2     | 1mV    |
| 110E                                    | Cell15 Voltage        | R   | UINT16  | 2     | 1mV    |
| 110F                                    | Cell16 Voltage        | R   | UINT16  | 2     | 1mV    |
| 1110                                    | Cell temperature 1    | R   | UINT16  | 2     | 0.1K   |
| 1111                                    | Cell temperature 2    | R   | UINT16  | 2     | 0.1K   |
| 1112                                    | Cell temperature 3    | R   | UINT16  | 2     | 0.1K   |
| 1113                                    | Cell temperature 4    | R   | UINT16  | 2     | 0.1K   |
| 1118                                    | Environment Temperature| R   | UINT16  | 2     | 0.1K   |
| 1119                                    | Power temperature      | R   | UINT16  | 2     | 0.1K   |

| Pack Info. C(电池信息 PIC)                |                        |     |           |       |        |
|------------------------------------------|------------------------|-----|-----------|-------|--------|
| 1200                                     | Cells voltage 08-01low alarm state         | R | HEX  | 1  | 1:alarm |
| 1208                                     | Cells voltage 16-09low alarm state         | R | HEX  | 1  | 1:alarm |
| 1210                                     | Cells voltage 08-01high alarm state        | R | HEX  | 1  | 1:alarm |
| 1218                                     | Cells voltage 16-09high alarm state        | R | HEX  | 1  | 1:alarm |
| 1220                                     | Cell 08-01 temperature Tlow alarm state    | R | HEX  | 1  | 1:alarm |
| 1228                                     | Cell 08-01 temperature high alarm state   | R | HEX  | 1  | 1:alarm |
| 1230                                     | Cell 08-01 equalization event code         | R | HEX  | 1  | 1:on   0:off |
| 1238                                     | Cell 16-09 equalization event code         | R | HEX  | 1  | 1:on   0:off |
| 1240                                     | System state code                          | R | HEX  | 1  | See TB09 |
| 1248                                     | Voltage event code                         | R | HEX  | 1  | See TB02 |
| 1250                                     | Cells Temperature event code               | R | HEX  | 1  | See TB03 |
| 1258                                     | Environment and power Temperature event code| R | HEX | 1 | See TB04 |
| 1260                                     | Current event code1                        | R | HEX  | 1  | See TB05 |
| 1268                                     | Current event code2                        | R | HEX  | 1  | See TB16 |
| 1270                                     | The residual capacity code                 | R | HEX  | 1  | See TB06 |
| 1278                                     | The FET event code                         | R | HEX  | 1  | See TB07 |
| 1280                                     | Battery equalization state code            | R | HEX  | 1  | See TB08 |
| 1288                                     | Hard fault event code                      | R | HEX  | 1  | See TB15 |

| PCS Control(版本信息 (PCT))  | Protocol type Switch       | R/W | UINT16 | 2     |
|-----------------------------|-----------------------------|-----|--------|-------|
| 1800                        | PCS Protocol type Switch   | R/W | UINT16 | 2     |
| 1801                        | PCS baud rate              | R   | UINT16 | 2     | Kbps/bps |
| 1802                        | PCS name                   | R   | ASCII  | 32    |
| 1812                        | Protocol support name      | R   | ASCII  | 32    |
| 1822                        | Protocol version           | R   | ASCII  | 2     |
| 1823                        | PCS Protocol pre Switch    | R/W | UINT16 | 2     |

| EMS Info.A(系统信息 EIA)     | Name                        | R   | Data Type | Bytes | Unit   |
|-----------------------------|-----------------------------|-----|-----------|-------|--------|
| 2000                        | Pack Voltage                | R   | UINT32    | 4     | 10mV   |
| 2002                        | Current                     | R   | INT32     | 4     | 100mA  |
| 2004                        | Remaining capacity          | R   | UINT32    | 4     | 10mAH  |
| 2006                        | Total Capacity              | R   | UINT32    | 4     | 10mAH  |
| 2008                        | Total Discharge Capacity    | R   | UINT32    | 4     | 10AH   |
| 200A                        | Rated Capacity              | R   | UINT32    | 4     | 10mAH  |
| 200C                        | Online Pack Flag            | R   | UINT32    | 4     |
| 200E                        | Protected Pack bit          | R   | UINT32    | 4     |
| 2010                        | Max Discharge Current       | R   | UINT32    | 4     | 100mA  |
| 2012                        | Max Charge Current          | R   | UINT32    | 4     | 100mA  |
| 2014                        | Suggest Pack OV             | R   | UINT16    | 2     | 100mV  |
| 2015                        | Suggest Pack UV             | R   | UINT16    | 2     | 100mV  |
| 2016                        | System Pack No.             | R   | UINT16    | 2     |
| 2017                        | Cycle                       | R   | UINT16    | 2     |
| 2018                        | SOC                         | R   | UINT16    | 2     | 0.1%   |
| 2019                        | SOH                         | R   | UINT16    | 2     | 0.1%   |

| EMS Info. B(系统信息 EIB)    | Name                        | R   | Data Type | Bytes | Unit   |
|-----------------------------|-----------------------------|-----|-----------|-------|--------|
| 2100                        | Max Cell Voltage            | R   | UINT16    | 2     | 1mV    |
| 2101                        | Min Cell Voltage            | R   | UINT16    | 2     | 1mV    |
| 2102                        | Max Cell Voltage Id         | R   | UINT16    | 2     |
| 2103                        | Min Cell Voltage Id         | R   | UINT16    | 2     |
| 2104                        | Max Pack Voltage            | R   | UINT16    | 2     | 10mV   |
| 2105                        | Min Pack Voltage            | R   | UINT16    | 2     | 10mV   |
| 2106                        | Max Cell Temperature        | R   | INT16     | 2     | 1℃     |
| 2107                        | Min Cell Temperature        | R   | INT16     | 2     | 1℃     |
| 2108                        | Avg Cell Temperature        | R   | INT16     | 2     | 1℃     |
| 2109                        | Max Cell Temperature Id     | R   | UINT16    | 2     |
| 210A                        | Min Cell Temperature Id     | R   | UINT16    | 2     |
| 210B                        | Max Pack Power temperature  | R   | INT16     | 2     | 1℃     |
| 210C                        | Min Pack Power temperature  | R   | INT16     | 2     | 1℃     |
| 210D                        | Avg Pack Power temperature  | R   | INT16     | 2     | 1℃     |
| 210E                        | Max Pack Power temperature Id | R | INT16   | 2     |
| 210F                        | Min Pack Power temperature Id | R | INT16   | 2     |
| 2110                        | Max Pack Soc                | R   | UINT16    | 2     | 0.1%   |
| 2111                        | Min Pack Soc                | R   | UINT16    | 2     | 0.1%   |
| 2112                        | Max Pack Cycle              | R   | UINT16    | 2     |
| 2113                        | Max Pack Soh                | R   | UINT16    | 2     | 0.1%   |

| EMS Info. C(系统信息 EIC)     | Name                        | R   | Data Type | Bytes | Unit   |
|------------------------------|-----------------------------|-----|-----------|-------|--------|
| 2200                         | System state code           | R   | HEX       | 1     | See TB09 |
| 2208                         | Voltage event code          | R   | HEX       | 1     | See TB02 |
| 2210                         | Cells Temperature event code| R | HEX       | 1     | See TB03 |
| 2218                         | Environment and power Temperature event code| R | HEX | 1 | See TB04 |
| 2220                         | Current event code1         | R   | HEX       | 1     | See TB05 |
| 2228                         | Current event code2         | R   | HEX       | 1     | See TB16 |
| 2230                         | The residual capacity code  | R   | HEX       | 1     | See TB06 |
| 2238                         | The FET event code          | R   | HEX       | 1     | See TB07 |
| 2240                         | Battery equalization state code| R | HEX    | 1     | See TB08 |
| 2248                         | Hard fault event code       | R   | HEX       | 1     | See TB15 |

| TB02:                        | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
|-----------------------------|-------------------------------------------------|------|------|------|------|------|------|------|------|
| INDEX                       | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
| 2100                        | Max Cell Voltage                                | 1    |      |      |      |      |      |      |      |
| 2101                        | Min Cell Voltage                                |      | 1    |      |      |      |      |      |      |
| 2102                        | Max Cell Voltage Id                             |      |      | 1    |      |      |      |      |      |
| 2103                        | Min Cell Voltage Id                             |      |      |      | 1    |      |      |      |      |
| 2104                        | Max Pack Voltage                                |      |      |      |      | 1    |      |      |      |
| 2105                        | Min Pack Voltage                                |      |      |      |      |      | 1    |      |      |
| 2106                        | Max Cell Temperature                            | 1    |      |      |      |      |      |      |      |
| 2107                        | Min Cell Temperature                            |      | 1    |      |      |      |      |      |      |
| 2108                        | Avg Cell Temperature                            |      |      | 1    |      |      |      |      |      |
| 2109                        | Max Cell Temperature Id                         |      |      |      | 1    |      |      |      |      |
| 210A                        | Min Cell Temperature Id                         |      |      |      |      | 1    |      |      |      |
| 210B                        | Max Pack Power temperature                      | 1    |      |      |      |      |      |      |      |
| 210C                        | Min Pack Power temperature                      |      | 1    |      |      |      |      |      |      |
| 210D                        | Avg Pack Power temperature                      |      |      | 1    |      |      |      |      |      |
| 210E                        | Max Pack Power temperature Id                   |      |      |      | 1    |      |      |      |      |
| 210F                        | Min Pack Power temperature Id                   |      |      |      |      | 1    |      |      |      |
| 2110                        | Max Pack Soc                                    | 1    |      |      |      |      |      |      |      |
| 2111                        | Min Pack Soc                                    |      | 1    |      |      |      |      |      |      |
| 2112                        | Max Pack Cycle                                  | 1    |      |      |      |      |      |      |      |
| 2113                        | Max Pack Soh                                    | 1    |      |      |      |      |      |      |      |

| TB03:                        | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
|-----------------------------|-------------------------------------------------|------|------|------|------|------|------|------|------|
| INDEX                       | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
| 2106                        | Max Pack Voltage Id                             |      |      | 1    |      |      |      |      |      |
| 2107                        | Min Pack Voltage Id                             |      |      |      | 1    |      |      |      |      |
| 2108                        | Max Cell Temperature                            | 1    |      |      |      |      |      |      |      |
| 2109                        | Min Cell Temperature                            |      | 1    |      |      |      |      |      |      |
| 210A                        | Avg Cell Temperature                            |      |      | 1    |      |      |      |      |      |
| 210B                        | Max Cell Temperature Id                         |      |      |      | 1    |      |      |      |      |
| 210C                        | Min Cell Temperature Id                         |      |      |      |      | 1    |      |      |      |
| 210D                        | Max Pack Power temperature                      | 1    |      |      |      |      |      |      |      |
| 210E                        | Min Pack Power temperature                      |      | 1    |      |      |      |      |      |      |
| 210F                        | Avg Pack Power temperature                      |      |      | 1    |      |      |      |      |      |
| 210F                        | Max Pack Power temperature Id                   |      |      |      | 1    |      |      |      |      |
| 210F                        | Min Pack Power temperature Id                   |      |      |      |      | 1    |      |      |      |
| 2112                        | Max Pack Cycle                                  | 1    |      |      |      |      |      |      |      |
| 2113                        | Max Pack Soh                                    | 1    |      |      |      |      |      |      |      |

| TB04:                        | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
|-----------------------------|-------------------------------------------------|------|------|------|------|------|------|------|------|
| INDEX                       | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
| 210B                        | Max Pack Power temperature                      | 1    |      |      |      |      |      |      |      |
| 210C                        | Min Pack Power temperature                      |      | 1    |      |      |      |      |      |      |
| 210D                        | Avg Pack Power temperature                      |      |      | 1    |      |      |      |      |      |
| 210E                        | Max Pack Power temperature Id                   |      |      |      | 1    |      |      |      |      |
| 210F                        | Min Pack Power temperature Id                   |      |      |      |      | 1    |      |      |      |
| 2110                        | Max Pack Soc                                    | 1    |      |      |      |      |      |      |      |
| 2111                        | Min Pack Soc                                    |      | 1    |      |      |      |      |      |      |
| 2112                        | Max Pack Cycle                                  | 1    |      |      |      |      |      |      |      |
| 2113                        | Max Pack Soh                                    | 1    |      |      |      |      |      |      |      |

| TB05:                        | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
|-----------------------------|-------------------------------------------------|------|------|------|------|------|------|------|------|
| INDEX                       | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
| 2200                        | System state code                               | 1    |      |      |      |      |      |      |      |
| 2208                        | Voltage event code                              | 1    |      |      |      |      |      |      |      |
| 2210                        | Cells Temperature event code                    | 1    |      |      |      |      |      |      |      |
| 2218                        | Environment and power Temperature event code    | 1    |      |      |      |      |      |      |      |
| 2220                        | Current event code1                             | 1    |      |      |      |      |      |      |      |
| 2228                        | Current event code2                             | 1    |      |      |      |      |      |      |      |
| 2230                        | The residual capacity code                      | 1    |      |      |      |      |      |      |      |
| 2238                        | The FET event code                              | 1    |      |      |      |      |      |      |      |
| 2240                        | Battery equalization state code                 | 1    |      |      |      |      |      |      |      |
| 2248                        | Hard fault event code                           | 1    |      |      |      |      |      |      |      |

| TB06:                        | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
|-----------------------------|-------------------------------------------------|------|------|------|------|------|------|------|------|
| INDEX                       | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
| 2230                        | The residual capacity code                      | 1    |      |      |      |      |      |      |      |
| 2240                        | Battery equalization state code                 | 1    |      |      |      |      |      |      |      |
| 2248                        | Hard fault event code                           | 1    |      |      |      |      |      |      |      |

| TB07:                        | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
|-----------------------------|-------------------------------------------------|------|------|------|------|------|------|------|------|
| INDEX                       | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
| 2238                        | The FET event code                              | 1    |      |      |      |      |      |      |      |
| 2240                        | Battery equalization state code                 | 1    |      |      |      |      |      |      |      |
| 2248                        | Hard fault event code                           | 1    |      |      |      |      |      |      |      |

| TB08:                        | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
|-----------------------------|-------------------------------------------------|------|------|------|------|------|------|------|------|
| INDEX                       | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
| 2240                        | Battery equalization state code                 | 1    |      |      |      |      |      |      |      |
| 2248                        | Hard fault event code                           | 1    |      |      |      |      |      |      |      |

| TB09:                        | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
|-----------------------------|-------------------------------------------------|------|------|------|------|------|------|------|------|
| INDEX                       | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
| 2200                        | System state code                               | 1    |      |      |      |      |      |      |      |

| TB15:                        | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
|-----------------------------|-------------------------------------------------|------|------|------|------|------|------|------|------|
| INDEX                       | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
| 2248                        | Hard fault event code                           | 1    |      |      |      |      |      |      |      |

| TB16:                        | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
|-----------------------------|-------------------------------------------------|------|------|------|------|------|------|------|------|
| INDEX                       | Definition                                      | Bit0 | Bit1 | Bit2 | Bit3 | Bit4 | Bit5 | Bit6 | Bit7 |
| 2228                        | Current event code2                             | 1    |      |      |      |      |      |      |      |

### Communication Demonstration

#### Get PIA Command
| Command Bytes       | Data                   |
|---------------------|------------------------|
| 00 04 10 00 00 12 75 16 | Get PIA command（获取 PIA 命令） |

#### Return Data
| Data Bytes       | Description                   | Value               |
|------------------|-------------------------------|---------------------|
| 00               | Address（地址）               | 0                   |
| 04               | Command（命令）               | 4                   |
| 24               | Bytes number（字节数）        | 36                  |
| 14 A1            | Pack Voltage（总压）          | 52.81V              |
| 00 00            | Current（电流）               | 0.00A               |
| 4E 20            | Remaining capacity（剩余容量） | 200.00AH            |
| 4E 20            | Total Capacity（总容量）       | 200.00AH            |
| 00 00            | Total Discharge Capacity（总放电容量） | 0.00AH      |
| 03 E8            | SOC                           | 100.0%              |
| 03 E8            | SOH                           | 100.0%              |
| 00 00            | Cycle（循环次数）             | 0                   |
| 0C E4            | Average of Cell Voltage（平均电芯电压） | 3.300V       |
| 0B 80            | Average of Cell Temperature（平均电芯温度） | 21.3℃      |
| 0C E6            | Max Cell Voltage（最高电芯电压） | 3.302V            |
| 0C E4            | Min Cell Voltage（最低电芯电压） | 3.300V            |
| 0B 82            | Max Cell Temperature（最高电芯温度） | 21.5℃          |
| 0B 7F            | Min Cell Temperature（最低电芯温度） | 21.2℃          |
| 00 00            | Reserve                        |                   |
| 00 B4            | Max Discharge Current（建议最大放电电流） | 180A         |
| 00 B4            | Max Charge Current（建议最大充电电流） | 180A           |
| 03 E8            | Reserve                        |                   |
| DB F6            | CRC Checksum                   |                   |

#### Get PIB Command
| Command Bytes       | Data                   |
|---------------------|------------------------|
| 00 04 11 00 00 1A 75 2C | Get PIB command（获取 PIB 命令） |

#### Return Data
| Data Bytes       | Description                   | Value               |
|------------------|-------------------------------|---------------------|
| 00               | Address（地址）               | 0                   |
| 04               | Command（命令）               | 4                   |
| 34               | Bytes number（字节数）        | 52                  |
| 0C E6            | Cell 1 Voltage（电芯 1 电压） | 3.302V              |
| 0C E4            | Cell 2 Voltage（电芯 2 电压） | 3.300V              |
| 0C E5            | Cell 3 Voltage（电芯 3 电压） | 3.301V              |
| 0C E4            | Cell 4 Voltage（电芯 4 电压） | 3.300V              |
| 0C E4            | Cell 5 Voltage（电芯 5 电压） | 3.300V              |
| 0C E5            | Cell 6 Voltage（电芯 6 电压） | 3.301V              |
| 0C E5            | Cell 7 Voltage（电芯 7 电压） | 3.301V              |
| 0C E4            | Cell 8 Voltage（电芯 8 电压） | 3.300V              |
| 0C E4            | Cell 9 Voltage（电芯 9 电压） | 3.300V              |
| 0C E4            | Cell 10 Voltage（电芯 10 电压） | 3.300V            |
| 0C E5            | Cell 11 Voltage（电芯 11 电压） | 3.301V            |
| 0C E5            | Cell 12 Voltage（电芯 12 电压） | 3.301V            |
| 0C E4            | Cell 13 Voltage（电芯 13 电压） | 3.300V            |
| 0C E5            | Cell 14 Voltage（电芯 14 电压） | 3.301V            |
| 0C E4            | Cell 15 Voltage（电芯 15 电压） | 3.300V            |
| 0C E4            | Cell 16 Voltage（电芯 16 电压） | 3.300V            |
| 0B 81            | Cell Temperature 1（电芯温度 1） | 21.4℃            |
| 0B 82            | Cell Temperature 2（电芯温度 2） | 21.5℃            |
| 0B 7F            | Cell Temperature 3（电芯温度 3） | 21.2℃            |
| 0B 7F            | Cell Temperature 4（电芯温度 4） | 21.2℃            |
| 0A AB            | Reserve                        |                   |
| 0A AB            | Reserve                        |                   |
| 0A AB            | Reserve                        |                   |
| 0A AB            | Reserve                        |                   |
| 0B 91            | Environment Temperature（环境温度） | 23.0℃            |
| 0B 83            | Power Temperature（功率温度）   | 21.6℃              |
| 34 DE            | CRC Checksum                   |                   |

#### Get PIC Command
| Command Bytes       | Data                   |
|---------------------|------------------------|
| 00 01 12 00 00 90 38 CF | Get PIC command（获取 PIC 命令） |

#### Return Data
| Data Bytes       | Description                   | Value               |
|------------------|-------------------------------|---------------------|
| 00               | Address（地址）               | 0                   |
| 01               | Command（命令）               | 1                   |
| 12               | Bytes number（字节数）        | 18                  |
| 00               | Cells voltage 08-01 low alarm state（8 个 bit，1-on、0-off） |                   |
| 00               | Cells voltage 16-09 low alarm state（8 个 bit，1-on、0-off） |                   |
| 00               | Cells voltage 08-01 high alarm state（8 个 bit，1-on、0-off） |                   |
| 00               | Cells voltage 16-09 high alarm state（8 个 bit，1-on、0-off） |                   |
| 00               | Cell 08-01 temperature Tlow alarm state（8 个 bit，1-on、0-off） |                   |
| 00               | Cell 08-01 temperature Thigh alarm state（8 个 bit，1-on、0-off） |                   |
| 00               | Cell 08-01 equalization event code（8 个 bit，1-on、0-off） |                   |
| 00               | Cell 16-09 equalization event code（8 个 bit，1-on、0-off） |                   |
| 10               | System state code（8 个 bit，1-on、0-off） |                   |
| 00               | Voltage event code（8 个 bit，1-on、0-off） |                   |
| 00               | Cells Temperature event code（8 个 bit，1-on、0-off） |                   |
| 00               | Environment and power Temperature event code（8 个 bit，1-on、0-off） |                   |
| 00               | Current event code1（8 个 bit，1-on、0-off） |                   |
| 00               | Current event code2（8 个 bit，1-on、0-off） |                   |
| 00               | The residual capacity code（8 个 bit，1-on、0-off） |                   |
| 03               | The FET event code（8 个 bit，1-on、0-off） |                   |
| 11               | Charge FET on、Discharge FET on（8 个 bit，1-on、0-off） |                   |
| 00               | Battery equalization state code（8 个 bit，1-on、0-off） |                   |
| 00               | Hard fault event code（8 个 bit，1-on、0-off） |                   |
| 6A 24            | CRC Checksum                   |                   |
