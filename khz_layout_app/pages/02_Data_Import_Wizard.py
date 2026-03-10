import json

import pandas as pd
import streamlit as st

from importers.csv_importer import load_csv
from importers.excel_importer import load_excel
from importers.mapper import map_to_canonical
from importers.sap_export_importer import load_sap_export
from utils.io import write_json
from utils.session_state import init_state

init_state()
st.title("Data Import Wizard")
up = st.file_uploader("Upload Excel/CSV/SAP export", type=["csv", "xlsx"])
if up is not None:
    if up.name.endswith(".xlsx"):
        xls = pd.ExcelFile(up)
        sh = st.selectbox("sheet selection", xls.sheet_names)
        df = load_excel(up, sheet_name=sh)
    elif "sap" in up.name.lower():
        df = load_sap_export(up)
    else:
        df = load_csv(up)
    st.session_state.import_df = df
    st.dataframe(df.head(20))

if st.session_state.import_df is not None:
    st.subheader("column mapping")
    canonical = ["aisle", "row", "bay", "level", "bin/location", "zone", "dock/staging area", "sku/material", "pick frequency", "movement count", "temperature class", "area type"]
    mapping = {}
    for c in canonical:
        mapping[c] = st.selectbox(c, ["<none>"] + list(st.session_state.import_df.columns), key=f"map_{c}")
    cleaned = {k: v for k, v in mapping.items() if v != "<none>"}
    if st.button("preview mapped"):
        mapped = map_to_canonical(st.session_state.import_df, cleaned)
        st.dataframe(mapped.head(20))
        missing = [c for c in canonical if c not in cleaned]
        if missing:
            st.warning(f"missing fields: {missing}")
        st.session_state.import_mapping = cleaned
    name = st.text_input("mapping profile name", "default_profile")
    if st.button("save mapping profile"):
        write_json(f"data/{name}.json", {"name": name, "mappings": st.session_state.import_mapping})
        st.success("saved")
