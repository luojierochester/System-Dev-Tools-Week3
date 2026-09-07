import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from patch_scope_guard import violations


class PatchScopeTest(unittest.TestCase):
    def test_accepts_only_approved_directory(self):
        paths = ["q10/src/greetlab/cli.py", "q10/tests/test_cli.py", "README.md"]
        self.assertEqual(violations(paths, ["q10"]), ["README.md"])


if __name__ == "__main__":
    unittest.main()

