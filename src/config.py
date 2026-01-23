from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    # `.../pyspark-simple-learning/src/config.py` -> root is parent of `src`
    return Path(__file__).resolve().parents[1]


ROOT = project_root()
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
OUTPUT_DIR = DATA_DIR / "output"

