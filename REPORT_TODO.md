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

## Q1c — Preprocessing (report Section 2)
- [ ] 1. **Pipeline:** each step (median imputation → standardisation; most-frequent imputation → one-hot `handle_unknown='ignore'`) and why it is there
- [ ] 2. **Fit on train only:** what the learned-statistics table proves; why scaled validation mean/std are close to but not exactly 0/1, and why that is correct
- [ ] 3. **Missing `TotalCharges`:** value given to the 11 rows; is the train median sensible for `tenure = 0`? one alternative (0, `tenure × MonthlyCharges`) and its trade-off
- [ ] 4. **Unseen categories:** what `handle_unknown='ignore'` does; why safer than an error; what information is lost
- [ ] 5. **Scaling sensitivity:** which models change, by how much, and why (distance, regularisation/solver iterations, threshold splits, per-feature Gaussian)
- [ ] 6. **Requirements table:** the *reason* behind each Yes/No per model family; mention Categorical NB (Q2b)
- [ ] 7. **Design decisions:** `SeniorCitizen` as categorical; `TotalCharges` kept (r = 0.9996); one-hot without `drop='first'`

## Q1d — Leakage demo (report Sections 2/5)
- [ ] 1. **Size of the effect:** valid vs INVALID on CV estimate and on validation score; optimism (CV − val) per experiment
- [ ] 2. **Mechanism:** which information from the held-out folds reached training in each INVALID procedure
- [ ] 3. **Pure noise, n = 200 vs 4,225:** why inflation is larger with few rows / many features (multiple comparisons, p ≫ n); what the honest score should be
- [ ] 4. **Real features + noise:** why the effect is smaller; does "small here" make it acceptable?
- [ ] 5. **Target-encoded `customerID`:** why INVALID CV is near-perfect but validation is not; how cross-fitted `TargetEncoder` prevents it; a realistic example
- [ ] 6. **Scaling/imputation on all training rows:** report the (small) difference honestly; why small; why still a violation and when it could matter more
- [ ] 7. **General lesson:** when a CV estimate is trustworthy ("every learned step inside the pipeline")
- [ ] Make sure every INVALID result in the report is labelled "INVALID – demonstration only"

## Q1e — Audit table, protocol diagram, failure modes
_(added when Q1e is written)_

## Q2 – Q5
_(added as each question is completed)_
