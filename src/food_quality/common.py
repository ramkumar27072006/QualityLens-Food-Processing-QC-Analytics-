from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
WEEKS_DIR = PROJECT_ROOT / "weeks"
MODELS_DIR = PROJECT_ROOT / "models"

DEFAULT_RANDOM_STATE = 42


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_json(path: Path, data: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")


def snake_case(name: str) -> str:
    return (
        name.strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("-", "_")
    )


def configure_matplotlib_backend() -> None:
    # Force a non-interactive backend for script runs.
    import matplotlib

    matplotlib.use("Agg", force=True)


@dataclass(frozen=True)
class DatasetPaths:
    red_csv: Path
    white_csv: Path


def wine_quality_paths() -> DatasetPaths:
    return DatasetPaths(
        red_csv=DATA_RAW_DIR / "winequality-red.csv",
        white_csv=DATA_RAW_DIR / "winequality-white.csv",
    )
