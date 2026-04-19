from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class BHResult:
    p_adjusted: np.ndarray
    rejected: np.ndarray


def benjamini_hochberg(p_values: np.ndarray, alpha: float = 0.05) -> BHResult:
    """Benjamini–Hochberg FDR control.

    Returns adjusted p-values and boolean rejections.
    """
    p = np.asarray(p_values, dtype=float)
    if p.ndim != 1:
        raise ValueError("p_values must be 1D")

    n = p.size
    order = np.argsort(p)
    ranked = p[order]

    # Compute adjusted p-values
    adjusted = np.empty(n, dtype=float)
    prev = 1.0
    for i in range(n - 1, -1, -1):
        rank = i + 1
        val = ranked[i] * n / rank
        prev = min(prev, val)
        adjusted[i] = prev

    # Map back to original order
    p_adj = np.empty(n, dtype=float)
    p_adj[order] = np.clip(adjusted, 0.0, 1.0)

    rejected = p_adj <= alpha
    return BHResult(p_adjusted=p_adj, rejected=rejected)
