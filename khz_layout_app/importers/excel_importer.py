from __future__ import annotations

import pandas as pd


def load_excel(file, sheet_name: str | int = 0) -> pd.DataFrame:
    return pd.read_excel(file, sheet_name=sheet_name)
