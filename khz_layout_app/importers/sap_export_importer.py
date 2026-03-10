from __future__ import annotations

import pandas as pd


def load_sap_export(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    return df.rename(columns={"material": "sku_material", "movement_cnt": "movement_count"})
