import streamlit as st

from core.validators import validate_inputs
from components.validation_panels import render_issues
from utils.session_state import init_state

init_state()
st.title("Baseline Review")
st.write("Normalized baseline data")
if st.session_state.site:
    st.json(st.session_state.site.model_dump())
if st.session_state.geometry:
    st.json(st.session_state.geometry.model_dump())
if st.session_state.operational:
    st.json(st.session_state.operational.model_dump())
if st.session_state.geometry and st.session_state.operational:
    issues = validate_inputs(st.session_state.geometry, st.session_state.operational)
    render_issues(issues)
