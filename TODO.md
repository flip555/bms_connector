# TODO for bms_connector

- [ ] Update the repository name from "seplos_bms_ha" to "bms_connector".
- [ ] Implement configflow verification for serial connection and sensor prefixes.
- [ ] Address and resolve Rust checks, and clean up template-related issues.
- [ ] Develop an ESPHome connector for integration.
- [ ] Develop a Bluetooth connector for integration.
- [ ] Implement comprehensive error handling across all aspects of the addon.

# Seplos V2 BMS

- [ ] Add support for multiple batteries.
	- [ ] Implement a "generate_command" function to create serial commands for each battery.
	- [ ] During asynchronous data updates, iterate through all batteries and adjust the battery pack reference in sensor names.
	- [ ] Revise the sensor generation process to include all batteries.
- [ ] Decode Modbus settings and integrate values as Home Assistant sensors.

# Seplos V3 BMS

- [ ] Begin the integration process with the PIA table.
- [ ] Conduct thorough testing to ensure proper functionality.
