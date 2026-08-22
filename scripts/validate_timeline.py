#!/usr/bin/env python3
"""Validate a 15-second prompt timeline from ranges such as 0-4秒."""

import argparse
import re
from pathlib import Path

RANGE = re.compile(r"(?<!\d)(\d+(?:\.\d+)?)\s*(?:—|–|-)\s*(\d+(?:\.\d+)?)\s*秒")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--duration", type=float, default=15.0)
    args = parser.parse_args()
    text = Path(args.file).read_text(encoding="utf-8-sig")
    ranges = [(float(a), float(b)) for a, b in RANGE.findall(text)]
    errors = []
    if not ranges:
        errors.append("no timeline ranges found")
    else:
        if ranges[0][0] != 0:
            errors.append(f"timeline starts at {ranges[0][0]}, expected 0")
        for i, (start, end) in enumerate(ranges):
            if end <= start:
                errors.append(f"range {i + 1} has non-positive duration")
            if i and start != ranges[i - 1][1]:
                errors.append(f"gap/overlap between {ranges[i - 1]} and {ranges[i]}")
        if ranges[-1][1] != args.duration:
            errors.append(f"timeline ends at {ranges[-1][1]}, expected {args.duration}")
        if not 2 <= len(ranges) <= 6:
            errors.append(f"found {len(ranges)} shots, expected 2..6")
    if errors:
        print("\n".join(f"ERROR: {x}" for x in errors))
        return 1
    print(f"PASS: {len(ranges)} shots cover 0-{args.duration:g} seconds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
