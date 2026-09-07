"""Greeting CLI with explicit validation for blank names."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    name = args.name.strip()
    if not name:
        parser.error("name must not be blank")
    print(f"Hello, {name}!")


if __name__ == "__main__":
    main()
