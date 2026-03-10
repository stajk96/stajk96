from __future__ import annotations

import streamlit as st


def init_state():
    defaults = {
        "site": None,
        "geometry": None,
        "operational": None,
        "lever_values": {},
        "results": {},
        "change_log": [],
        "import_df": None,
        "import_mapping": {},
        "khz_parse_result": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
