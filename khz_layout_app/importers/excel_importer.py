from __future__ import annotations

import pandas as pd


def list_excel_sheets(file) -> list[str]:
    xls = pd.ExcelFile(file)
    return xls.sheet_names


def load_excel(file, sheet_name: str | int = 0, header: int | None = 0) -> pd.DataFrame:
    return pd.read_excel(file, sheet_name=sheet_name, header=header)


def load_excel_raw(file, sheet_name: str | int = 0) -> pd.DataFrame:
    """Read sheet without assuming the first row is the header."""
    return pd.read_excel(file, sheet_name=sheet_name, header=None)
