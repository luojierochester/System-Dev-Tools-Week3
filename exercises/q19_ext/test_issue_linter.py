import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from issue_linter import lint_issue


class IssueLinterTest(unittest.TestCase):
    def test_complete_issue_passes(self):
        text = "环境：Windows，版本待确认。复现：`tool --bad`。期望：退出码 2。实际：退出码 0。"
        self.assertEqual(lint_issue(text), [])

    def test_vague_issue_fails(self):
        self.assertGreaterEqual(len(lint_issue("Windows 上运行不了，尽快修复。")), 4)


if __name__ == "__main__":
    unittest.main()

