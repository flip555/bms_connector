# Multi-BMS Home Assistant Integration (BMS Connector)

Easily connect and integrate Seplos Battery Management Systems with Home Assistant using this custom integration. Provides detailed sensor readings, alarm notifications, and telemetry data from your BMS.

[![Discord](https://img.shields.io/discord/1161651448011034734?style=for-the-badge&logo=discord)](https://discord.gg/4eQbPEETBR)
[![GitHub Discussions](https://img.shields.io/badge/GitHub-Discussions-0099ff?style=for-the-badge&logo=github)](https://github.com/f5uii/bms_connector/discussions)

## ⚠️ Breaking Changes in v1.2.x

- **Entity unique IDs changed** — stable entry_id-based unique IDs prevent duplication when changing the sensor prefix. **Delete existing config entries and re-add** to avoid orphaned entities.
- **Config flow simplified** — no more confirmation checkbox, goes straight to BMS selection.
- **Connection type selector** — choose USB Serial or Telnet during setup.
- **Devices reorganised** — Seplos V2 sensors now split into two devices per entry:
  - `{prefix}` — BMS data (80 entities)
  - `{prefix} Settings` — protection settings (87 entities)

## 🌟 Features

### Supported BMS Systems
- **Seplos BMS V2** (✅ tested):
  - Cell voltages for all 16 cells
  - Temperature sensors
  - Current, voltage, power readings
  - Comprehensive alarm/event decoding
  - Full protection settings retrieval (87 settings sensors)
  - Calculated values (battery watts, remaining capacity, etc.)

- **Seplos BMS V3** (🧪 untested):
  - Pack voltage, current, SOC, SOH
  - Cell voltages for all 16 cells
  - PIA and PIB Modbus RTU tables
  - Multiple device addressing

### Connection Methods
- **USB-RS485 Serial** (✅ tested) — direct serial connection via `/dev/ttyUSB0` etc.
- **Telnet/RS485-to-Ethernet** (🧪 untested) — for bridges like Elfin EW11, USR-N510

## 🚧 Upcoming Features
- Parallel BMS multi-pack support
- Configurable sensor refresh rate
- Further Seplos BMS V3 improvements

## 🔧 Installation

### Via HACS as a Custom Repository
1. Ensure you have [HACS](https://hacs.xyz/) installed.
2. Go to HACS → Integrations → Three dots → "Custom repositories".
3. Enter URL `https://github.com/flip555/bms_connector` and select `Integration`.
4. Click "Add", then find "BMS Connector" in HACS and install it.
5. Restart Home Assistant.

### Manual Installation
1. Download the ZIP from the [latest release](https://github.com/flip555/bms_connector/releases).
2. Extract `bms_connector` into your Home Assistant `custom_components` directory.
3. Restart Home Assistant.

## ⚙️ Configuration

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for **BMS Connector**.
3. Select your **BMS type** (Seplos V2 or V3).
4. Select your **connection type**:
   - **USB-RS485 Serial**: Enter the serial port (e.g., `/dev/ttyUSB0`).
   - **Telnet**: Enter the host address and port of your RS485-to-Ethernet bridge.
5. Enter the **battery address** (default `0x00` for single pack) and a **sensor prefix** (e.g., "Seplos BMS HA").
6. Click Submit.

## 📸 Screenshots
![Dashboard Visuals](https://github.com/f5uii/bms_connector/blob/main/assets/dashboard.png)

## 🙏 Acknowledgments

Special thanks to **Christian F5UII** ([@f5uii](https://github.com/f5uii)) for the substantial Seplos BMS V3 implementation, including:
- Complete Modbus RTU protocol support with CRC validation
- Multiple battery pack addressing
- Robust serial communication with frame validation
- PIA/PIB register parsing

His contributions made V3 support possible.

## 🆘 Support
Encountering an issue or need assistance? Open an issue on the [GitHub repository](https://github.com/flip555/bms_connector/issues).

## 📚 References
- **Seplos Protocol Manuals** — available in the [assets/](https://github.com/flip555/bms_connector/tree/main/assets) directory.
- **Integration Blueprint** — template for creating HA custom components. [GitHub Repository](https://github.com/ludeeus/integration_blueprint)
- **ESPHome Seplos BMS** — related ESPHome project. [GitHub Repository](https://github.com/syssi/esphome-seplos-bms)
- **Modbus Seplos BMS Reader** — Modbus implementation for Seplos BMS. [GitHub Repository](https://github.com/g992/modbus-seplos-bms-reader)
