from __future__ import annotations

import pandas as pd


def load_csv(file) -> pd.DataFrame:
    return pd.read_csv(file)
