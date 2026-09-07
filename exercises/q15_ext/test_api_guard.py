import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from api_guard import compare


class ApiGuardTest(unittest.TestCase):
    def test_reports_removed_and_added_symbols(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            old, new = root / "old.py", root / "new.py"
            old.write_text("def stable(): pass\ndef removed(): pass\n", encoding="utf-8")
            new.write_text("def stable(): pass\ndef added(): pass\n", encoding="utf-8")
            self.assertEqual(compare(old, new), {"removed": ["removed"], "added": ["added"]})


if __name__ == "__main__":
    unittest.main()

