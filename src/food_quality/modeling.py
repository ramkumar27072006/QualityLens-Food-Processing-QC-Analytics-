from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .common import DEFAULT_RANDOM_STATE, MODELS_DIR, ensure_dir


@dataclass(frozen=True)
class TrainResult:
    models: dict[str, Pipeline]
    meta: dict[str, Any]


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = [c for c in X.columns if c not in numeric_features]

    numeric_transformer = Pipeline(steps=[("scaler", StandardScaler())])
    categorical_transformer = Pipeline(
        steps=[
            (
                "onehot",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ],
        remainder="drop",
    )

    return preprocessor


def train_baseline_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    random_state: int = DEFAULT_RANDOM_STATE,
) -> TrainResult:
    preprocessor = build_preprocessor(X_train)

    models: dict[str, Pipeline] = {}

    models["logreg"] = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            (
                "model",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=random_state,
                ),
            ),
        ]
    )

    models["rf"] = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=400,
                    random_state=random_state,
                    class_weight="balanced",
                    n_jobs=-1,
                ),
            ),
        ]
    )

    for pipeline in models.values():
        pipeline.fit(X_train, y_train)

    ensure_dir(MODELS_DIR)
    for name, pipeline in models.items():
        dump(pipeline, MODELS_DIR / f"{name}.joblib")

    meta: dict[str, Any] = {
        "random_state": random_state,
        "n_train": int(X_train.shape[0]),
        "n_features": int(X_train.shape[1]),
        "models": list(models.keys()),
    }

    return TrainResult(models=models, meta=meta)
