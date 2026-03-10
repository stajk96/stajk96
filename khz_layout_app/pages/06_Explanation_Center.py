import streamlit as st

from components.explanation_panels import render_explanations
from core.explanations import explain_metric
from utils.session_state import init_state

init_state()
st.title("Explanation Center")
if "baseline" in st.session_state.results and "scenario_1" in st.session_state.results:
    b = st.session_state.results["baseline"]["kpis"]["values"]
    s = st.session_state.results["scenario_1"]["kpis"]["values"]
    blocks = [
        explain_metric(k, b[k], s[k], ["slotting quality", "flow separation", "dock adjacency"], ["congestion drag", "replenishment burden", "zone balance"])
        for k in s.keys()
    ]
    render_explanations(blocks)
else:
    st.info("Run scenario compare first.")
