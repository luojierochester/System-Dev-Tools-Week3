"""Validate a machine-readable coding-agent task contract."""

import argparse
import json
from pathlib import Path, PurePosixPath

REQUIRED = {"goal", "constraints", "test_command", "allowed_files"}


def validate(contract: dict[str, object]) -> list[str]:
    errors = [f"missing field: {key}" for key in sorted(REQUIRED - contract.keys())]
    if not isinstance(contract.get("goal"), str) or not str(contract.get("goal", "")).strip():
        errors.append("goal must be a non-empty string")
    for key in ("constraints", "allowed_files"):
        value = contract.get(key)
        if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
            errors.append(f"{key} must be a non-empty string list")
    command = contract.get("test_command")
    if not isinstance(command, str) or not command.strip():
        errors.append("test_command must be a non-empty string")
    for raw in contract.get("allowed_files", []) if isinstance(contract.get("allowed_files"), list) else []:
        path = PurePosixPath(str(raw).replace("\\", "/"))
        if path.is_absolute() or ".." in path.parts:
            errors.append(f"unsafe allowed path: {raw}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    errors = validate(contract)
    if errors:
        print("contract: FAIL\n" + "\n".join(f"- {item}" for item in errors))
        raise SystemExit(1)
    print("contract: PASS")


if __name__ == "__main__":
    main()

