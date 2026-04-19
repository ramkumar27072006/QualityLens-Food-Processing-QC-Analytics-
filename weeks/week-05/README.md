# Week 5 — Model Evaluation Framework and Risk Assessment (Implemented)

## What I did
- Evaluated trained models on a holdout test set and produced calibration curves.
- Computed segment-wise reliability (metrics by `wine_type`) to surface generalization gaps.
- Implemented a basic drift check (KS tests) comparing train vs test feature distributions.

## Holdout evaluation results (real numbers)
From `outputs/test_metrics.csv` (threshold = 0.5):
- Random Forest: ROC-AUC **0.873**, PR-AUC **0.626**, Precision **0.696**, Recall **0.317**
- Logistic Regression: ROC-AUC **0.819**, PR-AUC **0.473**, Precision **0.401**, Recall **0.797**

## Segment reliability (by wine type)
From `outputs/segment_metrics_*.csv`:
- RF on **red**: ROC-AUC **0.922**, PR-AUC **0.730** (n=275)
- RF on **white**: ROC-AUC **0.853**, PR-AUC **0.602** (n=789)

This demonstrates why segment checks matter in food processing: performance can differ across product lines/conditions.

## Drift check (train vs test)
From `outputs/train_test_drift_ks.csv`:
- Largest KS statistic observed: **0.043** (volatile_acidity)
- p-values are not significant at conventional thresholds, consistent with a random split and low drift.

## How to reproduce
- `python scripts/06_week5_evaluation_and_risk.py`

## Outputs (generated)
- `outputs/test_metrics.csv` — test-set metrics per model
- `outputs/calibration_logreg.png`, `outputs/calibration_rf.png` — calibration curves
- `outputs/segment_metrics_logreg.csv`, `outputs/segment_metrics_rf.csv` — metrics by segment
- `outputs/train_test_drift_ks.csv` — drift indicators (KS statistic)

## Why this matters
In food processing, the cost of mistakes is asymmetric. Evaluation must cover more than accuracy: ranking quality (AUC), rare-event sensitivity (PR-AUC), calibration, and performance consistency across segments.
