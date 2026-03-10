from __future__ import annotations

from core.models import Recommendation


def recommend_from_kpis(kpis: dict[str, float]) -> list[Recommendation]:
    recs: list[Recommendation] = []

    travel = kpis.get("estimated_travel_distance_per_pick", 100)
    repl = kpis.get("replenishment_burden_index", 100)
    congest = kpis.get("congestion_risk_score", 100)
    space = kpis.get("layout_utilization_pct", 100)
    dock = kpis.get("dock_staging_efficiency_score", 100)

    if travel < 98 and repl > 102:
        recs.append(Recommendation(title="Protect travel gains", priority="high", action="Travel improved, but replenishment burden rose. Add replenishment path isolation and timed replen windows."))
    if congest > 103:
        recs.append(Recommendation(title="Hotspot mitigation", priority="high", action="Apply hotspot dispersion and widen hot-zone aisles before scaling re-slotting changes."))
    if dock > 104 and space < 96:
        recs.append(Recommendation(title="Dock-space tradeoff review", priority="medium", action="Dock/staging gains are consuming space. Rebalance staging lane footprint by wave profile."))
    if kpis.get("scenario_overall_score", 100) < 95:
        recs.append(Recommendation(title="Re-sequence implementation", priority="high", action="Current scenario likely over-concentrates risky interventions. Stage actions in two phases."))

    if not recs:
        recs.append(Recommendation(title="Progressive rollout", priority="low", action="Scenario is balanced. Pilot in one zone with weekly KPI and bottleneck review."))

    return recs
