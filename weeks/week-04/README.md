# Week 4 — Predictive Modeling Strategy and Hypothesis Testing (Implemented)

## What I did
- Added a cross-validated model comparison (ROC-AUC and PR-AUC).
- Ran statistical hypothesis tests to quantify which numeric features differ significantly between high-quality vs low-quality classes (with FDR control).

## Predictive objective (implemented)
- Problem framing: predict whether a batch is **high quality (quality ≥ 7)** using measurable chemistry variables.
- This mimics a QC classification scenario: flag higher-quality vs lower-quality batches based on upstream measurements.

## Cross-validation results (5-fold CV)
From `outputs/cv_model_comparison.csv`:
- Random Forest: ROC-AUC **0.857 ± 0.014**, PR-AUC **0.588 ± 0.033**
- Logistic Regression: ROC-AUC **0.832 ± 0.019**, PR-AUC **0.519 ± 0.029**

## Hypothesis testing highlights (Welch t-test + Cohen’s d, FDR controlled)
From `outputs/hypothesis_tests.csv` (high vs low quality):
- `alcohol`: mean diff **+1.264**, Cohen’s d **+1.173** (very large effect)
- `density`: mean diff **−0.00223**, Cohen’s d **−0.787**
- `volatile_acidity`: mean diff **−0.0619**, Cohen’s d **−0.372**

Note: these are association-based results used to prioritize drivers for modeling and process insight; they do not establish causality.

## How to reproduce
- `python scripts/05_week4_modeling_and_hypothesis.py`

## Outputs (generated)
- `outputs/cv_model_comparison.csv` — 5-fold CV comparison across baseline models
- `outputs/hypothesis_tests.csv` — Welch t-tests + Cohen’s d + BH-adjusted p-values

## Notes
This week’s tests are **exploratory**: they support association-based hypotheses and help prioritize drivers, but they are not a claim of causality.
