import pandas as pd
import streamlit as st

from components.lever_inputs import render_lever_input
from core.audit import log_change
from utils.session_state import init_state

init_state()
st.title("Layout Levers")
levers = pd.read_csv("data/lever_catalog.csv").to_dict("records")
for lv in levers:
    with st.expander(f"{lv['group']} | {lv['label']}"):
        st.caption(lv["description"])
        old = st.session_state.lever_values.get(lv["lever_id"], float(lv["default"]))
        val = render_lever_input(lv, f"lever_{lv['lever_id']}", old)
        st.session_state.lever_values[lv["lever_id"]] = val
        st.write("Likely upside/downside shown via impacts + dependencies")
        if val != old:
            st.session_state.change_log.append(log_change(
                site=st.session_state.site.site_name if st.session_state.site else "unknown",
                scenario="working",
                lever_id=lv["lever_id"],
                lever_label=lv["label"],
                old=old,
                new=val,
                reason="User adjustment",
                impacted_vars=["intermediate_indexes"],
                impacted_bottlenecks=["all"],
                impacted_kpis=["all"],
            ))
