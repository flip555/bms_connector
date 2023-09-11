# Seplos BMS HA Custom Integration for Home Assistant

Easily connect and integrate the Seplos Battery Management Systems (BMS) with Home Assistant. This integration offers detailed sensor readings, alarm notifications, and a plethora of valuable telemetry data directly from the BMS.

[![GitHub Link](https://img.shields.io/badge/GitHub-Repo-green?style=for-the-badge&logo=github)](https://github.com/flip555/seplos_bms_ha)

## 🌟 Features
### Seplos BMS 2.0
- **Rapid Data Retrieval**: Fetch cell voltage for every cell in the system.
- **Advanced Alarm Monitoring**: Get unambiguous feedback from different alarm states.
- **Rich Telemetry Data**: Access vital information like temperatures, currents, and the system state.
- **Debug Mode**: Dive deep and see the underlying data for thorough insights.
- **High Frequency Polling**: Refreshes data every 5 seconds for up-to-the-minute updates.

## 🚧 Upcoming Features
- Support for Seplos BMS 3.0.
- Enhanced scanning capability to find all battery packs (Note: Currently focused on pack 0).
- Improved config_flow checks and additional options.
- Multilingual support with translations.
- Codebase optimization and removal of unnecessary blueprint integration.
- Robust error handling for better stability.

## 🔧 Installation

### Via HACS (Home Assistant Community Store) as a Custom Repository
1. Make sure [HACS](https://hacs.xyz/) is installed.
2. Head over to the HACS Integrations page.
3. Tap on the three dots in the upper right corner and pick "Custom repositories".
4. Plug in the URL `https://github.com/flip555/seplos_bms_ha` and opt for `Integration` in the category dropdown.
5. Hit "Add".
6. You'll now find `Seplos BMS HA` in the Integrations list within HACS. Simply install it.

### Manual Installation
1. Either clone this repo or grab the zip.
2. Transfer the `seplos_bms_ha` folder from the repository into the `custom_components` directory within your Home Assistant configuration.
3. Give Home Assistant a quick restart.

## ⚙️ Configuration
1. Access the Integrations page inside the Home Assistant UI.
2. Tap the "+" icon located at the bottom.
3. Type in "Seplos BMS HA" and commence the configuration process.
4. Pinpoint the suitable source for your hardware.
5. For users with the `RS485-USB` setup, punch in the USB port following the template `/dev/ttyUSBX`, where `X` represents the port digit (for instance, `/dev/ttyUSB0`).
6. Click "Submit" to seal the deal.

## 📸 Screenshots
![Dashboard Visuals](https://github.com/flip555/seplos_bms_ha/blob/main/assets/dashboard.png)

## 🤝 Contributing
Your inputs to bolster this integration will be wholeheartedly embraced! Dive into our [Contribution Guidelines](CONTRIBUTING.md) for an in-depth look.

## 🆘 Support
Facing a hiccup? Need a hand? Feel free to raise an issue on the [GitHub repository](https://github.com/flip555/seplos_bms_ha/issues).
