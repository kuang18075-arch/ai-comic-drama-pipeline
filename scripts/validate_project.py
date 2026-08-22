#!/usr/bin/env python3
"""Validate project state files and cross-resource identifiers."""

import argparse
import json
import re
from pathlib import Path

PATTERNS = {
    "characters": re.compile(r"^CH-\d{3}$"),
    "looks": re.compile(r"^CH-\d{3}-LOOK-[A-Z]$"),
    "scenes": re.compile(r"^LOC-\d{3}$"),
    "props": re.compile(r"^PR-\d{3}$"),
}


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise ValueError(f"{path}: invalid JSON-compatible YAML: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    args = parser.parse_args()
    root = Path(args.project).expanduser().resolve()
    errors, warnings = [], []

    required = [root / "project.yaml"] + [root / "state" / f for f in
        ("characters.yaml", "looks.yaml", "scenes.yaml", "props.yaml", "continuity.yaml")]
    for path in required:
        if not path.is_file():
            errors.append(f"missing {path}")
    if errors:
        print("\n".join(f"ERROR: {x}" for x in errors))
        return 1

    try:
        project = load(root / "project.yaml")
        if project.get("current_stage") not in range(1, 10):
            errors.append("project.yaml current_stage must be 1..9")
        if int(project.get("target_episode_count", 0)) < 1:
            errors.append("target_episode_count must be positive")

        ids = {}
        for kind in PATTERNS:
            data = load(root / "state" / f"{kind}.yaml")
            seen = set()
            for index, item in enumerate(data.get(kind, [])):
                value = item.get("id")
                if not PATTERNS[kind].match(str(value)):
                    errors.append(f"{kind}[{index}] invalid id: {value}")
                if value in seen:
                    errors.append(f"{kind} duplicate id: {value}")
                seen.add(value)
            ids[kind] = seen

        for look in load(root / "state" / "looks.yaml").get("looks", []):
            char_id = str(look.get("id", ""))[:6]
            if char_id not in ids["characters"]:
                errors.append(f"look {look.get('id')} refers to missing character {char_id}")

        continuity = load(root / "state" / "continuity.yaml")
        for char_id in continuity.get("characters", {}):
            if char_id not in ids["characters"]:
                errors.append(f"continuity refers to missing character {char_id}")
        for prop_id in continuity.get("props", {}):
            if prop_id not in ids["props"]:
                errors.append(f"continuity refers to missing prop {prop_id}")
        if continuity.get("mode_for_next_segment") not in ("MODE A", "MODE B"):
            errors.append("mode_for_next_segment must be MODE A or MODE B")
    except ValueError as exc:
        errors.append(str(exc))

    for msg in errors:
        print(f"ERROR: {msg}")
    for msg in warnings:
        print(f"WARNING: {msg}")
    if errors:
        return 1
    print("PASS: project state is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
