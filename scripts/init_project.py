#!/usr/bin/env python3
"""Initialize an AI comic-drama pipeline project using JSON-compatible YAML."""

import argparse
import json
import re
from pathlib import Path


def write_yaml(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Parent directory for the project")
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument("--episodes", type=int, default=60)
    parser.add_argument("--duration", type=int, choices=(60, 75, 90, 120), default=90)
    parser.add_argument("--model", default="Seedance 2.0 Mini")
    args = parser.parse_args()
    if args.episodes < 1:
        parser.error("--episodes must be positive")

    safe = re.sub(r'[<>:"/\\|?*]+', "-", args.name).strip(" .")
    if not safe:
        parser.error("--name must contain a usable filename character")
    project = Path(args.root).expanduser().resolve() / safe
    if project.exists() and any(project.iterdir()):
        parser.error(f"project directory is not empty: {project}")

    for rel in ("state", "story", "episodes", "reviews"):
        (project / rel).mkdir(parents=True, exist_ok=True)

    write_yaml(project / "project.yaml", {
        "schema_version": 1,
        "project_name": args.name,
        "target_episode_count": args.episodes,
        "episode_duration_seconds": args.duration,
        "video_model": args.model,
        "genre": "",
        "audience": "",
        "visual_style": "",
        "current_stage": 1,
        "current_episode": None,
        "current_segment": None,
        "locked": {
            "central_premise": "",
            "protagonist_desire": "",
            "central_conflict": "",
            "final_truth": "",
            "ending_direction": ""
        },
        "change_log": []
    })
    empty_files = {
        "characters.yaml": {"characters": []},
        "looks.yaml": {"looks": []},
        "scenes.yaml": {"scenes": []},
        "props.yaml": {"props": []},
        "continuity.yaml": {
            "last_completed_segment": None,
            "mode_for_next_segment": "MODE B",
            "characters": {}, "props": {}, "environment": {}, "camera": {}
        }
    }
    for name, data in empty_files.items():
        write_yaml(project / "state" / name, data)
    print(project)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
