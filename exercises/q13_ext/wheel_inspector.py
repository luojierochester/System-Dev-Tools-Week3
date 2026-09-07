"""Inspect a wheel without installing it, using only the standard library."""

import argparse
import configparser
import email
import json
from pathlib import Path
import zipfile


def inspect_wheel(path: Path) -> dict[str, object]:
    if path.suffix != ".whl" or not zipfile.is_zipfile(path):
        raise ValueError(f"not a valid wheel: {path}")
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        metadata_name = next(name for name in names if name.endswith(".dist-info/METADATA"))
        wheel_name = next(name for name in names if name.endswith(".dist-info/WHEEL"))
        metadata = email.message_from_bytes(archive.read(metadata_name))
        wheel_metadata = email.message_from_bytes(archive.read(wheel_name))
        entry_points = {}
        entry_name = next((name for name in names if name.endswith(".dist-info/entry_points.txt")), None)
        if entry_name:
            parser = configparser.ConfigParser()
            parser.read_string(archive.read(entry_name).decode())
            entry_points = dict(parser.items("console_scripts")) if parser.has_section("console_scripts") else {}
    return {
        "name": metadata["Name"],
        "version": metadata["Version"],
        "tag": wheel_metadata["Tag"],
        "entry_points": entry_points,
        "file_count": len(names),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect_wheel(args.wheel), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

