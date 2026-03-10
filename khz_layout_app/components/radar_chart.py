import plotly.express as px
import pandas as pd
import streamlit as st


def render_radar(values: dict[str, float], title: str = "Bottleneck Radar"):
    df = pd.DataFrame({"family": list(values.keys()), "score": list(values.values())})
    fig = px.line_polar(df, r="score", theta="family", line_close=True, title=title)
    st.plotly_chart(fig, use_container_width=True)
