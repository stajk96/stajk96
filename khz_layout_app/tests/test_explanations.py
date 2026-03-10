from core.explanations import explain_metric


def test_explanation_fields():
    b = explain_metric("estimated_pick_time_index", 100, 92, ["slotting", "flow", "dock"], ["congestion", "replenishment", "hotspot"])
    assert b.metric_name == "estimated_pick_time_index"
    assert b.direct_driver_rank_1 == "slotting"
