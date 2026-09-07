import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reproducibility_audit import audit


class ReproducibilityTest(unittest.TestCase):
    def test_same_seed_repeats_exactly(self):
        report = audit()
        self.assertTrue(report["exact_state_match"])
        self.assertTrue(report["loss_match"])
        self.assertLess(report["final_loss"], 0.001)


if __name__ == "__main__":
    unittest.main()

