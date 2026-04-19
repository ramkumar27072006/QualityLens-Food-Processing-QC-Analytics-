# Week 2 — Data Cleaning and Preprocessing (Implemented)

## What I did
- Implemented a cleaning and preprocessing pipeline that produces a cleaned dataset plus a structured cleaning report.
- Added safety-oriented checks (e.g., sulfur consistency flag) and outlier flagging (IQR-based) without deleting data blindly.

## Cleaning results (real numbers)
From `outputs/cleaning_report.json`:
- Rows before: **6,497**
- Exact duplicates removed: **1,177**
- Rows after: **5,320**
- Missing values before/after: **0 → 0** (no imputation required)
- New validation column added: `flag_free_sulfur_gt_total`
	- Count flagged True (in cleaned data): **0** (dataset is logically consistent for this rule)

Post-cleaning segment sizes (after dedup): **3,961 white**, **1,359 red**

## Outlier exploration (IQR flagging only)
Top IQR outlier counts (no automatic deletion):
- `fixed_acidity`: 304
- `volatile_acidity`: 279
- `chlorides`: 237
- `sulphates`: 163
- `citric_acid`: 143

These are treated as investigation cues; in food processing, extremes can be real process deviations.

## How to reproduce
- `python scripts/03_week2_clean.py`

## Outputs (generated)
- `data/processed/wine_quality_clean.csv` — cleaned dataset
- `data/processed/cleaning_report.json` — structured report
- `outputs/cleaning_report.json` — week-wise copy of the report
- `outputs/outlier_counts.png` — top outlier counts (flagging only)

## Why this matters
Food processing data is rarely perfect. Cleaning must be explainable and reproducible. This week’s output is a blueprint implemented as code: it records what changed (duplicates removed), what was checked (consistency flags), and what was detected (outlier counts) so later modeling decisions can be defended.
