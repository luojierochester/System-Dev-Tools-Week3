"""Check that an issue contains enough information to reproduce a defect."""

import argparse
from pathlib import Path

REQUIRED_MARKERS = ("环境", "复现", "期望", "实际")


def lint_issue(text: str) -> list[str]:
    errors = [f"missing marker: {marker}" for marker in REQUIRED_MARKERS if marker not in text]
    if "`" not in text:
        errors.append("missing fenced reproduction command")
    if "状态码" not in text and "退出码" not in text:
        errors.append("missing observable exit status")
    if "待确认" not in text:
        errors.append("unknown environment details must say 待确认")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("issue", type=Path)
    args = parser.parse_args()
    errors = lint_issue(args.issue.read_text(encoding="utf-8"))
    if errors:
        print("issue quality: FAIL\n" + "\n".join(f"- {error}" for error in errors))
        raise SystemExit(1)
    print("issue quality: PASS")


if __name__ == "__main__":
    main()

