# KHZ Layout Utilization Calculator & Scenario Simulator

“This app is a layout-focused decision-support simulator based on warehouse-science principles and explicit rules. It is designed for structured comparison of layout scenarios, not as a statistically calibrated digital twin.”

## Overview
Production-grade Python + Streamlit app for layout-only warehouse decision support across multiple FMCG archetypes and data maturity levels.

## Core architecture
1. Internal canonical data model (source of truth)
2. In-app Site Setup form (primary workflow)
3. Import Wizard (Excel/CSV/SAP-export secondary workflow)
4. Export layer (CSV/Excel/JSON ready; PDF-ready tables)

## Supported warehouse archetypes
- Dry FMCG pallet warehouse
- Dry pallet + case-pick warehouse
- Forward-pick / fast-pick warehouse
- Multi-temperature FMCG warehouse
- Partially automated warehouse
- Large automated dry-goods DC archetype

## Formula logic (indexed and explainable)
- Travel is driven by aisle geometry, cut-throughs, slotting, and dock adjacency.
- Slotting quality and zone balance increase pick density and labor index.
- Congestion and replenishment interference apply drag multipliers.
- Forward-pick expansion gives travel upside but may create replenishment downside.
- Dependency penalties apply explicit rule interactions.
- KPI values are capped/floored to avoid fake precision.

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tests
```bash
pytest -q
```

## Data import
Use **Data Import Wizard** page to upload CSV/XLSX, map columns to canonical schema, preview parsed rows, review missing fields, and save mapping profiles.

## Exports
- Scenario comparison CSV
- Scenario JSON
- Excel export from normalized tables

## Notes
- No Excel-core logic; all imports are mapped into canonical schema first.
- Rule-based transparent simulator, not black-box AI.


## Troubleshooting: `invalid decimal literal`
If you see an error like `SyntaxError: invalid decimal literal` and the line contains text such as `git apply`, `diff --git`, or `new file mode 100644`, you are running a **patch/diff** as Python code.

Use one of these correct launch methods instead:

```bash
cd khz_layout_app
python run_streamlit.py
```

or

```bash
cd khz_layout_app
streamlit run app.py
```

In Spyder, open and run `run_streamlit.py` (not pasted diff content).
