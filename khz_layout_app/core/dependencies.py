from __future__ import annotations


def dependency_penalties(levers: dict[str, dict]) -> dict[str, float]:
    penalties = {"travel": 0.0, "congestion": 0.0, "replenishment": 0.0, "space": 0.0, "route_complexity": 0.0}

    fp = float(levers.get("create_forward_pick_zone", {}).get("sku_share_moved_to_forward_pick", 0))
    fp_iso = levers.get("improve_forward_pick_replenishment_isolation", {}).get("isolation_enabled", False)
    if fp > 0.2 and not fp_iso:
        penalties["replenishment"] += 0.08
        penalties["congestion"] += 0.03

    fast_reloc = float(levers.get("reslot_top_50_fast_movers", {}).get("sku_count_relocated", 0))
    hot_aisle = float(levers.get("widen_hot_zone_aisles", {}).get("width_increase_m", 0))
    if fast_reloc >= 35 and hot_aisle < 0.2:
        penalties["congestion"] += 0.07

    staging_lanes = float(levers.get("add_staging_lanes", {}).get("lanes_added", 0))
    if staging_lanes > 6:
        penalties["space"] += 0.05

    one_way = levers.get("convert_to_one_way_aisle_flow", {}).get("enabled", False)
    cutthroughs = float(levers.get("create_cut_through_access", {}).get("count_added", 0))
    if one_way and cutthroughs < 2:
        penalties["route_complexity"] += 0.08

    return penalties
