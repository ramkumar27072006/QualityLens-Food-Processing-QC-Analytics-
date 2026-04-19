# Week 6 — End-to-End Project Documentation and Future Roadmap

This document integrates the Week 1→5 artifacts into a single, auditable workflow.

## Project Overview
- Objective: build a reproducible analytics pipeline for food-quality prediction and risk-aware evaluation.
- Dataset: UCI Wine Quality (red + white), used as a food-quality stand-in with measurable chemical attributes and a quality score.

## Dataset & Preparation (Results)
- Raw rows/cols: **6497** / **13**
- Missing values: **0**
- Exact duplicates detected: **1177**
- Wine types: red=1599, white=4898

Artifacts: `weeks/week-01/outputs/overview.json`

### Cleaning & Validation (Week 2)
- Rows before/after: **6497 → 5320**
- Duplicates removed: **1177**
- Missing values after: **0**

Artifacts: `weeks/week-02/outputs/cleaning_report.json`

### Features & Target (Week 3)
- Target: quality >= 7
- Rows/features: **5320** / **19**
- Positive rate: **0.1897**

Artifacts: `weeks/week-03/outputs/feature_metadata.json`

## Modeling & Evaluation Summary
### Holdout Baselines (Week 3/5)
(threshold=0.5)
- rf: ROC-AUC **0.873**, PR-AUC **0.626**, Precision **0.696**, Recall **0.317**
- logreg: ROC-AUC **0.819**, PR-AUC **0.473**, Precision **0.401**, Recall **0.797**

Artifacts: `weeks/week-03/outputs/baseline_metrics.csv`

### Cross-Validation (Week 4)
- rf: ROC-AUC **0.857 ± 0.014**, PR-AUC **0.588 ± 0.033**
- logreg: ROC-AUC **0.832 ± 0.019**, PR-AUC **0.519 ± 0.029**

Artifacts: `weeks/week-04/outputs/cv_model_comparison.csv`

### Hypothesis Testing Highlights (Week 4)
Top 5 features by BH-adjusted p-value (Welch t-test, effect size = Cohen’s d):
- alcohol: mean_diff 1.2636, d=1.173, p_adj=2.21e-174
- density_alcohol: mean_diff 1.2313, d=1.170, p_adj=2.21e-174
- density: mean_diff -0.0022, d=-0.787, p_adj=2.20e-97
- chlorides_log: mean_diff -0.0140, d=-0.440, p_adj=2.81e-61
- chlorides: mean_diff -0.0151, d=-0.416, p_adj=1.63e-58

Artifacts: `weeks/week-04/outputs/hypothesis_tests.csv`

### Best Holdout Snapshot (Week 5)
- Best ROC-AUC model: **rf**
- ROC-AUC: **0.873**
- PR-AUC: **0.626**

Artifacts: `weeks/week-05/outputs/test_metrics.csv`

### Segment Reliability (Week 5, RF by wine_type)
- red (n=275): ROC-AUC **0.922**, PR-AUC **0.730**
- white (n=789): ROC-AUC **0.853**, PR-AUC **0.602**

Artifacts: `weeks/week-05/outputs/segment_metrics_rf.csv`

### Drift & Monitoring Seed (Week 5)
- Largest KS statistic (train vs test): volatile_acidity = **0.043** (p=0.090)
- Interpretation: this split shows low drift; in production, run the same checks over time windows.

Artifacts: `weeks/week-05/outputs/train_test_drift_ks.csv`

## Challenges & Learnings
- Duplicates: raw data contained many exact duplicates; deduplication materially changed row count (6,497 → 5,320).
- Class imbalance: high-quality is ~19% overall, so PR-AUC and threshold trade-offs matter.
- Segment differences: performance differs by wine type; this mirrors multi-line/facility deployment risk.

## Future Roadmap (Food Processing Extension)
- Incorporate time-series sensors (temperature/pH/flow) with phase-aware aggregation.
- Add maintenance/sanitation logs and traceability joins (batch ↔ line ↔ supplier).
- Implement monitoring: drift checks, calibration tracking, and retraining triggers.
- Consider causal studies (designed experiments) before turning correlations into process changes.

## Reproducibility (Run Order)
- Week 1: `python scripts/02_week1_eda.py`
- Week 2: `python scripts/03_week2_clean.py`
- Week 3: `python scripts/04_week3_features_and_baseline.py`
- Week 4: `python scripts/05_week4_modeling_and_hypothesis.py`
- Week 5: `python scripts/06_week5_evaluation_and_risk.py`
- Week 6: `python scripts/07_week6_docs.py`
