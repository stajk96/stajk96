from __future__ import annotations


def dependency_penalties(levers: dict[str, float]) -> dict[str, float]:
    penalties = {"travel": 0.0, "congestion": 0.0, "replenishment": 0.0, "space": 0.0}
    if levers.get("expand_forward_pick_footprint", 0) > 0.4:
        penalties["replenishment"] += 0.06
    if levers.get("reslot_top_50_fast_movers", 0) > 0.5:
        penalties["congestion"] += 0.05
    if levers.get("reduce_aisle_width", 0) > 0.4:
        penalties["congestion"] += 0.08
        penalties["travel"] += 0.03
    if levers.get("add_staging_lanes", 0) > 0.3 and levers.get("improve_staging_to_door_mapping", 0) < 0.2:
        penalties["space"] += 0.03
    return penalties
