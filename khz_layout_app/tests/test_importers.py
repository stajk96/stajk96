import pandas as pd

from importers.mapper import map_to_canonical


def test_mapper():
    df = pd.DataFrame({"a": [1], "b": [2]})
    out = map_to_canonical(df, {"x": "a"})
    assert "x" in out.columns
