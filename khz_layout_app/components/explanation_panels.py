import streamlit as st


def render_explanations(blocks):
    for b in blocks:
        st.subheader(b.metric_name)
        st.write(b.interpretation_text)
        st.caption(f"Implication: {b.management_implication}")
        st.caption(f"Next: {b.recommendation_text}")
        st.warning(b.caution_note)
