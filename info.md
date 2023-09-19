# Multi-BMS Home Assistant Integration (BMS Connector)

Easily connect and integrate various Battery Management Systems (BMS) with Home Assistant using this custom integration. This versatile tool provides detailed sensor readings, alarm notifications, and a wealth of telemetry data directly from multiple BMS units.

[![GitHub Discussions](https://img.shields.io/badge/GitHub-Discussions-0099ff?style=for-the-badge&logo=github)](https://github.com/flip555/bms_connector/discussions)
[![GitHub Wiki](https://img.shields.io/badge/GitHub-Wiki-4db6ac?style=for-the-badge&logo=github)](https://github.com/flip555/bms_connector/wiki)

## 🌟 Features
### Supported BMS Systems
- **Seplos BMS 2.0**:
  - **Integration Highlights**:
    - Detailed Data: Fetch cell voltage for every cell in the system.
    - Comprehensive Alarms: Get unambiguous feedback from different alarm states.
    - Telemetry Insights: Access vital information like temperatures, currents, and the system state.
    - Full Retrieval of BMS Settings: Retrieve configuration settings from the BMS.

- **Seplos BMS 3.0**: 
  - Cell Voltages, Pack Voltages Temp and Currents should all be available and working for a single battery. More coming very soon!

- **Custom BMS Compatibility**: Enhanced scanning capability to find all battery packs (Note: Currently focused on pack 0).

## 🚧 Upcoming Features
- Extended support further for Seplos BMS 3.0.
- Improved scanning capabilities for various BMS models.
- Enhanced configuration options and multilingual support with translations.
- Codebase optimization and removal of unnecessary blueprint integrations.
- Robust error handling for enhanced stability.

## 🔧 Installation

### Via HACS (Home Assistant Community Store) as a Custom Repository
1. Ensure you have [HACS](https://hacs.xyz/) installed.
2. Go to the HACS Integrations page.
3. Click the three dots in the upper right corner and select "Custom repositories".
4. Enter the URL `https://github.com/flip555/bms_connector` and choose `Integration` from the category dropdown.
5. Click "Add".
6. You can now find `BMS Connector` in the Integrations list within HACS. Simply install it.

### Manual Installation
1. Clone this repository or download the ZIP file.
2. Transfer the `bms_connector` folder from the repository into the `custom_components` directory within your Home Assistant configuration.
3. Restart Home Assistant.

## ⚙️ Configuration
1. Access the Integrations page in the Home Assistant UI.
2. Click the "+" icon at the bottom.
3. Search for "BMS Connector" and start the configuration process.
4. Select the appropriate source for your BMS hardware.
5. For users with the `RS485-USB` setup, enter the USB port using the template `/dev/ttyUSBX`, where `X` represents the port number (e.g., `/dev/ttyUSB0`).
6. Click "Submit" to complete the setup.

## 📸 Screenshots
![Dashboard Visuals](https://github.com/flip555/bms_connector/blob/main/assets/dashboard.png)

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
Encountering an issue or need assistance? Don't hesitate to open an issue on the [GitHub repository](https://github.com/flip555/bms_connector/issues).

## 📚 References

- **ChatGPT**: Developed by OpenAI, ChatGPT is a large language model capable of understanding and generating human-like text.
- **Seplos Protocol Manuals**: You can find these in the [assets/](https://github.com/flip555/bms_connector/tree/main/assets) directory of this repository.
- **Integration Blueprint**: A valuable template for creating custom components for Home Assistant. [GitHub Repository](https://github.com/ludeeus/integration_blueprint)
- **ESPHome Seplos BMS**: A related project that integrates Seplos BMS with ESPHome. [GitHub Repository](https://github.com/syssi/esphome-seplos-bms)
- **Modbus Seplos BMS Reader**: A Modbus implementation for reading Seplos BMS data. [GitHub Repository](https://github.com/g992/modbus-seplos-bms-reader)
