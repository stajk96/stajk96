import streamlit as st

from utils.session_state import init_state

st.set_page_config(page_title="KHZ Layout Utilization Calculator & Scenario Simulator", layout="wide")
init_state()

st.markdown(
    """
    <style>
      .main h1, .main h2, .main h3 {letter-spacing:0.2px;}
      [data-testid='stMetricValue'] {font-size: 1.4rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("KHZ Layout Utilization Calculator & Scenario Simulator")
st.info("This app is a layout-focused decision-support simulator based on warehouse-science principles and explicit rules. It is designed for structured comparison of layout scenarios, not as a statistically calibrated digital twin.")

c1, c2, c3 = st.columns(3)
c1.metric("Decision scope", "Layout only")
c2.metric("Model type", "Rule-based")
c3.metric("Scenario mode", "Baseline + What-if")

st.write("Use the left sidebar pages for Site Setup, Import Wizard, Levers, Scenario Compare, Explanation, and Change Log.")
