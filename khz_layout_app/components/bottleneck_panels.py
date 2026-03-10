import streamlit as st


def render_bottlenecks(values: dict[str, float]):
    for k, v in values.items():
        st.progress(min(max(v / 150, 0.0), 1.0), text=f"{k}: {v:.1f}")
