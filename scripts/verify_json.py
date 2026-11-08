#!/usr/bin/env python3
"""Verify that a JSON output file contains the expected records in order."""

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", required=True, help="JSON array of expected records")
    parser.add_argument("--actual", required=True, help="JSON array written by the consumer")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    expected = json.loads(Path(args.expected).read_text(encoding="utf-8"))
    actual = json.loads(Path(args.actual).read_text(encoding="utf-8"))
    if actual != expected:
        raise SystemExit("Verification failed: JSON data differs")
    print(f"Verification passed: {len(expected)} records match")


if __name__ == "__main__":
    main()
