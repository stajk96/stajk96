import pandas as pd
import streamlit as st

from components.kpi_cards import render_kpi_cards
from components.radar_chart import render_radar
from components.scenario_tables import render_comparison_table
from components.waterfall_chart import render_waterfall
from core.engine import simulate
from core.models import BaselineOperationalInputs, LayoutGeometry, Scenario, SiteProfile
from utils.session_state import init_state

init_state()
st.title("Scenario Compare")
levers = pd.read_csv("data/lever_catalog.csv").to_dict("records")
site = st.session_state.site or SiteProfile()
geometry = st.session_state.geometry or LayoutGeometry()
ops = st.session_state.operational or BaselineOperationalInputs()
base = Scenario(name="baseline", site=site, geometry=geometry, operational=ops, lever_values={})
whatif = Scenario(name="scenario_1", site=site, geometry=geometry, operational=ops, lever_values=st.session_state.lever_values)
r0 = simulate(base, levers)
r1 = simulate(whatif, levers)
st.session_state.results = {"baseline": r0.model_dump(), "scenario_1": r1.model_dump()}
render_kpi_cards(r1.kpis.values)
render_comparison_table(r0.kpis.values, r1.kpis.values)
render_radar(r1.bottlenecks.values)
render_waterfall(r1.drivers)
