from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from .common import configure_matplotlib_backend, ensure_dir


def predict_proba_positive(model, X: pd.DataFrame) -> np.ndarray:
    prob = model.predict_proba(X)
    if prob.shape[1] != 2:
        raise ValueError("Expected binary classifier with predict_proba outputs.")
    return prob[:, 1]


def classification_metrics(y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.5) -> dict[str, Any]:
    from sklearn.metrics import (
        accuracy_score,
        average_precision_score,
        confusion_matrix,
        f1_score,
        precision_score,
        recall_score,
        roc_auc_score,
    )

    y_pred = (y_prob >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    return {
        "threshold": float(threshold),
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
        "pr_auc": float(average_precision_score(y_true, y_prob)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "tp": int(tp),
        "fp": int(fp),
        "tn": int(tn),
        "fn": int(fn),
        "positive_rate_true": float(np.mean(y_true)),
        "positive_rate_pred": float(np.mean(y_pred)),
    }


def plot_roc_pr_curves(y_true: np.ndarray, y_prob: np.ndarray, out_png: Path, title: str) -> None:
    configure_matplotlib_backend()
    import matplotlib.pyplot as plt
    from sklearn.metrics import precision_recall_curve, roc_curve

    ensure_dir(out_png.parent)

    fpr, tpr, _ = roc_curve(y_true, y_prob)
    precision, recall, _ = precision_recall_curve(y_true, y_prob)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(fpr, tpr)
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC")

    plt.subplot(1, 2, 2)
    plt.plot(recall, precision)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision-Recall")

    plt.suptitle(title)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()


def plot_calibration_curve(y_true: np.ndarray, y_prob: np.ndarray, out_png: Path, title: str, n_bins: int = 10) -> None:
    configure_matplotlib_backend()
    import matplotlib.pyplot as plt
    from sklearn.calibration import calibration_curve

    ensure_dir(out_png.parent)

    frac_pos, mean_pred = calibration_curve(y_true, y_prob, n_bins=n_bins, strategy="uniform")

    plt.figure(figsize=(6, 6))
    plt.plot(mean_pred, frac_pos, marker="o", label="model")
    plt.plot([0, 1], [0, 1], linestyle="--", label="perfect")
    plt.xlabel("Mean predicted probability")
    plt.ylabel("Fraction of positives")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()


def segment_metrics(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    segment: pd.Series,
    threshold: float = 0.5,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for seg_value, idx in segment.groupby(segment).groups.items():
        m = classification_metrics(y_true[idx], y_prob[idx], threshold=threshold)
        m["segment"] = str(seg_value)
        m["n"] = int(len(idx))
        rows.append(m)

    return pd.DataFrame(rows).sort_values(by="segment")
