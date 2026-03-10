from core.dependencies import dependency_penalties


def test_dependency_penalty_triggered():
    p = dependency_penalties({"expand_forward_pick_footprint": 0.8})
    assert p["replenishment"] > 0
