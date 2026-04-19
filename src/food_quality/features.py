from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class FeatureResult:
    X: pd.DataFrame
    y: pd.Series
    meta: dict[str, Any]


def add_engineered_features(df_in: pd.DataFrame) -> pd.DataFrame:
    df = df_in.copy()

    required = {
        "fixed_acidity",
        "volatile_acidity",
        "citric_acid",
        "free_sulfur_dioxide",
        "total_sulfur_dioxide",
        "residual_sugar",
        "chlorides",
        "density",
        "alcohol",
    }

    if required.issubset(df.columns):
        df["total_acidity"] = df["fixed_acidity"] + df["volatile_acidity"] + df["citric_acid"]
        df["sulfur_ratio"] = df["free_sulfur_dioxide"] / (df["total_sulfur_dioxide"] + 1e-6)
        df["residual_sugar_log"] = np.log1p(df["residual_sugar"])
        df["chlorides_log"] = np.log1p(df["chlorides"])
        df["density_alcohol"] = df["density"] * df["alcohol"]
        df["sugar_to_alcohol"] = df["residual_sugar"] / (df["alcohol"] + 1e-6)

    return df


def make_binary_target(df: pd.DataFrame, quality_threshold: int = 7) -> pd.Series:
    if "quality" not in df.columns:
        raise ValueError("Expected 'quality' column to build target.")

    return (df["quality"] >= quality_threshold).astype(int)


def build_features(df_clean: pd.DataFrame, quality_threshold: int = 7) -> FeatureResult:
    df = add_engineered_features(df_clean)
    y = make_binary_target(df, quality_threshold=quality_threshold)

    drop_cols = {"quality"}
    X = df.drop(columns=[c for c in drop_cols if c in df.columns])

    meta: dict[str, Any] = {
        "quality_threshold": quality_threshold,
        "positive_class_definition": f"quality >= {quality_threshold}",
        "n_rows": int(df.shape[0]),
        "n_features": int(X.shape[1]),
        "positive_rate": float(y.mean()),
    }

    return FeatureResult(X=X, y=y, meta=meta)
