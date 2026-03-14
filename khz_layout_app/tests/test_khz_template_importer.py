import pandas as pd

from importers.khz_template_importer import (
    detect_header_row,
    detect_khz_template_by_sheets,
    load_khz_schema,
    map_layout_observations_to_canonical,
    normalize_semantic_columns,
    parse_layout_sheet,
)


def test_detect_khz_template_by_sheets():
    schema = load_khz_schema("data/khz_template_schema.yaml")
    assert detect_khz_template_by_sheets(["01_SITE_PROFILE", "03_LAYOUT"], schema) is True
    assert detect_khz_template_by_sheets(["Sheet1", "Data"], schema) is False


def test_header_row_detection_for_layout_sheet():
    raw = pd.DataFrame(
        [
            ["KHZ Layout Assessment", None, None],
            [None, None, None],
            ["Category", "Metric code", "Observed value"],
            ["Travel", "TRV_01", 88],
        ]
    )
    row, confidence, candidates = detect_header_row(raw, ["category", "metric", "observed value"])
    assert row == 2
    assert confidence > 0.5
    assert 2 in candidates


def test_semantic_column_normalization():
    schema = load_khz_schema("data/khz_template_schema.yaml")
    mapping = normalize_semantic_columns(["Observed value", "Root cause / comments", "Required?"], schema)
    assert mapping["Observed value"] == "observed_value"
    assert mapping["Root cause / comments"] == "comments"
    assert mapping["Required?"] == "required_flag"


def test_parse_03_layout_sheet():
    schema = load_khz_schema("data/khz_template_schema.yaml")
    raw = pd.DataFrame(
        [
            ["title", None, None, None],
            ["Category", "Metric code", "Observed value", "Score"],
            ["Congestion", "CG_01", 75, 80],
            ["Travel", "TRV_01", 65, 78],
        ]
    )
    result = parse_layout_sheet(raw, "03_LAYOUT", schema)
    assert result.recognized is True
    assert result.header_row == 1
    assert len(result.observations) == 2


def test_map_layout_observations_to_canonical():
    schema = load_khz_schema("data/khz_template_schema.yaml")
    raw = pd.DataFrame(
        [
            ["Category", "Metric code", "Metric name", "Observed value", "Score"],
            ["Congestion", "CG_01", "Waves per aisle", 0.9, 90],
        ]
    )
    parsed = parse_layout_sheet(raw, "03_LAYOUT", schema)
    mapped, unmapped = map_layout_observations_to_canonical(parsed.observations, schema)
    assert "congestion_index" in mapped
    assert len(unmapped) == 0


def test_fallback_generic_signal():
    schema = load_khz_schema("data/khz_template_schema.yaml")
    # This workbook should not trigger KHZ mode; UI should route to generic.
    assert detect_khz_template_by_sheets(["operations_export", "raw_data"], schema) is False
