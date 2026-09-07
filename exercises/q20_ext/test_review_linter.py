import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from review_linter import lint_review


class ReviewLinterTest(unittest.TestCase):
    def test_actionable_review_passes(self):
        comment = "Blocking：空值会导致调用方误判。请补充校验并运行测试验证。"
        self.assertEqual(lint_review(comment), [])

    def test_vague_review_fails(self):
        self.assertGreaterEqual(len(lint_review("这里写得不好，重写。")), 3)


if __name__ == "__main__":
    unittest.main()

