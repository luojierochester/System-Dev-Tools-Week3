"""Behavior checks for the learned parameters and loss."""

import unittest

from train import train


class TrainingTest(unittest.TestCase):
    def test_loss_and_parameters_converge(self):
        model, final_loss = train()
        self.assertLess(final_loss, 0.001)
        self.assertAlmostEqual(model.weight.item(), 3.0, places=3)
        self.assertAlmostEqual(model.bias.item(), -1.0, places=3)


if __name__ == "__main__":
    unittest.main()

