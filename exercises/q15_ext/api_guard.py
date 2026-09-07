"""Detect removed public Python symbols before publishing a new package."""

import argparse
import ast
import json
from pathlib import Path


def public_symbols(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and not node.name.startswith("_")
    }


def compare(old: Path, new: Path) -> dict[str, list[str]]:
    before, after = public_symbols(old), public_symbols(new)
    return {"removed": sorted(before - after), "added": sorted(after - before)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("old", type=Path)
    parser.add_argument("new", type=Path)
    args = parser.parse_args()
    report = compare(args.old, args.new)
    print(json.dumps(report, ensure_ascii=False))
    raise SystemExit(1 if report["removed"] else 0)


if __name__ == "__main__":
    main()

