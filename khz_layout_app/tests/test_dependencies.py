from core.dependencies import dependency_penalties


def test_dependency_penalty_triggered():
    p = dependency_penalties({"create_forward_pick_zone": {"sku_share_moved_to_forward_pick": 0.4}})
    assert p["replenishment"] > 0
