from core.engine import simulate
from core.lever_catalog import load_lever_catalog
from core.models import BaselineOperationalInputs, LayoutGeometry, Scenario, SiteProfile


def test_engine_no_impossible_values():
    levers = load_lever_catalog("data/layout_lever_catalog.yaml")
    s = Scenario(name="x", site=SiteProfile(), geometry=LayoutGeometry(), operational=BaselineOperationalInputs(), lever_values={})
    r = simulate(s, levers)
    for v in r.kpis.values.values():
        assert 0 <= v <= 200


def test_scenario_compare_consistency():
    levers = load_lever_catalog("data/layout_lever_catalog.yaml")
    s = Scenario(
        name="x",
        site=SiteProfile(),
        geometry=LayoutGeometry(),
        operational=BaselineOperationalInputs(),
        lever_values={"reslot_top_50_fast_movers": {"sku_count_relocated": 40, "average_distance_reduction_m": 35, "target_zone": "dispatch_near"}},
    )
    r1 = simulate(s, levers)
    r2 = simulate(s, levers)
    assert r1.kpis.values == r2.kpis.values
