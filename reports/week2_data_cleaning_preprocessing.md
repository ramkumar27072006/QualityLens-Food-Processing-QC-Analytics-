# Week 2 Report: Data Cleaning and Preprocessing Strategy (Food Processing Datasets)

## 1. Executive Summary
This report defines a detailed, reproducible data cleaning and preprocessing strategy for food processing datasets, with a focus on quality metrics and in-line sensor readings from production environments. The plan emphasizes systematic data profiling, practical handling of missing values and outliers, unit/time standardization, and validation checks that reflect real constraints in food manufacturing (e.g., acceptable pH ranges, temperature compliance, and batch traceability).

The output of this plan is a blueprint: a step-by-step pipeline that transforms raw, heterogeneous inputs into an analysis-ready dataset suitable for exploratory modeling (Week 3) and predictive strategy design (Week 4).

## 2. Why Data Cleaning Matters in Food Processing
Food processing analytics is sensitive to data defects because decisions may affect safety, regulatory compliance, and production efficiency. Common issues include sensor dropouts, mis-calibrated probes, inconsistent sampling intervals, mixed units, and label noise in QA outcomes. A strong preprocessing plan reduces false conclusions and prevents model leakage (e.g., using “future” information to predict past outcomes).

## 3. Data Profiling Plan
Before modifying any data, the dataset is assessed to quantify quality issues.

### 3.1 Structural checks
- Validate schema (expected columns, data types, primary keys).
- Confirm grain:
  - Batch-level (one row per batch/lot)
  - Time-series (one row per timestamp per sensor)
- Identify duplicates (exact duplicates; near-duplicates with minor timestamp shifts).

### 3.2 Statistical profiling
- Missingness rate per column and per segment (product line, facility, shift).
- Distribution review (skewness, heavy tails, multimodality).
- Range checks using domain knowledge (e.g., temperature, pH, moisture).
- Cardinality and rare-category detection for categorical fields.

### 3.3 Time-series-specific profiling (if applicable)
- Sampling frequency consistency (expected interval vs observed interval).
- Gaps, spikes, and flatlines (potential sensor failure).
- Clock alignment issues (time zones, daylight saving changes).

## 4. Data Cleaning Techniques
### 4.1 Handling missing data
**Step 1: Classify missingness**
- Not recorded (sensor outage), not applicable (field irrelevant), or unknown.

**Step 2: Choose an approach by variable type and missingness pattern**
- Numeric sensor data:
  - Short gaps: forward-fill/back-fill with maximum gap threshold.
  - Longer gaps: interpolation (linear) or model-based imputation, with flags.
- Batch-level lab metrics:
  - Impute with group statistics (by product/facility) when defensible.
  - Otherwise, keep missing and create “missing indicator” features.
- Categorical:
  - Standardize “Unknown/Not Recorded” categories.

**Guardrails**
- Never impute the target label with information derived from the future.
- Always create audit columns: `was_imputed`, `imputation_method`, `imputation_group`.

### 4.2 Duplicate handling
- Remove exact duplicates.
- Investigate near-duplicates:
  - Keep the record with the most complete fields.
  - For sensor streams, aggregate duplicates using median/mean per timestamp.

### 4.3 Outlier detection and treatment
Outliers are common in sensor data; treat carefully to avoid removing true process deviations.

**Detection methods (choose based on context)**
- Rule-based thresholds (domain constraints): e.g., pH cannot be negative.
- Robust statistics: IQR rule, Median Absolute Deviation (MAD).
- Model-based anomaly scores (conceptual, optional): Isolation Forest for multivariate sensor patterns.

**Treatment strategies**
- If confirmed error: remove or set to missing + impute (with flags).
- If plausible process deviation: keep, but annotate with `anomaly_flag`.
- Winsorization (cap extremes) only when aligned with business meaning.

### 4.4 Consistency fixes and standardization
- Unit normalization (°C vs °F; mg/L vs ppm; minutes vs seconds).
- Standardize category labels (trim whitespace, unify casing, map synonyms).
- Timestamp normalization:
  - Convert to ISO format.
  - Normalize time zone.
  - Ensure monotonic ordering within batch/sensor.

### 4.5 Traceability and join integrity
Food processing analytics often requires joins across:
- Batch master data
- Lab results
- Sensor streams
- QA inspections
- Cleaning/maintenance logs

**Join checks**
- One-to-one vs one-to-many expectations.
- Orphan records and unexpected fan-outs.
- Coverage metrics: % batches that have lab tests; % batches with complete sensor windows.

## 5. Preprocessing Steps (Analysis-Ready Dataset)
### 5.1 Feature-ready transformations
- Scaling/normalization for numeric variables:
  - StandardScaler for symmetric distributions
  - RobustScaler for heavy-tailed noise
- Encoding categorical variables:
  - One-hot encoding for low/medium cardinality
  - Group rare categories into “Other” to avoid sparsity
- Datetime feature creation (if timestamps exist):
  - Shift/day-of-week/seasonality flags (only when meaningful)

### 5.2 Time-series preprocessing (if applicable)
- Resample to a consistent interval (e.g., 1-min, 5-sec) as appropriate.
- Smooth noise cautiously (rolling median) to reduce spikes while preserving events.
- Align sensor windows to process phases (mixing, heating, cooling, packaging).

### 5.3 Leakage prevention and split strategy
- If predicting batch outcomes, ensure features come from data available **before** the outcome is known.
- Use time-based splits when data is chronological.
- Keep facility/product segmentation in mind to test generalization.

### 5.4 Data validation checks (must-pass rules)
- Schema validation (types, required columns).
- Range checks:
  - Temperature, pH, moisture, water activity, etc.
- Logical consistency:
  - Start time < end time
  - Batch_id present for all sensor rows
  - Non-negative counts and durations
- Distribution drift checks (basic): compare train vs validation distributions for key features.

## 6. Documentation and Reproducibility Plan
A cleaning strategy is only useful if it is repeatable.

**Documentation artifacts**
- Data dictionary with units and allowed ranges.
- Cleaning log capturing:
  - rows removed
  - fields imputed
  - outliers flagged
  - unit conversions applied
- Versioning approach:
  - Store raw vs cleaned dataset snapshots separately.
  - Maintain configuration files describing thresholds and rules.

**Traceability principle**
Every transformation must be explainable and reversible at the rule level (even if not reversible row-by-row).

## 7. Work Plan and Timeline (30–35 Hours)
- Profiling + issue inventory (7–8h)
- Missing data strategy + imputation rules (6–7h)
- Outlier/anomaly plan + decision criteria (6–7h)
- Standardization (units, categories, timestamps) + join integrity plan (5–6h)
- Validation checks + documentation template (6–7h)

## 8. Expected Challenges and Solutions
- **Sensor drift and calibration**: include per-sensor baseline checks; flag long-term drift for later modeling.
- **Mixed granularity** (batch vs time-series): define aggregation rules (min/max/mean/percentile) with phase-aware windows.
- **Label noise** in QA outcomes: keep uncertainty flags; avoid overconfident conclusions.
- **Class imbalance** (few failures): plan stratified sampling and metrics suited to rare events.

## 9. Week 2 Deliverables Checklist
- Full cleaning and preprocessing blueprint
- Missing value handling rules + audit flags
- Outlier detection and treatment plan
- Normalization/encoding strategy
- Validation checklist and reproducibility documentation outline
