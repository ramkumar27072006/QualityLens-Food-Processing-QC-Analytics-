# Week 3 — Feature Engineering and Exploratory Modeling (Implemented)

## What I did
- Implemented feature engineering (interpretable derived features) and an exploratory modeling baseline.
- Trained two baseline models (logistic regression + random forest) on a binary “high quality” target.

## Feature dataset (real numbers)
From `outputs/feature_metadata.json`:
- Rows: **5,320**
- Features (X columns): **19**
- Target rule: **high quality = quality ≥ 7**
- Positive rate: **18.97%** (1,009 / 5,320)
	- By wine type (cleaned data): red **13.54%**, white **20.83%**

## Baseline model results (holdout test split)
From `outputs/baseline_metrics.csv` (threshold = 0.5):
- Random Forest: ROC-AUC **0.873**, PR-AUC **0.626**, Precision **0.696**, Recall **0.317**
- Logistic Regression: ROC-AUC **0.819**, PR-AUC **0.473**, Precision **0.401**, Recall **0.797**

Interpretation: RF ranks batches better (higher AUC), while logistic regression is more recall-heavy at the default 0.5 threshold (more positives predicted, lower precision). This trade-off is important for quality-control escalation policies.

## Top drivers (model-extracted)
- RF feature importance (top): `density_alcohol`, `alcohol`, `density`, `volatile_acidity`
- Logistic regression (strong negatives): `density`, `volatile_acidity`; strong positives: `residual_sugar_log`, `sugar_to_alcohol`, `ph`

## How to reproduce
- `python scripts/04_week3_features_and_baseline.py`

## Outputs (generated)
- `data/processed/wine_quality_features.csv` — features + binary target
- `outputs/feature_metadata.json` — target definition and feature counts
- `outputs/baseline_metrics.csv` — baseline model performance on a holdout set
- `outputs/roc_pr_logreg.png`, `outputs/roc_pr_rf.png` — ROC + PR curves
- `outputs/logreg_top_coefficients.csv` — top positive/negative drivers (interpretable)
- `outputs/rf_feature_importances.csv` — tree-based importance ranking

## Why this matters
Feature engineering captures process-relevant signals (ratios, exposure proxies, transformed distributions). Exploratory models validate that engineered features carry signal and remain interpretable enough for quality-control settings.
