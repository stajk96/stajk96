from core.recommendations import recommend_from_kpis


def test_recommendation_generation():
    recs = recommend_from_kpis({
        "estimated_travel_distance_per_pick": 95,
        "replenishment_burden_index": 110,
        "congestion_risk_score": 108,
        "layout_utilization_pct": 94,
        "dock_staging_efficiency_score": 108,
        "scenario_overall_score": 92,
    })
    assert len(recs) >= 1
