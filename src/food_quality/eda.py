from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from .common import configure_matplotlib_backend, ensure_dir, save_json


def dataframe_overview(df: pd.DataFrame) -> dict[str, Any]:
    missing_by_col = df.isna().sum().sort_values(ascending=False)
    duplicate_rows = int(df.duplicated().sum())

    overview: dict[str, Any] = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "missing_total": int(df.isna().sum().sum()),
        "missing_by_col": {k: int(v) for k, v in missing_by_col.items() if int(v) > 0},
        "duplicate_rows": duplicate_rows,
    }

    if "quality" in df.columns:
        quality_counts = df["quality"].value_counts(dropna=False).sort_index()
        overview["quality_distribution"] = {int(k): int(v) for k, v in quality_counts.items()}

    if "wine_type" in df.columns:
        type_counts = df["wine_type"].value_counts(dropna=False)
        overview["wine_type_distribution"] = {str(k): int(v) for k, v in type_counts.items()}

    return overview


def save_overview(df: pd.DataFrame, out_json: Path) -> None:
    save_json(out_json, dataframe_overview(df))


def plot_quality_distribution(df: pd.DataFrame, out_png: Path) -> None:
    configure_matplotlib_backend()
    import matplotlib.pyplot as plt
    import seaborn as sns

    ensure_dir(out_png.parent)

    plt.figure(figsize=(10, 5))
    if "wine_type" in df.columns:
        sns.countplot(data=df, x="quality", hue="wine_type")
        plt.legend(title="wine_type")
    else:
        sns.countplot(data=df, x="quality")

    plt.title("Quality Score Distribution")
    plt.xlabel("quality")
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()


def plot_missingness(df: pd.DataFrame, out_png: Path, top_n: int = 25) -> None:
    configure_matplotlib_backend()
    import matplotlib.pyplot as plt
    import seaborn as sns

    ensure_dir(out_png.parent)

    missing = df.isna().sum().sort_values(ascending=False)
    missing = missing[missing > 0].head(top_n)

    plt.figure(figsize=(10, 5))
    if missing.empty:
        plt.text(0.5, 0.5, "No missing values detected", ha="center", va="center")
        plt.axis("off")
    else:
        sns.barplot(x=missing.values, y=missing.index)
        plt.title("Missing Values by Column")
        plt.xlabel("missing_count")
        plt.ylabel("column")

    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()


def plot_correlation_heatmap(df: pd.DataFrame, out_png: Path) -> None:
    configure_matplotlib_backend()
    import matplotlib.pyplot as plt
    import seaborn as sns

    ensure_dir(out_png.parent)

    num_df = df.select_dtypes(include=[np.number])
    corr = num_df.corr(numeric_only=True)

    plt.figure(figsize=(11, 9))
    sns.heatmap(corr, cmap="vlag", center=0, square=False)
    plt.title("Correlation Heatmap (Numeric Features)")
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()
