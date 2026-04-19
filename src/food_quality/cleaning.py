from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class CleaningResult:
    df: pd.DataFrame
    report: dict[str, Any]


def _iqr_outlier_counts(df: pd.DataFrame, numeric_cols: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for col in numeric_cols:
        s = df[col].dropna()
        if s.empty:
            counts[col] = 0
            continue

        q1 = float(s.quantile(0.25))
        q3 = float(s.quantile(0.75))
        iqr = q3 - q1
        if iqr == 0:
            counts[col] = 0
            continue

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        counts[col] = int(((df[col] < lower) | (df[col] > upper)).sum())

    return counts


def clean_wine_quality(df_raw: pd.DataFrame) -> CleaningResult:
    df = df_raw.copy()

    report: dict[str, Any] = {
        "rows_before": int(df.shape[0]),
        "cols_before": int(df.shape[1]),
        "missing_total_before": int(df.isna().sum().sum()),
        "duplicate_rows_before": int(df.duplicated().sum()),
    }

    # Type fixes
    if "quality" in df.columns:
        df["quality"] = df["quality"].astype(int)

    # Drop exact duplicates
    df = df.drop_duplicates().reset_index(drop=True)

    # Basic domain consistency check (should hold for this dataset, but we record it anyway)
    if {"free_sulfur_dioxide", "total_sulfur_dioxide"}.issubset(df.columns):
        df["flag_free_sulfur_gt_total"] = (
            df["free_sulfur_dioxide"] > df["total_sulfur_dioxide"]
        )

    # Missing value handling (only applied if missing exists)
    missing_total_after_dedup = int(df.isna().sum().sum())
    report["missing_total_after_dedup"] = missing_total_after_dedup

    numeric_cols = [
        c
        for c in df.select_dtypes(include=[np.number]).columns
        if c not in {"quality"}
    ]

    # IQR outlier counts (we flag but do not delete rows)
    outlier_counts = _iqr_outlier_counts(df, numeric_cols)
    report["iqr_outlier_counts"] = outlier_counts

    # Minimal imputation strategy if needed
    imputed_cols: list[str] = []
    if missing_total_after_dedup > 0:
        for col in numeric_cols:
            if df[col].isna().any():
                df[f"was_missing_{col}"] = df[col].isna()
                df[col] = df[col].fillna(df[col].median())
                imputed_cols.append(col)

        # Categorical missing
        for col in df.select_dtypes(exclude=[np.number]).columns:
            if df[col].isna().any():
                df[f"was_missing_{col}"] = df[col].isna()
                df[col] = df[col].fillna("Unknown")
                imputed_cols.append(col)

    report["imputed_columns"] = imputed_cols

    report.update(
        {
            "rows_after": int(df.shape[0]),
            "cols_after": int(df.shape[1]),
            "missing_total_after": int(df.isna().sum().sum()),
            "duplicate_rows_after": int(df.duplicated().sum()),
        }
    )

    return CleaningResult(df=df, report=report)
