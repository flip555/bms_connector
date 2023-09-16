## I. Communication Instructions

The EMU11XX series of BMS products communicate with FSU, PC, or other upper controllers via RS485, using the MODBUS ASCII communication protocol as per the YD/T1363.3 specification.

### 1.1 Interface Setting

- EMU11XX series of BMS products use asynchronous serial communication interfaces.
- Start bit: 1
- Data bit: 8
- Stop bit: 1
- Check bit: None
- Default data transmission rate: 9600 BPS.

### 1.2 Interface Connection

Note: A 120Ω terminal matching resistor should be added to the starting and final points of the communication connection respectively.

### 1.3 Connection Mode

The communication between the supervision unit (SU) and the supervision module (SM) is a point-to-multipoint master-slave mode. SU calls SM using BMS DIP addresses:

- BMS DIP address 1
- BMS DIP address 2
- BMS DIP address 3
- ...
- BMS DIP address 15

SU issues commands to the called SM at the corresponding address, and the SM receives the command and returns the response information. If SU does not receive the response information from SM within 500ms or receives the wrong response information, the communication process is considered to have failed.

## II. Information Structure

Information is organized in a structured manner for correct transmission between SU and SM. Refer to Table 1 for information structure. Information is composed of multiple bytes, where one or more bytes form a unit, each having a name that represents its defined meaning. Additional details about the units in Table 1 can be found in Table 2. Furthermore, Table 3 provides comments on CID1 in Table 2, while Table 4 and Table 5 offer further comments on CID2 in Table 2.

### Table 1: List of Information Structures

| Items | SOI | VER | ADR | CID1 | CID2 | LENGTH | INFO | CHKSUM | EOI |
| ----- | --- | --- | --- | ---- | ---- | ------ | ---- | ------ | --- |
| ASCII byte | 1 | 2   | 2   | 2    | 2    | 4      | LENID | 4      | 1   |

### Table 2: Comments on Information Structures

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
