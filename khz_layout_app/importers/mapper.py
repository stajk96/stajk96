from __future__ import annotations

import pandas as pd


def map_to_canonical(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    out = pd.DataFrame()
    for canonical, src in mapping.items():
        if src in df.columns:
            out[canonical] = df[src]
    return out
