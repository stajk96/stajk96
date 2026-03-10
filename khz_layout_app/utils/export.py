from __future__ import annotations

import io
import json

import pandas as pd


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def to_json_bytes(payload: dict) -> bytes:
    return json.dumps(payload, indent=2).encode("utf-8")


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name="export")
    return buf.getvalue()
