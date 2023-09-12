# Seplos BMS HA Custom Integration for Home Assistant

Easily connect and integrate the Seplos Battery Management Systems (BMS) with Home Assistant. This integration offers detailed sensor readings, alarm notifications, and a plethora of valuable telemetry data directly from the BMS.

[![GitHub Discussions](https://img.shields.io/badge/GitHub-Discussions-0099ff?style=for-the-badge&logo=github)](https://github.com/flip555/seplos_bms_ha/discussions)
[![GitHub Wiki](https://img.shields.io/badge/GitHub-Wiki-4db6ac?style=for-the-badge&logo=github)](https://github.com/flip555/seplos_bms_ha/wiki)

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

## 🤝 Contributing Guidelines

Thank you for your interest in contributing to our project! Whether you're reporting bugs, proposing new features, or contributing code, we appreciate your support. Here are some guidelines to follow:

### Git Branch Workflow

#### Main Branch

- **Branch name**: `main`
- **Purpose**: This branch contains the production-ready code. It should always be stable and deployable.
- **Maintainer**: flip555

#### Next Branch

- **Branch name**: `next-branch`
- **Purpose**: This is the development or integration branch where new features and fixes are accumulated before being merged into `main`.
- **Maintainer**: flip555

#### Feature or Fix Branches

- **Branch names**: E.g., `battery-multipacks`
- **Purpose**: These branches are created for new features or fixes to keep work isolated. They will be merged into `next-branch` once completed.
- **Maintainer**: Individual contributors

#### Workflow Overview

1. **Creating new branches**: For any new feature or fix, create a new branch.
2. **Merging into `next-branch`**: Once your work is complete, create a pull request to merge it into `next-branch`.
3. **Testing**: Before merging changes into `main`, we conduct thorough testing in the `next-branch`.
4. **Merging into `main`**: After ensuring stability, changes from `next-branch` are merged into `main`.
5. **Releasing**: Following a successful merge into `main`, tag the commit with a version number to indicate a new release.
6. **Reset `next-branch`**: Post-release, reset `next-branch` to the current state of `main` to begin the next development cycle.

### Getting Help

Feel free to use resources like ChatGPT to assist you, even if you are a novice coder. We are here to foster a collaborative and inclusive environment.

### Reporting Issues

When reporting issues, please be as descriptive as possible. Provide the steps to reproduce the issue, expected outcome, and actual results.

Thank you for your collaboration and contribution!

## 🆘 Support
Facing a hiccup? Need a hand? Feel free to raise an issue on the [GitHub repository](https://github.com/flip555/seplos_bms_ha/issues).

## 📚 References

- **ChatGPT**: Developed by OpenAI, ChatGPT is a large language model capable of understanding and generating human-like text.
- **Seplos Protocol Manuals**: You can find these in the [assets/](https://github.com/flip555/seplos_bms_ha/tree/main/assets) directory of this repository.
- **Integration Blueprint**: A valuable template for creating custom components for Home Assistant. [GitHub Repository](https://github.com/ludeeus/integration_blueprint)
- **ESPHome Seplos BMS**: A related project which integrates Seplos BMS with ESPHome. [GitHub Repository](https://github.com/syssi/esphome-seplos-bms)
- **Modbus Seplos BMS Reader**: A Modbus implementation for reading Seplos BMS data. [GitHub Repository](https://github.com/g992/modbus-seplos-bms-reader)
