"""Portable resource locations shared by the original application variants."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "yolov8n.pt"
VIDEO_DIR = PROJECT_ROOT / "Source_vids"
DIRECTIONS = ("north", "east", "south", "west")


def video_path(direction):
    return str(VIDEO_DIR / f"{direction}.mp4")


def validate_resources():
    required = [MODEL_PATH, *(Path(video_path(d)) for d in DIRECTIONS)]
    missing = [str(p) for p in required if not p.is_file()]
    if missing:
        raise FileNotFoundError(
            "Missing project resources:\n" + "\n".join(missing)
            + "\nSee README.md for model and video setup."
        )
