# CLAUDE.md — CENG 463 Take-Home Midterm

This file summarises the earlier claude.ai conversation. Claude Code must read this file before working on this project and follow the rules below.

## User and communication
- The user is a Computer Engineering student at IZTECH (İYTE); course **CENG 463 – Introduction to Machine Learning** (Prof. Dr. Aytuğ Onan, Fall 2026–27).
- Talk to the user in **Turkish**. Code, comments, file names and report text may be in **English**.
- The user wants to proceed step by step: at each step, briefly and clearly explain what is being done and why.
- **Git/GitHub operations (add, commit, push) are done by the user.** Claude never commits or pushes. When a piece of work is done, Claude says "time to push" and gives the commands (with a suggested commit message); the user types them in the terminal.
- Code examples and topics should be tied to the approaches covered in lectures and labs whenever possible (see below).

## ⚠️ Permissions — binding rules for Claude (set by the user on 2026-11-25)
The Claude Code permission mode may stay on "Auto", but Claude must behave as if every action needs approval:
- **Claude does NOT run any commands** (Bash/PowerShell/terminal), **does NOT install** programs, packages or extensions, and **does NOT download** data or files. For these tasks Claude only shows the steps and the exact commands; the user runs them.
- **Before writing or editing any code file**, Claude explains what it will write and why, and waits for the user's explicit approval.
- Claude does nothing that the user has not approved and has not had explained.
- Read-only inspection of project files (reading, searching) is allowed when needed to give guidance.
- **Notebooks:** before editing a notebook, Claude asks the user to **close it in VS Code** (otherwise the open editor overwrites Claude's changes on save) and edits only after the user confirms.

## Working files — keep updated after every section (set by the user on 2026-11-25)
- **`REPORT_TODO.md`** (English): checklist of the interpretation questions the user must answer in the report, per sub-question. Questions only, never answers. Add the questions of each new section when its code is written.
- **`CALISMA_NOTLARI.md`** (Turkish, git-ignored, not part of the submission): whenever Claude explains a section, the explanation is also saved here in the format *Ne yaptık → Neden → Ne gördük (sayılar) → Kavram → Düşün*, plus a short summary per section. Concepts and guiding questions only — no ready-made interpretations to copy into the report. Numbers come only from outputs that were actually run.

## Task
**Take-Home Midterm** (20% of the grade, individual). 5 questions, all mandatory, 20 points each.
- **Deadline:** Officially **1 December 2026, 23:59** (Turkey time). The user's own target is **30 November**; 1 December is a buffer day.
- **Submission:** Only via **Microsoft Teams**. A single ZIP file: `CENG463_Midterm_<StudentID>.zip`
- **ZIP contents:** LaTeX source + compiled PDF report, runnable notebooks or scripts, `requirements.txt`, run instructions (README), saved tables and figures, hardware/software summary, and a **GitHub or Colab link** in the report (accessible to the instructor).
- **Grading (within each question):** methodological correctness 40%, depth of evidence-based analysis 30%, reproducibility and code quality 20%, report clarity 10%.

## ⚠️ Academic integrity — binding rules for Claude
According to the exam text, LLMs may be used **only for writing code, debugging and environment setup**.
- ✅ Allowed: writing code, debugging, guiding environment setup (steps only — see Permissions), preparing the LaTeX template and table/figure inclusion code, reminding of methodological requirements, showing the user **what they need to interpret**.
- ❌ Not allowed: writing the **scientific interpretation and discussion text** of the report (interpretation of results, discussion, limitations analysis, model-selection rationale). The user writes these. On request, Claude may point out technical errors in the user's text.
- ❌ **Never** fabricate results, metrics or observations. Every reported number must come from code that was actually run.
- The user must write an **"LLM Usage Disclosure"** section in the report: which tool, for what purpose, and example prompts. Record every significant piece of code help in `LLM_USAGE_LOG.md` with a short entry: date, task and what was done.

## General protocol (applies to every question)
- `SEED = 463`. All randomness is tied to this seed: numpy, sklearn `random_state`, bootstrap, corruptions.
- **Split first, then fit.** Train/validation/test splits are made before any transformation is fitted. **Exact split sizes** are reported.
- Classification data: **60% / 20% / 20% stratified** split. Indices are saved to `results/splits/clf_split_indices.csv` and **all notebooks read the same file** (Q1, Q2, Q4, Q5).
- All preprocessing (imputation, scaling, encoding, feature selection, vectorization) is done **inside a `Pipeline` / `ColumnTransformer`**. In CV it is fitted only on the training part of each fold.
- **Hyperparameter tuning:** `GridSearchCV` with **5-fold StratifiedKFold** on the training data. Selection metric: **Macro-F1**. All models use **the same folds** (the `cv` object is defined in one place in `utils.py`).
- Comparisons and analyses (Q2c–e, Q4, Q5b–c) are done on the **validation** set.
- **THE TEST SET IS NOT OPENED UNTIL Q5e.** No tuning or selection decision is made by looking at test metrics. Q3 has its own regression test set, used only once at the end of Q3.
- For each model, record the search space (grid), selection metric, pipeline steps and run times. All tables are saved as `results/tables/*.csv`, all figures as `results/figures/*.png` (dpi ≥ 150).
- If computation is heavy, the dataset may be reduced **consistently and transparently**, but the number of required comparisons may not be reduced. Any reduction is stated in the report.
- The invalid leakage demo is clearly labelled **`INVALID – demonstration only`** in code and outputs and is not used anywhere else.

## Datasets (proposed in the earlier conversation; final once the user confirms)
- **Classification (Q1, Q2, Q4, Q5): IBM Telco Customer Churn** (Kaggle). 7,043 rows, binary target `Churn` (about 26% Yes), mixed feature types.
  - `TotalCharges` is read as string; 11 blank values → `pd.to_numeric(errors='coerce')`.
  - `customerID` is an ID column → dropped from the model.
  - `TotalCharges` ≈ `tenure × MonthlyCharges` → high correlation.
  - Alternative: UCI Bank Marketing. Larger, but its `duration` column is a natural leakage example.
- **Regression (Q3): California Housing** (`sklearn.datasets.fetch_california_housing`).
  - No missing values.
  - Target is capped at 5.0 (about 965 rows).
  - Correlated pairs: `AveRooms`–`AveBedrms`, `Latitude`–`Longitude`.
  - Extreme outliers in `AveOccup` and `AveRooms`.
  - Target unit: $100,000.

## Project structure
```
CENG463_Midterm/
├── CLAUDE.md
├── README.md                 # setup + step-by-step run instructions
├── requirements.txt
├── environment.txt           # python/library versions, CPU, RAM
├── LLM_USAGE_LOG.md          # log for the disclosure section
├── data/                     # raw data (or download instructions)
├── src/utils.py              # SEED, load_data, make_split, load_split, build_preprocessor,
│                             # cv object, metric functions, save_table, save_fig, timer
├── notebooks/
│   ├── 00_setup_split.ipynb
│   ├── 01_Q1_data_leakage.ipynb
│   ├── 02_Q2_classification.ipynb
│   ├── 03_Q3_regression.ipynb
│   ├── 04_Q4_trees_ensembles.ipynb
│   └── 05_Q5_robustness_selection.ipynb
├── results/
│   ├── splits/  tables/  figures/
│   ├── frozen_configs.json   # settings + selection rule frozen before Q5e
│   └── models/               # joblib
└── report/
    ├── main.tex  (9 mandatory sections)
    ├── figures/  (link to or copy of results/figures)
    └── main.pdf
```

## Per-question checklist

### Q1 – Data preparation, leakage, experimental design
- [ ] **a)** Domain, target, feature types, sample count, class distribution. Missing values, duplicates (with and without `customerID`), anomalous values, problematic predictors (ID, `TotalCharges` correlation, rare or dependent categories).
- [ ] **b)** 60/20/20 stratified split + size table. **Stratified vs. random comparison:** over 200 seeds, the absolute deviation of each split's positive rate from the full data (mean, max, std) + boxplot. When each method fails: random on small or imbalanced data; stratified with very rare classes, grouped data or time series.
- [ ] **c)** Numeric: `SimpleImputer(median)` → `StandardScaler`. Categorical: `SimpleImputer(most_frequent)` → `OneHotEncoder(handle_unknown='ignore')`. Table of which transformation each model family needs (LR and k-NN need scaling; trees do not, but sklearn requires encoding; NB depends on the variant).
- [ ] **d)** Compare the valid pipeline with an **INVALID** method on the same CV folds. Suggestions: (1) add 200 noise columns and fit `SelectKBest` on all rows, (2) target encoding computed on all data. Scaling on all data is also tried, and if the difference is small it is reported honestly.
- [ ] **e)** Dataset audit table (column, type, missing count/ratio, unique values, min/max or most frequent value, note). Protocol diagram (TikZ or draw.io). At least 3 failure modes that could invalidate the result even if the code runs.

### Q2 – Classification and error analysis
- [ ] **a)** `DummyClassifier(most_frequent)`, Logistic Regression, Naive Bayes (variant choice justified), k-NN.
- [ ] **b)** At least 2 hyperparameters per model, same CV:
  - LR: `C ∈ {0.01, 0.1, 1, 10, 100}` × `class_weight ∈ {None, 'balanced'}`
  - NB: GaussianNB `var_smoothing ∈ logspace(-12, -3)` + representation comparison (Gaussian+scaled vs. `KBinsDiscretizer`+CategoricalNB, `alpha ∈ {0.1, 0.5, 1, 2}`, `n_bins ∈ {5, 10}`)
  - k-NN: `n_neighbors ∈ {1, 3, 5, 11, 21, 41}` × `weights ∈ {uniform, distance}` (optional `p ∈ {1, 2}`)
- [ ] **c)** On validation: Accuracy, Macro-F1, per-class P/R/F1, confusion matrix (counts + normalised), ROC-AUC, PR-AUC and curves. Justify which metric is most appropriate (imbalanced data → Macro-F1, PR-AUC, churn recall).
- [ ] **d)** Per-class errors. Controlled intervention: `class_weight='balanced'` vs. unweighted (or oversampling only on the training fold, with an imblearn Pipeline). Optional: threshold tuning on validation.
- [ ] **e)** At least 10 validation examples misclassified by the final candidate: table (features, true, predicted, probability), error categories, relation to input features, concrete improvement suggestions. **Test labels are not looked at.**

### Q3 – Regression, regularization, generalization (California Housing)
- [ ] **a)** Missing data, target distribution (skewness, 5.0 cap), correlation matrix, outliers. 60/20/20 split (KFold). Scaling inside the pipeline.
- [ ] **b)** `DummyRegressor`, `LinearRegression`, `Ridge`, `Lasso`, `DecisionTreeRegressor`, `RandomForestRegressor`.
- [ ] **c)** Train and validation complexity curves for polynomial degree 1–4 (+ Ridge with small alpha) and tree depth 1–20. Interpretation via bias-variance. Optional: `learning_curve`.
- [ ] **d)** CV tuning of `alpha ∈ logspace(-4, 2)` for Ridge and Lasso. Coefficient path plot. Number of coefficients zeroed by Lasso. Comparison table of OLS, Ridge and Lasso coefficients for the correlated pairs.
- [ ] **e)** MAE, RMSE, R² (unit: $100,000). Predicted vs. actual and residual vs. predicted plots. Individual inspection of at least the 5 largest validation residuals (cap point? extreme `AveOccup`?). Residual pattern (heteroscedasticity). Final Q3 test once.

### Q4 – Decision trees, bagging, boosting
- [ ] **a)** DT, RF, AdaBoost, GB + the best non-tree model from Q2 (reference). Same protocol.
- [ ] **b)** DT: `criterion ∈ {gini, entropy, log_loss}`, `max_depth`, `min_samples_leaf`, `ccp_alpha` (or `max_leaf_nodes`). For a tree of depth ≤ 3: `plot_tree` + `export_text` and interpretation of at least 3 decision paths.
- [ ] **c)** RF: `n_estimators ∈ {50, 100, 200, 400}`, `max_depth ∈ {5, 10, None}`, `max_features ∈ {'sqrt', 'log2', 0.5, None}`. Train and validation scores, OOB. Evidence: mean pairwise correlation between trees' validation predictions for different `max_features` values. Lab 07 formula: Var = σ²(ρ + (1−ρ)/B).
- [ ] **d)** AdaBoost and GB: `n_estimators ∈ {50, 100, 200, 400}` × `learning_rate ∈ {0.05, 0.1, 0.5, 1.0}`. Plot of validation Macro-F1 vs. number of estimators using `staged_predict`. Sequential error correction vs. independent bagging.
- [ ] **e)** Table: Macro-F1, Accuracy, train time, inference time (`time.perf_counter`). Built-in importance side by side with permutation importance on validation data. At least 2 cases where importance is misleading (correlated features, impurity favouring high-cardinality/continuous features, one-hot splitting, not causality).

### Q5 – Robustness, statistical comparison, model selection
- [ ] **a)** At least 4 candidates (LR, NB, RF, GB; optional k-NN). CV Macro-F1 on the same folds, mean ± std, per-fold boxplot.
- [ ] **b)** Robustness on validation: missing-value rate (0%, 10%, 30%, 50%) or numeric noise (σ = 0, 0.1, 0.3, 0.5 × feature std). The same corrupted set, generated **once** with a fixed seed, is used for all models. Plot Macro-F1 vs. severity.
- [ ] **c)** Paired bootstrap: sampling unit = validation example, B = 2000 (or 5000). Macro-F1 difference between two models in each resample, 95% percentile confidence interval + histogram. What it shows and what it does not.
- [ ] **d)** Multi-criteria table: performance, robustness, interpretability, train/inference cost, implementation complexity. 0–1 normalisation, justified weights (e.g. 0.40 / 0.20 / 0.15 / 0.15 / 0.10). Sensitivity analysis (±50% or 1000 random weight scenarios): does the winner change?
- [ ] **e)** Save hyperparameters and the selection rule to `results/frozen_configs.json` + models with joblib **before testing**. Evaluate all frozen candidates on the test set **once**. Final table, selected model (per the rule), limitations and threats to validity.

## Report (LaTeX, mandatory section order)
1. Introduction, research questions, datasets
2. Data audit, preprocessing, leakage controls
3. Methods and experimental design (Q1–5)
4. Validation scheme, tuning grids, random seeds, computing environment
5. Results (labelled tables and figures) and interpretation
6. Error analysis, robustness, uncertainty, limitations
7. Final model-selection rationale and test-set evaluation
8. LLM Usage Disclosure
9. References and reproducibility appendix (commands, links, configurations)

Claude may prepare the LaTeX skeleton, table/figure inclusion code and the reproducibility appendix. **The user writes the interpretation and discussion paragraphs.**

## Schedule
| Day | Work |
|---|---|
| Wed 25 Nov (evening) | Setup: repo, folders, `requirements.txt`, Overleaf/LaTeX template, data download, `utils.py`, `00_setup_split`. Start Q1a. |
| Thu 26 | All of Q1 + report section 2 |
| Fri 27 | All of Q2 + Q2 report part |
| Sat 28 | All of Q3 (separate dataset) + Q3 report part |
| Sun 29 | All of Q4 + Q5a in the evening |
| Mon 30 | Q5b–e (freeze → final test) + rest of the report, README, Restart & Run All, ZIP, upload to Teams |
| Tue 1 Dec | Buffer day (official deadline 23:59) |

## Code rules
- Every notebook imports from `src/utils.py` at the top and sets the seed. All notebooks must run without errors via **Restart & Run All**.
- Use `n_jobs=-1` for parallelism. Run times of long cells are measured and recorded.
- Every table is saved as CSV and in a LaTeX-includable form (`df.to_latex`).
- Versions are pinned with `pip freeze > requirements.txt`. `environment.txt` records Python version, OS, CPU and RAM.

## Course links (for reference in code and explanations)
- **L2 (Data & Learning):** train/test, 10-fold CV, overfitting, ZeroR baseline, accuracy/TP/FP/FN, ROC/AUC, F = 2TP/(2TP+FP+FN), confusion matrix. A class going missing in CV folds on imbalanced data (the R warning in L5 pp. 32–33).
- **L3 (Text Classification):** Naive Bayes, Laplace smoothing, Multinomial/Bernoulli/Gaussian variants.
- **L4 (Regression):** k-NN regression, inverse/Gaussian weighting, need for normalisation.
- **L5 (Decision Support):** entropy, information gain, overfitting and pruning, J48/CART.
- **L6 (Kernel & SVM):** RBF, C, γ.
- **L7 (Ensemble):** bias/variance, bagging reduces variance, boosting reduces bias, RF, AdaBoost, GB, XGBoost, stacking.
- **L8 (ANN):** softmax, cross-entropy, L2 regularization, gradient descent, ReLU hidden layer.
- **Labs (code can be adapted):** Lab02-03 (Dummy, NB variants, threshold and abstention, imbalance), Lab04 (ColumnTransformer + Pipeline, scaler comparison, MAE/RMSE/R², residual plots, leakage example), Lab05 (ID3, Gini/entropy, ccp_alpha, RF/ET/AdaBoost/GB/HGB, permutation importance, calibration), Lab06 (SVM, GridSearch), Lab07 (voting, bagging, OOB, correlation formula, staged boosting, comparison on the same folds), Lab08 (NumPy MLP).
- If the user's own course materials (slide PDFs, lab notebooks) are not in this repo and are needed, Claude may ask the user to put them in a `course_materials/` folder.
