"""Install one wheel into a disposable environment and run its console script."""

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile
import venv


def verify(wheel: Path, expected: str) -> str:
    with tempfile.TemporaryDirectory(prefix="wheel-check-") as directory:
        root = Path(directory)
        venv.EnvBuilder(with_pip=True).create(root)
        python = root / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        command = root / ("Scripts/sdt-greet.exe" if sys.platform == "win32" else "bin/sdt-greet")
        subprocess.run(
            [str(python), "-m", "pip", "install", "--no-deps", "--no-index", str(wheel.resolve())],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        completed = subprocess.run(
            [str(command), "--name", "24020007086"],
            check=True,
            cwd=root,
            text=True,
            capture_output=True,
        )
        output = completed.stdout.strip()
        if output != expected:
            raise RuntimeError(f"unexpected output: {output!r}")
        return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", type=Path)
    parser.add_argument("--expect", default="Hello, 24020007086!")
    args = parser.parse_args()
    print("isolated output:", verify(args.wheel, args.expect))
    print("isolated install: PASS")


if __name__ == "__main__":
    main()

