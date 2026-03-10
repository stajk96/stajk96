import pandas as pd

from importers.mapper import map_to_canonical, map_to_canonical_normalized


def test_mapper():
    df = pd.DataFrame({"a": [1], "b": [2]})
    out = map_to_canonical(df, {"x": "a"})
    assert "x" in out.columns


def test_mapper_normalized():
    df = pd.DataFrame({"Observed value": [7], "Metric Code": ["L-1"]})
    out = map_to_canonical_normalized(df, {"observed_value": "observed_value", "metric_code": "metric code"})
    assert "observed_value" in out.columns
    assert "metric_code" in out.columns
