import streamlit as st


def render_issues(issues):
    for i in issues:
        if i.severity == "error":
            st.error(f"{i.field}: {i.message}")
        else:
            st.warning(f"{i.field}: {i.message}")
