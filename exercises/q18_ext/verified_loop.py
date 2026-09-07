"""Run a verification command with bounded retries and structured evidence."""

import argparse
from dataclasses import asdict, dataclass
import json
import subprocess
import time
from typing import Callable


@dataclass
class Attempt:
    number: int
    returncode: int
    seconds: float
    output: str


def run_verified(
    command: list[str],
    attempts: int = 3,
    timeout: float = 30,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> list[Attempt]:
    history = []
    for number in range(1, attempts + 1):
        started = time.perf_counter()
        try:
            completed = runner(command, text=True, capture_output=True, timeout=timeout)
            code = completed.returncode
            output = (completed.stdout + completed.stderr).strip()
        except subprocess.TimeoutExpired as error:
            code, output = 124, f"timeout after {error.timeout}s"
        history.append(Attempt(number, code, time.perf_counter() - started, output))
        if code == 0:
            break
    return history


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("a verification command is required")
    history = run_verified(command, args.attempts, args.timeout)
    print(json.dumps([asdict(item) for item in history], indent=2, ensure_ascii=False))
    raise SystemExit(history[-1].returncode)


if __name__ == "__main__":
    main()
