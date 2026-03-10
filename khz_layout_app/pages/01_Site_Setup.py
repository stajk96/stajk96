import streamlit as st

from core.enums import AutomationLevel, TemperatureType, WarehouseArchetype
from core.models import BaselineOperationalInputs, LayoutGeometry, SiteProfile
from core.validators import validate_inputs
from components.validation_panels import render_issues
from utils.session_state import init_state

init_state()
st.title("Site Setup")

with st.form("site_form"):
    c1, c2, c3 = st.columns(3)
    site = SiteProfile(
        site_name=c1.text_input("site name", "Sample Site"),
        country=c1.text_input("country", "UK"),
        region=c1.text_input("region", "EMEA"),
        business_unit=c1.text_input("business unit", "Meals"),
        warehouse_archetype=WarehouseArchetype(c2.selectbox("warehouse archetype", [e.value for e in WarehouseArchetype])),
        temperature_type=TemperatureType(c2.selectbox("temperature type", [e.value for e in TemperatureType])),
        automation_level=AutomationLevel(c2.selectbox("automation level", [e.value for e in AutomationLevel])),
    )
    geom = LayoutGeometry(
        total_area=c3.number_input("total area", value=20000.0),
        usable_area=c3.number_input("usable area", value=16000.0),
        clear_height=c3.number_input("clear height", value=11.0),
        storage_rows=st.number_input("number of storage rows", value=30),
        row_length_m=st.number_input("row lengths", value=70.0),
        aisle_count=st.number_input("aisle count", value=28),
        aisle_width_m=st.number_input("aisle width", value=3.5),
        cross_aisle_count=st.number_input("cross-aisle count", value=3),
        cross_aisle_placement_quality=st.slider("cross-aisle placement quality", 0.0, 1.0, 0.6),
        lane_depth=st.number_input("lane depth", value=4),
        pallet_positions=st.number_input("pallet positions", value=15000),
        rack_share=st.slider("rack share", 0.0, 1.0, 0.7),
        floor_stack_share=st.slider("floor-stack share", 0.0, 1.0, 0.3),
        forward_pick_area=st.number_input("forward-pick area size", value=1800.0),
        reserve_area=st.number_input("reserve area size", value=9000.0),
        dock_door_count=st.number_input("dock door count", value=24),
        inbound_door_count=st.number_input("inbound door count", value=10),
        outbound_door_count=st.number_input("outbound door count", value=14),
        staging_area_size=st.number_input("staging area size", value=2200.0),
        staging_lane_count=st.number_input("staging lane count", value=26),
    )
    ops = BaselineOperationalInputs()
    if st.form_submit_button("save baseline"):
        st.session_state.site = site
        st.session_state.geometry = geom
        st.session_state.operational = ops
        render_issues(validate_inputs(geom, ops))
        st.success("Baseline saved")
