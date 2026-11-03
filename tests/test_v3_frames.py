import importlib.util
import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
FIX = Path(__file__).resolve().parent / "fixtures" / "v3"


def load(name):
    spec = importlib.util.spec_from_file_location(
        name, BASE / "custom_components/bms_connector/bms/seplos/v3/data_parser.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v3 = load("v3_data_parser")


def fixture(name):
    return json.loads((FIX / name).read_text())


class V3FrameTests(unittest.TestCase):
    def test_pia_frame(self):
        data = fixture("pia_sp05b.json")
        self.assertTrue(v3.verify_crc(data["frame_hex"]))
        pia = v3.decode_pia_table(data["frame_hex"])
        self.assertIsNotNone(pia)
        for key, expected in data["expected"].items():
            self.assertAlmostEqual(getattr(pia, key), expected, places=4, msg=key)

    def test_pib_frame(self):
        data = fixture("pib_sp05b.json")
        self.assertTrue(v3.verify_crc(data["frame_hex"]))
        pib = v3.decode_pib_table(data["frame_hex"])
        self.assertIsNotNone(pib)
        for key, expected in data["expected"].items():
            self.assertAlmostEqual(getattr(pib, key), expected, places=4, msg=key)

    def test_bad_crc_rejected(self):
        data = fixture("pia_sp05b.json")
        raw = bytearray.fromhex(data["frame_hex"])
        raw[10] ^= 0xFF
        self.assertIsNone(v3.decode_pia_table(raw.hex()))

    def test_truncated_rejected(self):
        data = fixture("pib_sp05b.json")
        raw = data["frame_hex"][:-8]
        self.assertIsNone(v3.decode_pib_table(raw))
