"""Ensure an agent-generated patch only touches approved path prefixes."""

import argparse
from pathlib import PurePosixPath


def normalize(path: str) -> str:
    return PurePosixPath(path.strip().replace("\\", "/")).as_posix()


def violations(paths: list[str], allowed: list[str]) -> list[str]:
    prefixes = [normalize(prefix).rstrip("/") + "/" for prefix in allowed]
    bad = []
    for raw in paths:
        path = normalize(raw)
        if path and not any((path + "/").startswith(prefix) for prefix in prefixes):
            bad.append(path)
    return sorted(set(bad))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow", action="append", required=True)
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    bad = violations(args.paths, args.allow)
    if bad:
        print("out-of-scope files:")
        print("\n".join(f"- {path}" for path in bad))
        raise SystemExit(1)
    print(f"patch scope: PASS ({len(args.paths)} files)")


if __name__ == "__main__":
    main()

