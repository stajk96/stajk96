import streamlit as st

from components.explanation_panels import render_explanations
from core.explanations import explain_metric
from utils.session_state import init_state

init_state()
st.title("Explanation Center")
st.caption("What changed, why by that amount, side-effects, and what to do next.")

if "baseline" in st.session_state.results and "scenario_1" in st.session_state.results:
    b = st.session_state.results["baseline"]["kpis"]["values"]
    s = st.session_state.results["scenario_1"]["kpis"]["values"]
    deltas = {k: s[k] - b[k] for k in s.keys()}
    top_drivers = sorted(deltas.items(), key=lambda x: abs(x[1]), reverse=True)

    blocks = []
    for k in s.keys():
        drivers = [x[0] for x in top_drivers[:3]]
        secondary = [x[0] for x in top_drivers[3:6]]
        blocks.append(explain_metric(k, b[k], s[k], drivers, secondary))

    render_explanations(blocks)
else:
    st.info("Run Scenario Compare first.")
