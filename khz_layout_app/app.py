import streamlit as st

from utils.session_state import init_state

st.set_page_config(page_title="KHZ Layout Utilization Calculator & Scenario Simulator", layout="wide")
init_state()

st.title("KHZ Layout Utilization Calculator & Scenario Simulator")
st.info("This app is a layout-focused decision-support simulator based on warehouse-science principles and explicit rules. It is designed for structured comparison of layout scenarios, not as a statistically calibrated digital twin.")
st.write("Use the left sidebar pages for Site Setup, Import Wizard, Scenario building, and comparison.")
