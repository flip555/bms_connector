# TODO for bms_connector

- Add options_flow to change entries after initial setup.
- Enhance config flow verification for serial connection and sensor prefixes.
 	- Check if Port Already Added.
 	- Verify Battery Address accessibility via Port (Note: V2 won't add entities if the battery number isn't in the modbus response; consider adding a check at setup to prevent initial entry creation. V3 requires similar handling but requires extracting the battery number from the response first).
- Implement proper handling of multiple batteries, either by queuing access to the serial port to prevent overlap or by considering an auto-scanning approach that minimizes unnecessary serial commands. Auto-scanning might be the preferred option.
- Develop an ESPHome connector for integration.
- Develop a Bluetooth connector for integration.
- Implement comprehensive error handling across all aspects of the addon.
- Add docstrings to all functions and reinstate docstring checks in Rust.
- Improve code layout
	- Create a function to generate modbus ASCII commands dynamically rather than relying on fixed strings.
	- Enhance response reading functions to better handle common response layouts. Consider developing towards these common protocols rather than specific hardware.

# Seplos V2 BMS

- Continue refining support for multiple battery addresses.
- Revisit the Settings import (51H) as it becomes problematic after the times near the end. This is related to the "Improve code layout" enhancements.

# Seplos V3 BMS

- Revisit the Temp sensor data handling to ensure accurate PIC extraction.
- Review the process of extracting the battery address from the response to ensure the correct battery pack is identified.
- Implement support for multiple battery addresses - move away from fixed strings.
- Conduct comprehensive testing to validate proper functionality.
