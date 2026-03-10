import pandas as pd
import streamlit as st


def render_comparison_table(baseline: dict[str, float], scenario: dict[str, float]):
    df = pd.DataFrame({"baseline": baseline, "scenario": scenario})
    df["delta"] = df["scenario"] - df["baseline"]
    st.dataframe(df)
