# KHZ Layout Utilization Calculator & Scenario Simulator

“This app is a layout-focused decision-support simulator based on warehouse-science principles and explicit rules. It is designed for structured comparison of layout scenarios, not as a statistically calibrated digital twin.”

## What changed in this upgrade
The lever system is now a professional decision engine:
- Levers are **operational actions** (not KPI sliders)
- Each lever has **parameterized inputs** (numeric, slider, toggle, selectbox)
- Engine chain is explicit: **Action -> Intermediate Variables -> Bottlenecks -> KPIs -> Explanations -> Recommendations**
- Every lever models **upside + drag/tradeoff**
- Layout Levers page now uses **professional decision cards** and a scenario summary sidebar

## Core architecture
1. Canonical data model (`core/models.py`)
2. Lever knowledge base (`data/layout_lever_catalog.yaml`)
3. Rule-based simulation (`core/engine.py` + `core/dependencies.py`)
4. Explanation and recommendation engines (`core/explanations.py`, `core/recommendations.py`)
5. Streamlit pages and reusable components (`pages/`, `components/`)

## KHZ structured workbook import (new)
The Import Wizard now supports a first-class **KHZ structured site template** path, separate from generic flat data imports.

### Supported structured sheet types
- `01_SITE_PROFILE` (recognized)
- `02_PICKING` (recognized)
- `03_LAYOUT` (**semantically parsed with header detection**)
- `04_DOCK` (recognized)
- `05_SCENARIOS` (recognized)

### How KHZ mode works
1. Workbook type selection in Import Wizard.
2. Auto-detect helper checks known KHZ sheet names.
3. Header detection scans first 20–30 rows and scores likely header row using semantic tokens.
4. Semantic column normalization maps synonym columns (e.g., `Observed value`, `Current value`) to canonical names.
5. Parsed observations are mapped conservatively to canonical intermediate variables.
6. Unmapped metrics remain visible for manual review (never silently dropped).

### KHZ mode vs Generic mode
- **KHZ mode**: template-aware parser for structured assessment sheets and semantic fields.
- **Generic/SAP/WMS mode**: raw tabular mapper for transactional exports.

## Lever catalog
The new catalog includes **53 realistic layout interventions** across:
- Aisle / geometry
- Slotting / SKU location
- Forward-pick / fast-pick
- Dock / staging
- Congestion / interference
- Flow segregation

Each lever stores:
- business intent
- operational mechanism
- parameter definitions
- primary impacts
- secondary impacts
- effort/confidence/risk badges
- watch-outs and “why this move?” guidance

## Formula and simulation logic
- Levers update intermediate variables first (travel, congestion, slotting, staging, flow separation, etc.)
- KPI changes are computed from those intermediates, not directly edited
- Dependency penalties model tradeoffs (e.g., forward-pick expansion without isolation increases replenishment/congestion drag)
- KPI caps/floors prevent fake precision and impossible outputs

## Run
```bash
cd khz_layout_app
pip install -r requirements.txt
python run_streamlit.py
```

or

```bash
cd khz_layout_app
streamlit run app.py
```

## Tests
```bash
cd khz_layout_app
pytest -q
```

## Troubleshooting: `invalid decimal literal`
If `SyntaxError: invalid decimal literal` appears with text like `git apply`, `diff --git`, or `new file mode 100644`, you are running a patch/diff as Python. Run `run_streamlit.py` (or `streamlit run app.py`) instead.
