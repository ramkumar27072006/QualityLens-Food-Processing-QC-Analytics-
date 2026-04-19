from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind

from .stats_utils import benjamini_hochberg


@dataclass(frozen=True)
class HypothesisTestResult:
    table: pd.DataFrame


def _cohen_d(x: np.ndarray, y: np.ndarray) -> float:
    x = x.astype(float)
    y = y.astype(float)

    nx = x.size
    ny = y.size
    if nx < 2 or ny < 2:
        return float("nan")

    vx = x.var(ddof=1)
    vy = y.var(ddof=1)
    pooled = ((nx - 1) * vx + (ny - 1) * vy) / (nx + ny - 2)
    if pooled <= 0:
        return 0.0

    return float((x.mean() - y.mean()) / np.sqrt(pooled))


def run_feature_group_tests(X: pd.DataFrame, y: pd.Series, alpha: float = 0.05) -> HypothesisTestResult:
    """Welch t-test (high vs low quality) for numeric features.

    This is intended as exploratory hypothesis support, not a causal claim.
    """
    if set(y.unique()) - {0, 1}:
        raise ValueError("y must be binary (0/1)")

    num_cols = X.select_dtypes(include=[np.number]).columns

    rows: list[dict[str, float | str]] = []
    p_values: list[float] = []

    x_hi = X[y == 1]
    x_lo = X[y == 0]

    for col in num_cols:
        a = x_hi[col].dropna().to_numpy()
        b = x_lo[col].dropna().to_numpy()
        if a.size < 2 or b.size < 2:
            continue

        t_stat, p = ttest_ind(a, b, equal_var=False)
        d = _cohen_d(a, b)

        row = {
            "feature": str(col),
            "mean_high": float(np.mean(a)),
            "mean_low": float(np.mean(b)),
            "mean_diff": float(np.mean(a) - np.mean(b)),
            "t_stat": float(t_stat),
            "p_value": float(p),
            "cohen_d": float(d),
        }
        rows.append(row)
        p_values.append(float(p))

    if not rows:
        return HypothesisTestResult(table=pd.DataFrame())

    p_arr = np.asarray(p_values, dtype=float)
    bh = benjamini_hochberg(p_arr, alpha=alpha)

    table = pd.DataFrame(rows)
    table["p_adj_bh"] = bh.p_adjusted
    table["reject_fdr"] = bh.rejected

    table = table.sort_values(by=["p_adj_bh", "p_value"], ascending=True)
    return HypothesisTestResult(table=table)
