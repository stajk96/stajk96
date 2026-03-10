from __future__ import annotations

import re

import pandas as pd


def normalize_column_token(name: str) -> str:
    n = str(name).strip().lower()
    n = re.sub(r"[^a-z0-9]+", "_", n)
    return re.sub(r"_+", "_", n).strip("_")


def map_to_canonical(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    out = pd.DataFrame()
    for canonical, src in mapping.items():
        if src in df.columns:
            out[canonical] = df[src]
    return out


def map_to_canonical_normalized(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    """Maps columns using normalized source names to avoid minor naming mismatches."""
    norm_cols = {normalize_column_token(c): c for c in df.columns}
    out = pd.DataFrame()
    for canonical, src in mapping.items():
        src_real = norm_cols.get(normalize_column_token(src))
        if src_real:
            out[canonical] = df[src_real]
    return out
