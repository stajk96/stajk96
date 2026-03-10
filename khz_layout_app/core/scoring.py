from __future__ import annotations


def overall_score(kpis: dict[str, float]) -> float:
    weights = {
        "layout_utilization_pct": 0.08,
        "usable_cube_pct": 0.07,
        "accessibility_score": 0.1,
        "estimated_travel_distance_per_pick": 0.12,
        "estimated_pick_time_index": 0.1,
        "estimated_lines_per_labor_hour_index": 0.12,
        "congestion_risk_score": 0.1,
        "replenishment_burden_index": 0.08,
        "dock_staging_efficiency_score": 0.08,
        "order_flow_smoothness_score": 0.08,
        "backlog_risk_index": 0.04,
        "service_risk_index": 0.05,
        "flexibility_score": 0.08,
    }
    score = 0.0
    for k, w in weights.items():
        v = kpis.get(k, 100)
        norm = v if "distance" not in k and "risk" not in k and "burden" not in k and "time" not in k else (200 - v)
        score += w * max(0, min(150, norm))
    return round(score, 2)
