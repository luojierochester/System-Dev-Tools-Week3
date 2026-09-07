import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from checkpoint_roundtrip import roundtrip


class CheckpointTest(unittest.TestCase):
    def test_predictions_survive_save_and_load(self):
        report = roundtrip()
        self.assertEqual(report["step"], 100)
        self.assertTrue(report["exact_prediction_match"])
        self.assertEqual(report["max_absolute_difference"], 0.0)
        self.assertGreater(report["checkpoint_bytes"], 0)


if __name__ == "__main__":
    unittest.main()

