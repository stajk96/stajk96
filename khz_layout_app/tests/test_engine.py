import pandas as pd

from core.engine import simulate
from core.models import BaselineOperationalInputs, LayoutGeometry, Scenario, SiteProfile


def test_engine_no_impossible_values():
    levers = pd.read_csv("data/lever_catalog.csv").to_dict("records")
    s = Scenario(name="x", site=SiteProfile(), geometry=LayoutGeometry(), operational=BaselineOperationalInputs(), lever_values={})
    r = simulate(s, levers)
    for v in r.kpis.values.values():
        assert 0 <= v <= 200

def test_scenario_compare_consistency():
    levers = pd.read_csv("data/lever_catalog.csv").to_dict("records")
    s = Scenario(name="x", site=SiteProfile(), geometry=LayoutGeometry(), operational=BaselineOperationalInputs(), lever_values={"improve_abc_slotting":0.4})
    r1 = simulate(s, levers)
    r2 = simulate(s, levers)
    assert r1.kpis.values == r2.kpis.values
