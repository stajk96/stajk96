import streamlit as st

from components.lever_card import render_lever_card
from core.audit import log_change
from core.lever_catalog import lever_default_inputs, lever_intensity, load_lever_catalog
from core.recommendations import recommend_from_kpis
from utils.session_state import init_state

init_state()
st.title("Layout Levers")
st.caption("Professional decision cards: action -> parameters -> intermediate variables -> KPI effects")

catalog = load_lever_catalog()

for lever in catalog:
    old = st.session_state.lever_values.get(lever.lever_id, lever_default_inputs(lever))
    new = render_lever_card(lever, old)
    st.session_state.lever_values[lever.lever_id] = new

    old_i = lever_intensity(lever, old)
    new_i = lever_intensity(lever, new)
    if abs(new_i - old_i) > 1e-9:
        st.session_state.change_log.append(log_change(
            site=st.session_state.site.site_name if st.session_state.site else "unknown",
            scenario="working",
            lever_id=lever.lever_id,
            lever_label=lever.name,
            old=old_i,
            new=new_i,
            reason="User lever parameter update",
            impacted_vars=lever.affected_intermediate_variables,
            impacted_bottlenecks=[lever.category],
            impacted_kpis=lever.affected_kpis,
        ))

# Sidebar decision summary
active = []
for l in catalog:
    vals = st.session_state.lever_values.get(l.lever_id, lever_default_inputs(l))
    intensity = lever_intensity(l, vals)
    if intensity > 0.01:
        active.append((l.name, intensity, l.risk_level))

st.sidebar.subheader("Scenario Lever Summary")
st.sidebar.write(f"Active lever count: {len(active)}")
if active:
    top = sorted(active, key=lambda x: x[1], reverse=True)[0]
    st.sidebar.write(f"Most impactful lever: {top[0]} ({top[1]:.2f})")
    risk = "high" if any(r == "high" for _, _, r in active) else "medium" if any(r == "medium" for _, _, r in active) else "low"
    st.sidebar.write(f"Scenario risk level: {risk}")
    st.sidebar.write("Recommended follow-up: validate congestion and replenishment checks before rollout.")
else:
    st.sidebar.info("No active lever changes")

if st.session_state.get("results") and st.session_state.results.get("scenario_1"):
    kpis = st.session_state.results["scenario_1"]["kpis"]["values"]
    recs = recommend_from_kpis(kpis)
    st.sidebar.write(f"Biggest positive KPI: {min((k for k in kpis if 'distance' in k or 'risk' in k), key=lambda x: kpis[x], default='n/a')}")
    st.sidebar.write(f"Biggest side effect: {max((k for k in kpis if 'risk' in k or 'burden' in k), key=lambda x: kpis[x], default='n/a')}")
    st.sidebar.write(f"Next action: {recs[0].action}")
