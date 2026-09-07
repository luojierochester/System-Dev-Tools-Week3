import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prompt_contract import validate


class ContractTest(unittest.TestCase):
    def test_rejects_parent_path_and_missing_test(self):
        contract = {"goal": "fix", "constraints": ["small diff"], "allowed_files": ["../secret"]}
        errors = validate(contract)
        self.assertIn("missing field: test_command", errors)
        self.assertIn("unsafe allowed path: ../secret", errors)


if __name__ == "__main__":
    unittest.main()

