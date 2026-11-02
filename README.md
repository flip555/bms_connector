# BMS Connector

Seplos battery data in Home Assistant — cell voltages, temperatures, current, alarms and protection settings — over USB-RS485 or an RS485-to-Ethernet bridge.

[![Release](https://img.shields.io/github/v/release/flip555/bms_connector?style=flat-square)](https://github.com/flip555/bms_connector/releases)
[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5?style=flat-square)](https://hacs.xyz/)
[![License](https://img.shields.io/github/license/flip555/bms_connector?style=flat-square)](LICENSE)
[![Discord](https://img.shields.io/discord/1161651448011034734?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/4eQbPEETBR)

## Supported

| BMS | USB-RS485 | RS485 → Ethernet |
|---|---|---|
| Seplos V2 | ✅ tested | ✅ supported |
| Seplos V3 | ✅ tested | ✅ tested |

Requires **Home Assistant 2025.1 or newer**.

## Install

**HACS** — add `https://github.com/flip555/bms_connector` as a custom repository (*Integration*), install, restart Home Assistant.

**Manual** — copy `custom_components/bms_connector` into your configuration directory and restart.

Then add it from **Settings → Devices & Services → Add Integration → BMS Connector**.

## Documentation

- **[Wiki home](https://github.com/flip555/bms_connector/wiki)** — setup, configuration and troubleshooting
- **[V2 sensor definitions](https://github.com/flip555/bms_connector/wiki/V2.0-Seplos-BMS-HA-Sensors-in-Home-Assistant:-Definitions-and-Data-Parameters)** — every field and unit
- **[Parallel packs](https://github.com/flip555/bms_connector/wiki/Parallel-Packs)** — RS485 limits and the BLE alternative

## Parallel packs

RS485 is unreliable for parallel Seplos V2 stacks because of firmware limitations. Use one entry per pack where possible; for true per-pack data from a parallel stack, use the ESP32 BLE component: **[flip555/seplos-v2-esp32-ble](https://github.com/flip555/seplos-v2-esp32-ble)**. See the [wiki page](https://github.com/flip555/bms_connector/wiki/Parallel-Packs) for details.

## Support

[Issues](https://github.com/flip555/bms_connector/issues) · [Discussions](https://github.com/flip555/bms_connector/discussions) · [Discord](https://discord.gg/4eQbPEETBR)

## Credits

V3 support began with **Christian F5UII ([@f5uii](https://github.com/f5uii))**. TCP frame scanning contributed by **[@foxy82](https://github.com/foxy82)** and confirmed by **[@peterb-dev](https://github.com/peterb-dev)**. Thanks to everyone who has filed hardware reports.
