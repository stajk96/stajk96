from __future__ import annotations

import streamlit as st


LOWER_IS_BETTER = ("risk", "distance", "time", "burden")


def _status(metric: str, value: float) -> str:
    lib = metric.lower()
    lower_better = any(k in lib for k in LOWER_IS_BETTER)
    if lower_better:
        return "good" if value < 100 else "mixed" if value < 105 else "caution"
    return "good" if value > 100 else "mixed" if value > 95 else "caution"


def render_kpi_cards(kpis: dict[str, float]):
    cols = st.columns(4)
    for i, (k, v) in enumerate(kpis.items()):
        s = _status(k, v)
        cols[i % 4].metric(k.replace("_", " ").title(), f"{v:.2f}", help=f"Status: {s}")
