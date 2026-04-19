from __future__ import annotations

import datetime as dt
import urllib.request
from pathlib import Path

import pandas as pd

from .common import DATA_RAW_DIR, ensure_dir, snake_case, wine_quality_paths, write_text_if_missing


UCI_BASE = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/"
WINE_RED_URL = UCI_BASE + "winequality-red.csv"
WINE_WHITE_URL = UCI_BASE + "winequality-white.csv"


def _download(url: str, dest: Path) -> None:
    ensure_dir(dest.parent)
    # urllib is sufficient; avoids extra dependencies.
    urllib.request.urlretrieve(url, dest)  # noqa: S310


def download_wine_quality_if_needed() -> None:
    paths = wine_quality_paths()

    if not paths.red_csv.exists():
        _download(WINE_RED_URL, paths.red_csv)

    if not paths.white_csv.exists():
        _download(WINE_WHITE_URL, paths.white_csv)

    meta_path = DATA_RAW_DIR / "DATASET_SOURCES.md"
    retrieved = dt.datetime.now().strftime("%Y-%m-%d")
    content = (
        "# Dataset Sources (Public)\n\n"
        f"Retrieved: {retrieved}\n\n"
        "## UCI Wine Quality\n"
        f"- Red: {WINE_RED_URL}\n"
        f"- White: {WINE_WHITE_URL}\n\n"
        "Notes:\n"
        "- Files are downloaded as-is (CSV with ';' separator).\n"
        "- This dataset is used as a practical stand-in for food-quality metrics.\n"
    )
    write_text_if_missing(
        meta_path,
        content,
    )


def load_wine_quality_raw() -> pd.DataFrame:
    download_wine_quality_if_needed()
    paths = wine_quality_paths()

    red = pd.read_csv(paths.red_csv, sep=";")
    red["wine_type"] = "red"

    white = pd.read_csv(paths.white_csv, sep=";")
    white["wine_type"] = "white"

    df = pd.concat([red, white], ignore_index=True)

    # Standardize column names.
    df.columns = [snake_case(c) for c in df.columns]

    return df
