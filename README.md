# CENG 463 – Take-Home Midterm

Introduction to Machine Learning, IZTECH, Fall 2026–27.

All experiments are reproducible from this repository: fixed seed (`SEED = 463`), a single saved train/validation/test split, and the same 5-fold CV object shared by every model.

## Datasets
| Used in | Dataset | Source | File |
|---|---|---|---|
| Q1, Q2, Q4, Q5 (classification) | IBM Telco Customer Churn (7,043 rows, target `Churn`) | Kaggle `blastchar/telco-customer-churn` | `data/telco_churn.csv` |
| Q3 (regression) | California Housing (20,640 rows, target `MedHouseVal`, unit 100,000 USD) | `sklearn.datasets.fetch_california_housing` | `data/california_housing.csv` |

Both CSV files are included in the repository. To re-download them, delete the files and run `python src/download_data.py` (requires internet; Telco uses `kagglehub`).

## Repository structure
```
├── data/                 raw CSV files
├── src/
│   ├── utils.py          seed, paths, loaders, split, CV, preprocessing, metrics, saving helpers
│   └── download_data.py  dataset download script
├── notebooks/            00 … 05, run in order
├── results/
│   ├── splits/           saved split indices (fixed; created once by notebook 00)
│   ├── tables/           all tables (.csv and .tex)
│   ├── figures/          all figures (.png)
│   ├── models/           saved models (.joblib, not tracked by git)
│   └── frozen_configs.json   configurations frozen before the final test (Q5e)
├── report/               LaTeX source (main.tex, references.bib) and compiled main.pdf
├── requirements.txt      pinned package versions
├── environment.txt       hardware / software summary
└── LLM_USAGE_LOG.md      record of LLM assistance (for the disclosure section)
```

## Setup (Windows, PowerShell)
```powershell
python -m venv .venv                 # Python 3.12
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
On macOS/Linux activate with `source .venv/bin/activate`.

In VS Code / Jupyter select the `.venv` interpreter as the notebook kernel.

## How to run
Run the notebooks **in order**, each with *Restart & Run All*:

| Notebook | Content |
|---|---|
| `00_setup_split.ipynb` | Creates and saves the 60/20/20 splits (skips if they already exist) |
| `01_Q1_data_leakage.ipynb` | Q1 – data audit, split comparison, preprocessing, leakage demo |
| `02_Q2_classification.ipynb` | Q2 – baseline, LR, NB, k-NN, error analysis |
| `03_Q3_regression.ipynb` | Q3 – regression, regularization, complexity curves |
| `04_Q4_trees_ensembles.ipynb` | Q4 – decision trees, bagging, boosting, importance |
| `05_Q5_robustness_selection.ipynb` | Q5 – robustness, bootstrap, model selection, final test |

All tables and figures are written to `results/tables/` and `results/figures/`.

**Test-set protocol:** the classification test set is used only once, in Q5e, after configurations are frozen in `results/frozen_configs.json`. The Q3 regression test set is used only once at the end of Q3.

## Report
```powershell
cd report
pdflatex main.tex; bibtex main; pdflatex main.tex; pdflatex main.tex
```
(or build with the LaTeX Workshop extension in VS Code). Figures and tables are read directly from `../results/`.

## Environment
See `environment.txt` (OS, CPU, RAM, Python and library versions).
