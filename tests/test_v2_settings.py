import importlib.util
import pathlib
import unittest

BASE = pathlib.Path(__file__).resolve().parents[1] / "custom_components/bms_connector/bms/seplos/v2"


def load(name):
    spec = importlib.util.spec_from_file_location(name, BASE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


settings = load("settings_protection")
info = load("management_info")
commands = load("commands")


class SettingsDecodeTest(unittest.TestCase):
    def _frame(self, **overrides):
        data = bytearray(148)
        spec = {f[0]: f for f in settings.FIELD_SPEC}
        for name, value in overrides.items():
            _, offset, width, signed, addend, scale = spec[name]
            raw = int(round(value / scale - addend))
            data[offset:offset + width] = raw.to_bytes(width, "big", signed=signed)
        return (len(data).to_bytes(2, "big") + data).hex()

    def test_thresholds_and_tail(self):
        frame = self._frame(
            monomer_high_voltage_alarm=3.5,
            charging_high_temperature_warning=50.0,
            charging_overcurrent_warning=100.0,
            discharge_overcurrent_warning=-100.0,
            output_soft_start_delay=2000,
            battery_number_in_series=16,
            cell_invalidation_differential_pressure=0.5,
            cell_invalidation_recovery=0.2,
            equalization_opening_pressure_difference=0.02,
            equalization_closing_pressure_difference=0.01,
            static_equilibrium_time=15,
            standby_shutdown_delay=48,
            work_record_interval=30,
            connection_fault_impedance=1.0,
        )
        r = settings.decode_fourseven(frame)
        self.assertAlmostEqual(r.monomer_high_voltage_alarm, 3.5, places=3)
        self.assertAlmostEqual(r.charging_high_temperature_warning, 50.0, places=3)
        self.assertAlmostEqual(r.charging_overcurrent_warning, 100.0, places=3)
        self.assertAlmostEqual(r.discharge_overcurrent_warning, -100.0, places=3)
        self.assertEqual(r.output_soft_start_delay, 2000)
        self.assertEqual(r.battery_number_in_series, 16)
        self.assertAlmostEqual(r.cell_invalidation_differential_pressure, 0.5, places=3)
        self.assertAlmostEqual(r.cell_invalidation_recovery, 0.2, places=3)
        self.assertAlmostEqual(r.equalization_opening_pressure_difference, 0.02, places=3)
        self.assertAlmostEqual(r.equalization_closing_pressure_difference, 0.01, places=3)
        self.assertEqual(r.static_equilibrium_time, 15)
        self.assertEqual(r.standby_shutdown_delay, 48)
        self.assertEqual(r.work_record_interval, 30)
        self.assertAlmostEqual(r.connection_fault_impedance, 1.0, places=3)

    def test_short_payload_does_not_raise(self):
        r = settings.decode_fourseven("0094" + "00" * 20)
        self.assertIsNotNone(r)
        self.assertIsNone(r.battery_number_in_series)

    def test_version_bytes(self):
        payload = b"1101-SP76 " + b"\x10\x06" + b"CAN:Victron "
        r = info.decode_fiveone(payload.hex())
        self.assertEqual(r.software_version, "16.6")
        self.assertEqual(r.device_name.strip(), "1101-SP76")


if __name__ == "__main__":
    unittest.main()


class CommandBuilderTest(unittest.TestCase):
    def test_known_zero_address(self):
        self.assertEqual(
            commands.build_v2_commands("0x00"),
            ["~20004642E00200FD37\r", "~20004644E00200FD35\r",
             "~20004647E00200FD32\r", "~20004651E00200FD37\r"],
        )

    def test_address_one_uses_address_in_info(self):
        cmds = commands.build_v2_commands("0x01")
        self.assertTrue(cmds[0].startswith("~20004642E00201"))
        self.assertEqual(len(cmds[0]), 20)

    def test_all_addresses_build(self):
        for addr in range(0x10):
            cmds = commands.build_v2_commands(f"0x{addr:02X}")
            self.assertEqual(len(cmds), 4)
            self.assertIn(f"E002{addr:02X}", cmds[0])

    def test_invalid_address(self):
        with self.assertRaises(ValueError):
            commands.build_v2_commands("0x10")
