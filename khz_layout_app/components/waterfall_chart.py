import plotly.graph_objects as go
import streamlit as st


def render_waterfall(drivers: dict[str, float], title: str = "Driver Contribution"):
    keys = list(drivers.keys())[:10]
    vals = [drivers[k] for k in keys]
    fig = go.Figure(go.Waterfall(x=keys, y=vals))
    fig.update_layout(title=title)
    st.plotly_chart(fig, use_container_width=True)
