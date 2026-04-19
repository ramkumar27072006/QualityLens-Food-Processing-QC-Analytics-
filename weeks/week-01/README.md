# Week 1 — Data Exploration and Strategic Planning (Implemented)

## What I did
- Selected a real **public** food-quality dataset (UCI Wine Quality: red + white).
- Implemented a reproducible EDA workflow that produces objective artifacts (JSON summaries + plots), not just narrative text.

## Dataset summary (real results)
From `outputs/overview.json` (after combining red + white):
- Rows: **6,497**
- Columns: **13** (11 numeric chemistry variables + `quality` + `wine_type`)
- Missing values: **0** (dataset is complete)
- Exact duplicates detected: **1,177** (handled in Week 2)
- Wine types: **1,599 red**, **4,898 white**

Quality label distribution (counts):
- 3: 30, 4: 216, 5: 2,138, 6: 2,836, 7: 1,079, 8: 193, 9: 5

## EDA insights (food-quality framing)
Using the cleaned dataset (Week 2 output) for stable analysis, numeric correlations with `quality` show:
- Strongest positive: `alcohol` (**+0.469**)
- Strongest negative: `density` (**−0.326**), `volatile_acidity` (**−0.265**), `chlorides` (**−0.202**)

Interpretation (high level): higher alcohol content aligns with higher quality scores, while higher density / volatile acidity tend to align with lower quality. These are not causal claims; they are early prioritization signals for cleaning rules, feature engineering, and hypothesis testing.

## Strategic plan (30–35 hours, feasible)
- 6–7h: dataset sourcing + licensing notes + target definition
- 8–10h: EDA execution (profiling, distributions, correlations) + artifact packaging
- 6–7h: define validation rules (ranges/units/consistency) and data dictionary template
- 5–6h: stakeholder-style interpretation (risks, priorities, candidate drivers)
- 5h: reporting and reproducibility polish (folder structure, scripts, README)

## Data sources (public)
Primary dataset used here is documented in `data/raw/DATASET_SOURCES.md`.
Additional relevant sources you can cite (optional, depending on scope): USDA FoodData Central, Open Food Facts, FDA recalls/enforcement datasets, and academic repositories (UCI/Kaggle) with clear licensing.

## How to reproduce
From repo root:
- `python scripts/02_week1_eda.py`

This script also downloads the dataset if it is not present.

## Outputs (generated)
See `outputs/`:
- `overview.json` — dataset shape, dtypes, missingness, duplicates, quality distribution
- `summary_stats.csv` — descriptive statistics
- `quality_distribution.png` — target distribution (by wine type)
- `missingness.png` — missing-value overview
- `correlation_heatmap.png` — numeric feature correlation map

## Why this matters (food processing framing)
Even when the dataset is “lab-style” rather than high-frequency sensors, the Week 1 process is the same in production environments: validate grain and target definition, quantify missingness/duplicates, map variables to quality meaning, and detect early signals (correlations, distribution shifts) that inform later cleaning, feature engineering, and modeling.
