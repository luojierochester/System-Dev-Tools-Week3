import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verified_loop import run_verified


class VerifiedLoopTest(unittest.TestCase):
    def test_stops_after_first_success(self):
        codes = iter([1, 0, 0])

        def fake_runner(*_args, **_kwargs):
            code = next(codes)
            return subprocess.CompletedProcess([], code, stdout=f"code={code}", stderr="")

        history = run_verified(["test"], attempts=3, runner=fake_runner)
        self.assertEqual([item.returncode for item in history], [1, 0])


if __name__ == "__main__":
    unittest.main()

