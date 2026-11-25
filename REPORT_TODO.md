# Report TODO — parts YOU must write

Interpretation and discussion text is written by the student (exam rule). This file only lists the
questions to answer; it contains no answers. Tick `[x]` when the paragraph is written in `report/main.tex`.

## General (whole report)
- [ ] Title page: name, student ID, public GitHub/Colab link (`main.tex` author block)
- [ ] Section 1: motivation, research questions, dataset descriptions (cite `\cite{telco}`, `\cite{pace1997}`)
- [ ] Section 4: describe the validation scheme in your own words (60/20/20, 5-fold StratifiedKFold on train, Macro-F1, seed 463, test used once)
- [ ] Section 8: LLM Usage Disclosure (tool, purpose, example prompts; source: `LLM_USAGE_LOG.md`)
- [ ] Remove `\nocite{*}` once all references are cited in the text
- [ ] Insert Q1 tables/figures into `main.tex` (planned: after Q1e, in one batch)

## Q1a — Data audit (notebook `01_Q1_data_leakage.ipynb`, report Section 2)
- [ ] 1. **Imbalance:** exact class ratio; what it implies for metrics (accuracy of the majority-class baseline)
- [ ] 2. **Missing values:** how many, which column, what the affected rows share (`tenure`, `Contract`); unknown vs. structurally missing; is median imputation sensible for them?
- [ ] 3. **Duplicates:** with/without `customerID`; conflicting labels; real identical customers or data errors? groups crossing splits — does it matter?
- [ ] 4. **Anomalies:** impossible/out-of-range values; `tenure == 0`; skewness of `TotalCharges`
- [ ] 5. **Redundancy:** `TotalCharges` vs `tenure × MonthlyCharges` (r = 0.9996) — consequences for LR (collinearity), NB (independence), importance (Q4e); keep or drop?
- [ ] 6. **Problematic predictors:** `customerID`; rare levels; structurally dependent `No internet service` / `No phone service` levels and one-hot encoding
- [ ] 7. **Target relations (train only):** strongest univariate differences in churn rate (descriptive, not causal)
- [ ] State the protocol: descriptive checks on full data, target-related analysis on train only, test never inspected

## Q1b — Split comparison (report Sections 4/5)
- [ ] 1. Exact split sizes and why 7,043 cannot be split exactly 60/20/20
- [ ] 2. Stratified vs random over 200 seeds: mean/max deviation (pp), share > 1 pp; practical importance for val/test of 1,409 rows
- [ ] 3. Deviation vs dataset size: around which n random splitting becomes a problem
- [ ] 4. CV folds: share of `KFold` folds with zero churners at n = 30; effect on Macro-F1 / ROC-AUC (lecture warning)
- [ ] 5. When stratification fails / is not enough: very rare classes, grouped data (`GroupKFold`), time series (`TimeSeriesSplit`), regression (binned target), multi-label
- [ ] 6. Why the class ratio of the test part is not "looking at the test set"

## Q1c — Preprocessing
_(added when Q1c is written)_

## Q1d — Leakage demo
_(added when Q1d is written)_

## Q1e — Audit table, protocol diagram, failure modes
_(added when Q1e is written)_

## Q2 – Q5
_(added as each question is completed)_
