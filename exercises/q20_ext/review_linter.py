"""Check whether a review comment communicates severity, risk, and action."""

import argparse
from pathlib import Path

SEVERITIES = ("Blocking", "Suggestion", "Nit")


def lint_review(text: str) -> list[str]:
    errors = []
    if not any(label in text for label in SEVERITIES):
        errors.append("missing severity: Blocking, Suggestion, or Nit")
    if not any(word in text for word in ("风险", "会", "导致", "调用方")):
        errors.append("missing concrete risk")
    if not any(word in text for word in ("请", "建议", "应", "需要")):
        errors.append("missing recommended action")
    if not any(word in text for word in ("测试", "验证", "复现")):
        errors.append("missing verification condition")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("review", type=Path)
    args = parser.parse_args()
    errors = lint_review(args.review.read_text(encoding="utf-8"))
    if errors:
        print("review quality: FAIL\n" + "\n".join(f"- {error}" for error in errors))
        raise SystemExit(1)
    print("review quality: PASS")


if __name__ == "__main__":
    main()

