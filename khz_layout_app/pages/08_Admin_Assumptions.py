import pandas as pd
import streamlit as st

from core.assumptions import load_assumptions

st.title("Admin / Assumptions")
st.info("Edit assumptions.yaml and lever_catalog.csv externally, then reload app.")
st.json(load_assumptions("data/assumptions.yaml"))
st.dataframe(pd.read_csv("data/lever_catalog.csv").head(20))
