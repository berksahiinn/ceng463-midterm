"""Download raw datasets into data/.

Usage (from project root):
    python src/download_data.py

- Telco Customer Churn (IBM sample, Kaggle: blastchar/telco-customer-churn)
- California Housing (sklearn.datasets.fetch_california_housing)
"""
import shutil
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

TELCO_FILE = "WA_Fn-UseC_-Telco-Customer-Churn.csv"


def download_telco() -> Path:
    out = DATA / "telco_churn.csv"
    if out.exists():
        print(f"[skip] {out.name} already exists")
        return out
    import kagglehub

    src_dir = Path(kagglehub.dataset_download("blastchar/telco-customer-churn"))
    shutil.copy(src_dir / TELCO_FILE, out)
    print(f"[ok] Telco -> {out}")
    return out


def download_california() -> Path:
    out = DATA / "california_housing.csv"
    if out.exists():
        print(f"[skip] {out.name} already exists")
        return out
    from sklearn.datasets import fetch_california_housing

    ds = fetch_california_housing(as_frame=True, data_home=str(DATA / "sklearn_cache"))
    ds.frame.to_csv(out, index=False)
    print(f"[ok] California Housing -> {out}")
    return out


if __name__ == "__main__":
    for path in (download_telco(), download_california()):
        df = pd.read_csv(path)
        print(f"{path.name}: {df.shape[0]} rows x {df.shape[1]} cols")
