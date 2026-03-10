import pandas as pd
import streamlit as st

from importers.csv_importer import load_csv
from importers.excel_importer import list_excel_sheets, load_excel
from importers.khz_template_importer import detect_khz_template_by_sheets, load_khz_schema, parse_khz_template_workbook
from importers.mapper import map_to_canonical_normalized
from importers.sap_export_importer import load_sap_export
from utils.io import write_json
from utils.session_state import init_state

init_state()
st.title("Data Import Wizard")

mode = st.selectbox(
    "What type of file are you uploading?",
    [
        "KHZ structured site template",
        "SAP / WMS operational export",
        "Generic Excel / CSV",
        "Manual entry only",
    ],
)

if mode == "Manual entry only":
    st.info("Use Site Setup page for manual baseline creation.")
    st.stop()

up = st.file_uploader("Upload workbook or file", type=["csv", "xlsx"])
if up is None:
    st.stop()

schema = load_khz_schema()

if up.name.endswith(".xlsx"):
    sheets = list_excel_sheets(up)
    auto_khz = detect_khz_template_by_sheets(sheets, schema)
    if auto_khz and mode != "KHZ structured site template":
        st.info("Auto-detect suggestion: workbook looks like a KHZ structured template (sheet names match known KHZ pattern).")

if mode == "KHZ structured site template":
    if not up.name.endswith(".xlsx"):
        st.error("KHZ structured template mode expects an Excel workbook (.xlsx).")
        st.stop()

    result = parse_khz_template_workbook(up)
    st.session_state.khz_parse_result = result.model_dump()

    st.subheader("A. Workbook type")
    st.write({"selected_mode": mode, "detected_khz_template": result.detected, "confidence_score": result.confidence_score})

    st.subheader("B. Parsed sheets summary")
    st.write({
        "recognized_sheets": result.recognized_sheets,
        "unrecognized_sheets": result.unrecognized_sheets,
        "header_rows": {r.sheet_name: r.header_row for r in result.sheet_results},
    })

    st.subheader("C. Parsed layout metrics table")
    parsed_rows = []
    for sr in result.sheet_results:
        for o in sr.observations:
            parsed_rows.append(o.model_dump())
    parsed_df = pd.DataFrame(parsed_rows)
    if not parsed_df.empty:
        st.dataframe(parsed_df)
    else:
        st.warning("No layout observations parsed.")

    st.subheader("D. Auto-mapped baseline fields")
    st.json(result.mapped_baseline_fields)

    st.subheader("E. Unmapped observations")
    unmapped_df = pd.DataFrame([x.model_dump() for x in result.unmapped_observations])
    if not unmapped_df.empty:
        st.dataframe(unmapped_df)
        st.caption("Manual mapping option: export table and map fields in Generic mode if needed.")
    else:
        st.success("No unmapped observations.")

    st.subheader("F. Validation warnings")
    if result.validation_warnings:
        for w in result.validation_warnings:
            st.warning(w)
    else:
        st.success("No warnings.")

    if st.button("Apply mapped baseline to session"):
        if st.session_state.operational:
            for k, v in result.mapped_baseline_fields.items():
                if hasattr(st.session_state.operational, k):
                    setattr(st.session_state.operational, k, v)
            st.success("Applied mapped baseline fields to current operational profile.")
        else:
            st.warning("Create baseline first in Site Setup page.")

    if st.button("Save KHZ parse result JSON"):
        write_json("data/khz_last_parse_result.json", result.model_dump())
        st.success("Saved to data/khz_last_parse_result.json")

else:
    # Keep generic and SAP/WMS paths unchanged conceptually.
    if mode == "SAP / WMS operational export":
        if up.name.endswith(".xlsx"):
            sh = st.selectbox("sheet selection", list_excel_sheets(up))
            df = load_excel(up, sheet_name=sh)
        elif "sap" in up.name.lower():
            df = load_sap_export(up)
        else:
            df = load_csv(up)
    else:
        if up.name.endswith(".xlsx"):
            sh = st.selectbox("sheet selection", list_excel_sheets(up))
            df = load_excel(up, sheet_name=sh)
        else:
            df = load_csv(up)

    st.session_state.import_df = df
    st.dataframe(df.head(20))

    st.subheader("column mapping")
    canonical = [
        "aisle",
        "row",
        "bay",
        "level",
        "bin/location",
        "zone",
        "dock/staging area",
        "sku/material",
        "pick frequency",
        "movement count",
        "temperature class",
        "area type",
    ]
    mapping = {}
    for c in canonical:
        mapping[c] = st.selectbox(c, ["<none>"] + list(st.session_state.import_df.columns), key=f"map_{c}")
    cleaned = {k: v for k, v in mapping.items() if v != "<none>"}
    if st.button("preview mapped"):
        mapped = map_to_canonical_normalized(st.session_state.import_df, cleaned)
        st.dataframe(mapped.head(20))
        missing = [c for c in canonical if c not in cleaned]
        if missing:
            st.warning(f"missing fields: {missing}")
        st.session_state.import_mapping = cleaned
    name = st.text_input("mapping profile name", "default_profile")
    if st.button("save mapping profile"):
        write_json(f"data/{name}.json", {"name": name, "mappings": st.session_state.import_mapping})
        st.success("saved")
