#!/usr/bin/env python3
"""Merge an asset increment into a project asset file without overwriting IDs."""

import argparse
import json
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("increment")
    parser.add_argument("--key", choices=("characters", "looks", "scenes", "props"), required=True)
    args = parser.parse_args()
    target, increment = Path(args.target), Path(args.increment)
    current, added = load(target), load(increment)
    existing = {item.get("id") for item in current.get(args.key, [])}
    incoming = added.get(args.key, [])
    duplicate = sorted({item.get("id") for item in incoming if item.get("id") in existing})
    if duplicate:
        print("ERROR: refusing to overwrite existing IDs: " + ", ".join(duplicate))
        return 1
    current.setdefault(args.key, []).extend(incoming)
    target.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: merged {len(incoming)} {args.key}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
