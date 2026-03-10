import streamlit as st

from core.assumptions import load_assumptions
from core.lever_catalog import load_lever_catalog

st.title("Admin / Assumptions")
st.info("Edit assumptions and lever catalog files externally, then reload app.")
st.json(load_assumptions("data/assumptions.yaml"))

catalog = load_lever_catalog()
st.write(f"Loaded levers: {len(catalog)}")
st.dataframe([
    {
        "lever_id": l.lever_id,
        "name": l.name,
        "category": l.category,
        "effort": l.implementation_effort,
        "risk": l.risk_level,
        "confidence": l.confidence_level,
    }
    for l in catalog
])
