import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gradient_diagnostics import train_with_diagnostics


class GradientDiagnosticsTest(unittest.TestCase):
    def test_training_is_finite_and_converges(self):
        report = train_with_diagnostics()
        self.assertGreater(report["maximum_grad_norm"], 1.0)
        self.assertLess(report["final_grad_norm"], 0.01)
        self.assertLess(report["final_loss"], 0.001)


if __name__ == "__main__":
    unittest.main()

