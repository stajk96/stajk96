from __future__ import annotations

import streamlit as st

from components.lever_inputs import render_parameter_input
from core.models import EnhancedLayoutLever


BADGE_COLORS = {
    "low": "#2e7d32",
    "medium": "#ef6c00",
    "high": "#c62828",
}


def _badge(text: str, level: str):
    color = BADGE_COLORS.get(level.lower(), "#455a64")
    st.markdown(f"<span style='background:{color};padding:2px 8px;border-radius:10px;color:white;font-size:12px'>{text}: {level}</span>", unsafe_allow_html=True)


def render_lever_card(lever: EnhancedLayoutLever, values: dict) -> dict:
    with st.container(border=True):
        st.subheader(lever.name)
        st.caption(lever.description)
        c1, c2, c3 = st.columns(3)
        with c1:
            _badge("Effort", lever.implementation_effort)
        with c2:
            _badge("Confidence", lever.confidence_level)
        with c3:
            _badge("Risk", lever.risk_level)

        st.markdown(f"**Business intent:** {lever.business_question}")
        st.markdown(f"**Mechanism:** {lever.operational_mechanism}")

        out = dict(values)
        for p in lever.input_parameters:
            out[p.name] = render_parameter_input(p, key=f"{lever.lever_id}_{p.name}")

        ac1, ac2 = st.columns(2)
        ac1.markdown("**Affects**")
        ac1.write(", ".join(lever.affected_intermediate_variables[:8]) or "n/a")
        ac2.markdown("**Watch-outs**")
        ac2.write("; ".join(lever.watchouts[:3]) or "n/a")

        with st.expander("Why this move?"):
            st.markdown(f"**Typical situations:** {'; '.join(lever.typical_use_cases) if lever.typical_use_cases else 'n/a'}")
            st.markdown(f"**When not to use:** {'; '.join(lever.avoid_when) if lever.avoid_when else 'n/a'}")
            st.markdown(f"**Implementation caution:** {lever.recommendation_template}")

        active = any(v != p.default for p, v in zip(lever.input_parameters, [out[p.name] for p in lever.input_parameters]))
        st.info("Active change" if active else "At baseline defaults")

    return out
