"""Shared utilities for the CENG 463 take-home midterm.

Every notebook starts with:

    import sys; sys.path.insert(0, "..")      # when running from notebooks/
    from src.utils import *
    set_seed()

Everything that must be identical across questions lives here:
seed, paths, data loading, the saved train/val/test split, the CV object,
the preprocessing ColumnTransformer and metric definitions.
"""
from __future__ import annotations

import random
import time
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    mean_absolute_error,
    r2_score,
    roc_auc_score,
    root_mean_squared_error,
)
from sklearn.model_selection import KFold, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ---------------------------------------------------------------------------
# Seed
# ---------------------------------------------------------------------------
SEED = 463


def set_seed(seed: int = SEED) -> None:
    """Fix Python and NumPy global RNGs. sklearn objects get random_state=SEED explicitly."""
    random.seed(seed)
    np.random.seed(seed)


# ---------------------------------------------------------------------------
# Paths (resolved from this file, so they work from any working directory)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"
SPLITS_DIR = RESULTS_DIR / "splits"
TABLES_DIR = RESULTS_DIR / "tables"
FIGURES_DIR = RESULTS_DIR / "figures"
MODELS_DIR = RESULTS_DIR / "models"

for _d in (SPLITS_DIR, TABLES_DIR, FIGURES_DIR, MODELS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

CLF_SPLIT_FILE = SPLITS_DIR / "clf_split_indices.csv"
REG_SPLIT_FILE = SPLITS_DIR / "reg_split_indices.csv"

# ---------------------------------------------------------------------------
# Telco Customer Churn (classification: Q1, Q2, Q4, Q5)
# ---------------------------------------------------------------------------
TELCO_TARGET = "Churn"
TELCO_ID = "customerID"
NUM_COLS = ["tenure", "MonthlyCharges", "TotalCharges"]
# SeniorCitizen is stored as 0/1 but is semantically a yes/no category,
# so it is treated as categorical (consistent with Partner, Dependents, ...).
CAT_COLS = [
    "gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService",
    "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaperlessBilling", "PaymentMethod",
]


def load_telco_raw() -> pd.DataFrame:
    """Raw Telco data exactly as in the CSV (for the Q1a audit)."""
    return pd.read_csv(DATA_DIR / "telco_churn.csv")


def load_telco() -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Return (X, y, ids).

    - TotalCharges: string -> float; blank strings become NaN (imputed later
      inside the pipeline, never here).
    - SeniorCitizen: 0/1 -> "No"/"Yes" so it is handled as a category.
    - y: Churn Yes/No -> 1/0.
    - customerID is returned separately and is NOT a feature.
    """
    df = load_telco_raw()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["SeniorCitizen"] = df["SeniorCitizen"].map({0: "No", 1: "Yes"})
    y = (df[TELCO_TARGET] == "Yes").astype(int).rename(TELCO_TARGET)
    ids = df[TELCO_ID]
    X = df[NUM_COLS + CAT_COLS]
    return X, y, ids


# ---------------------------------------------------------------------------
# California Housing (regression: Q3)
# ---------------------------------------------------------------------------
HOUSING_TARGET = "MedHouseVal"  # unit: 100,000 USD, capped at 5.0


def load_housing() -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(DATA_DIR / "california_housing.csv")
    return df.drop(columns=HOUSING_TARGET), df[HOUSING_TARGET]


# ---------------------------------------------------------------------------
# Train / validation / test split (60 / 20 / 20), made once and saved
# ---------------------------------------------------------------------------
def make_split(
    y: pd.Series,
    path: Path,
    stratify: bool = True,
    ids: pd.Series | None = None,
    overwrite: bool = False,
) -> pd.DataFrame:
    """Split row positions into train/val/test (60/20/20) and save to CSV.

    Test (20%) is separated first; the remaining 80% is split 75/25 into
    train/val, giving 60/20/20 of the full data. Refuses to overwrite an
    existing split unless overwrite=True, so the split cannot change silently.
    """
    path = Path(path)
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} already exists; use load_split() or overwrite=True.")

    idx = np.arange(len(y))
    strat = y.to_numpy() if stratify else None
    idx_trval, idx_test = train_test_split(
        idx, test_size=0.20, stratify=strat, random_state=SEED
    )
    strat_trval = y.to_numpy()[idx_trval] if stratify else None
    idx_train, idx_val = train_test_split(
        idx_trval, test_size=0.25, stratify=strat_trval, random_state=SEED
    )

    split = pd.Series("", index=idx, name="split")
    split.iloc[idx_train] = "train"
    split.iloc[idx_val] = "val"
    split.iloc[idx_test] = "test"

    out = pd.DataFrame({"row": idx, "split": split.to_numpy()})
    if ids is not None:
        out.insert(1, "id", ids.to_numpy())
    out.to_csv(path, index=False)
    return out


def load_split(X: pd.DataFrame, y: pd.Series, path: Path, ids: pd.Series | None = None) -> dict:
    """Read a saved split and return a dict with X_train, X_val, X_test, y_train, y_val, y_test.

    If ids were saved, they are checked against the current data so a changed
    CSV cannot be silently paired with an old split.
    """
    s = pd.read_csv(path)
    if len(s) != len(y):
        raise ValueError(f"Split has {len(s)} rows but data has {len(y)}.")
    if ids is not None and "id" in s.columns and not (s["id"].to_numpy() == ids.to_numpy()).all():
        raise ValueError("IDs in split file do not match the data.")

    out = {}
    for part in ("train", "val", "test"):
        rows = s.loc[s["split"] == part, "row"].to_numpy()
        out[f"X_{part}"] = X.iloc[rows]
        out[f"y_{part}"] = y.iloc[rows]
    return out


def split_size_table(parts: dict) -> pd.DataFrame:
    """Exact split sizes and positive rate (classification) / target mean (regression)."""
    rows = []
    n_total = sum(len(parts[f"y_{p}"]) for p in ("train", "val", "test"))
    for p in ("train", "val", "test"):
        yy = parts[f"y_{p}"]
        rows.append({"split": p, "n": len(yy), "fraction": len(yy) / n_total, "target_mean": yy.mean()})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Cross-validation: ONE definition, shared by all models
# ---------------------------------------------------------------------------
def get_cv(kind: str = "clf", n_splits: int = 5):
    """5-fold CV with fixed seed. 'clf' -> StratifiedKFold, 'reg' -> KFold."""
    if kind == "clf":
        return StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=SEED)
    if kind == "reg":
        return KFold(n_splits=n_splits, shuffle=True, random_state=SEED)
    raise ValueError("kind must be 'clf' or 'reg'")


# ---------------------------------------------------------------------------
# Preprocessing (always used inside a Pipeline -> fitted only on training folds)
# ---------------------------------------------------------------------------
def build_preprocessor(
    num_cols: list[str] = NUM_COLS,
    cat_cols: list[str] = CAT_COLS,
    scale: bool = True,
) -> ColumnTransformer:
    """Numeric: median imputation (+ StandardScaler if scale=True).
    Categorical: most-frequent imputation + one-hot (unknown categories ignored).

    scale=False is meant for tree-based models, which are invariant to monotone
    rescaling of features.
    """
    num_steps = [("impute", SimpleImputer(strategy="median"))]
    if scale:
        num_steps.append(("scale", StandardScaler()))
    cat_steps = [
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ]
    transformers = [("num", Pipeline(num_steps), num_cols)]
    if cat_cols:
        transformers.append(("cat", Pipeline(cat_steps), cat_cols))
    return ColumnTransformer(transformers, remainder="drop")


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------
def clf_metrics(y_true, y_pred, y_score=None) -> dict:
    """Accuracy, Macro-F1, churn (positive class) F1; ROC-AUC and PR-AUC if scores given."""
    m = {
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(y_true, y_pred, average="macro"),
        "f1_pos": f1_score(y_true, y_pred, pos_label=1),
    }
    if y_score is not None:
        m["roc_auc"] = roc_auc_score(y_true, y_score)
        m["pr_auc"] = average_precision_score(y_true, y_score)
    return m


def reg_metrics(y_true, y_pred) -> dict:
    """MAE, RMSE, R2 (California target unit: 100,000 USD)."""
    return {
        "mae": mean_absolute_error(y_true, y_pred),
        "rmse": root_mean_squared_error(y_true, y_pred),
        "r2": r2_score(y_true, y_pred),
    }


# ---------------------------------------------------------------------------
# Saving tables and figures
# ---------------------------------------------------------------------------
def save_table(df: pd.DataFrame, name: str, index: bool = False, float_format: str = "%.4f") -> Path:
    """Save as results/tables/<name>.csv and <name>.tex (for \\input in the report)."""
    csv_path = TABLES_DIR / f"{name}.csv"
    df.to_csv(csv_path, index=index)
    (TABLES_DIR / f"{name}.tex").write_text(
        df.to_latex(index=index, float_format=float_format.__mod__, escape=True),
        encoding="utf-8",
    )
    return csv_path


def save_fig(fig, name: str, dpi: int = 200) -> Path:
    """Save as results/figures/<name>.png."""
    path = FIGURES_DIR / f"{name}.png"
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return path


# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------
@contextmanager
def timer(label: str = "", verbose: bool = True):
    """Usage:
        with timer("fit RF") as t:
            model.fit(X, y)
        t["seconds"]
    """
    t = {"seconds": None}
    start = time.perf_counter()
    try:
        yield t
    finally:
        t["seconds"] = time.perf_counter() - start
        if verbose:
            print(f"[timer] {label}: {t['seconds']:.3f} s")
