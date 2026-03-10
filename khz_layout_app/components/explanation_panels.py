import streamlit as st


def render_explanations(blocks):
    for b in blocks:
        with st.container(border=True):
            st.subheader(b.metric_name.replace("_", " ").title())
            st.write(b.interpretation_text)
            c1, c2 = st.columns(2)
            c1.caption(f"Implication: {b.management_implication}")
            c2.caption(f"Next action: {b.recommendation_text}")
            st.warning(b.caution_note)
