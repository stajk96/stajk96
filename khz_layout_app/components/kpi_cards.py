from __future__ import annotations

import streamlit as st


def render_kpi_cards(kpis: dict[str, float]):
    cols = st.columns(4)
    for i, (k, v) in enumerate(kpis.items()):
        cols[i % 4].metric(k.replace("_", " ").title(), f"{v:.2f}")
