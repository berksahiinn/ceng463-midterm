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
