import sys
import unittest
from pathlib import Path

from wheel_inspector import inspect_wheel


class WheelInspectorTest(unittest.TestCase):
    def test_real_q09_wheel_metadata(self):
        repo = Path(__file__).resolve().parents[2]
        wheels = list((repo / "q09" / "dist").glob("*.whl"))
        self.assertEqual(len(wheels), 1, "build q09 before running this test")
        report = inspect_wheel(wheels[0])
        self.assertEqual(report["name"], "greetlab-24020007086")
        self.assertEqual(report["entry_points"]["sdt-greet"], "greetlab.cli:main")
        self.assertIn("py3-none-any", report["tag"])


if __name__ == "__main__":
    unittest.main()

