from __future__ import annotations

import streamlit as st


def render_lever_input(lever: dict, key: str, default: float) -> float:
    t = lever["input_type"]
    if t == "toggle":
        return 1.0 if st.checkbox(lever["label"], value=default > 0.5, key=key) else 0.0
    if t == "selectbox":
        options = [lever["min"], lever["default"], lever["max"]]
        return float(st.selectbox(lever["label"], options=options, index=1, key=key))
    if t == "number_input":
        return float(st.number_input(lever["label"], min_value=float(lever["min"]), max_value=float(lever["max"]), value=float(default), step=float(lever["step"]), key=key))
    return float(st.slider(lever["label"], min_value=float(lever["min"]), max_value=float(lever["max"]), value=float(default), step=float(lever["step"]), key=key))
