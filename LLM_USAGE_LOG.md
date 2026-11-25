# LLM Usage Log

Tool: Claude Code (Anthropic, model Claude Opus 5.5), VS Code extension.
Permitted scope (per exam rules): code writing, debugging, environment setup only.

| Date | Task | What the LLM did |
|---|---|---|
| 2026-11-25 | Project setup | Created folder structure, CLAUDE.md, .gitignore, LLM usage log; set up Python virtual environment and installed packages. |
| 2026-11-25 | Environment | Created Python 3.12 venv, installed numpy/pandas/scikit-learn/imbalanced-learn/matplotlib/seaborn/jupyter; registered Jupyter kernel; generated requirements.txt (pip freeze) and environment.txt. |
| 2026-11-25 | Data download | Wrote src/download_data.py (Telco via kagglehub, California Housing via sklearn) and ran it. |
| 2026-11-25 | Tooling | Installed GitHub CLI and MiKTeX (local LaTeX), LaTeX Workshop VS Code extension; wrote .vscode/settings.json (venv interpreter, pdflatex recipe). |
| 2026-11-25 | Project rules | Translated CLAUDE.md to English; added a rule that Claude only shows commands (does not run, install or download anything) and asks before writing code. |
| 2026-11-25 | Shared utilities | Wrote src/utils.py: SEED=463, paths, Telco/California loaders, saved 60/20/20 split (make_split/load_split), shared 5-fold CV object, preprocessing ColumnTransformer, metric helpers, table/figure saving, timer. Design choice confirmed by the user: SeniorCitizen treated as categorical. |
| 2026-11-25 | Split notebook | Wrote notebooks/00_setup_split.ipynb: creates (once) and saves the 60/20/20 splits for Telco (stratified) and California (random), integrity asserts, exact split-size tables. Run by the user. |
| 2026-11-25 | README and report skeleton | Wrote README.md (setup, run order, test-set protocol) and report/main.tex skeleton with the 9 mandatory section headings, table/figure inclusion helpers and reproducibility appendix; report/references.bib with dataset and library references. Section contents are left for the user. |
| 2026-11-25 | Debugging (LaTeX) | Diagnosed `pdflatex ENOENT` in LaTeX Workshop (VS Code started before MiKTeX was on PATH); fixed bibtex lowercase "IBM" and listings spacing. |
| 2026-11-25 | Q1a code | Wrote notebooks/01_Q1_data_leakage.ipynb (Q1a section): feature types, class distribution, missing/blank values, duplicates with/without customerID (label conflicts, groups across splits), numeric ranges, TotalCharges vs tenure×MonthlyCharges, rare and dependent category levels, churn rate by feature on TRAIN only; saves tables/figures. Interpretation left to the user. |
| 2026-11-25 | Q1b code | Added Q1b cells: exact split sizes; stratified vs random 60/20/20 over 200 seeds (mean/std/max deviation of churn rate, share > 1 pp, boxplot); deviation vs dataset size (n = 100 … 7043); class ratio inside StratifiedKFold vs KFold folds (full train and n = 30 subsample). Interpretation left to the user. |
| 2026-11-25 | Study aids | Created REPORT_TODO.md (list of interpretation questions, no answers) and CALISMA_NOTLARI.md (Turkish concept explanations for the student's own study; git-ignored, not submitted). |
| 2026-11-25 | Q1c code | Added Q1c cells: fitted ColumnTransformer and output features; evidence that imputer/scaler statistics equal TRAIN statistics; fate of missing TotalCharges and of an unseen category (synthetic row); scaling on/off with the same 5 CV folds for LR, k-NN, GaussianNB, DT, RF, AdaBoost, GB (incl. LR solver iterations); empirical preprocessing-requirements table (fit attempts on raw strings / NaN). Interpretation left to the user. |
