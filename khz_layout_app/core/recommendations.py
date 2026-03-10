from __future__ import annotations

from core.models import Recommendation


def recommend_from_kpis(kpis: dict[str, float]) -> list[Recommendation]:
    recs: list[Recommendation] = []
    if kpis.get("congestion_risk_score", 100) > 105:
        recs.append(Recommendation(title="Mitigate congestion", priority="high", action="Increase one-way aisle discipline and reduce hotspot overlaps."))
    if kpis.get("replenishment_burden_index", 100) > 105:
        recs.append(Recommendation(title="Rebalance forward-pick", priority="medium", action="Isolate replenishment windows and review FP footprint."))
    if kpis.get("dock_staging_efficiency_score", 100) < 95:
        recs.append(Recommendation(title="Dock-staging redesign", priority="high", action="Improve staging-to-door mapping and lane segregation."))
    if not recs:
        recs.append(Recommendation(title="Maintain and monitor", priority="low", action="Track KPI drift and run monthly scenario refresh."))
    return recs
