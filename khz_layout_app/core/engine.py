from __future__ import annotations

import json

from core.dependencies import dependency_penalties
from core.formulas import clamp, indexed_kpi, sat_gain, sat_penalty
from core.models import BottleneckState, IntermediateState, KPIState, Scenario, ScenarioResult
from core.scoring import overall_score


BASE_INTERMEDIATE = {
    "travel_distance_index": 1.0,
    "travel_time_index": 1.0,
    "pick_density_index": 1.0,
    "slotting_quality_index": 1.0,
    "congestion_index": 1.0,
    "replenishment_interference_index": 1.0,
    "dock_adjacency_index": 1.0,
    "staging_efficiency_index": 1.0,
    "flow_separation_index": 1.0,
    "route_complexity_index": 1.0,
    "hotspot_concentration_index": 1.0,
    "usable_space_index": 1.0,
    "cube_utilization_index": 1.0,
    "accessibility_index": 1.0,
    "forward_pick_effectiveness_index": 1.0,
    "reserve_pressure_index": 1.0,
    "zone_balance_index": 1.0,
    "service_risk_index": 1.0,
    "temperature_integrity_risk_index": 1.0,
}


def simulate(scenario: Scenario, lever_catalog: list[dict]) -> ScenarioResult:
    inter = BASE_INTERMEDIATE.copy()
    drivers: dict[str, float] = {}
    for lever in lever_catalog:
        lever_id = lever["lever_id"]
        raw = scenario.lever_values.get(lever_id, float(lever["default"]))
        norm = 0 if float(lever["max"]) == float(lever["min"]) else (raw - float(lever["min"])) / (float(lever["max"]) - float(lever["min"]))
        impact = sat_gain(norm) * float(lever["weight"])
        for k, v in json.loads(lever["direct_impacts_json"]).items():
            inter[k] = clamp(inter.get(k, 1.0) + impact * float(v), 0.5, 1.6)
        for k, v in json.loads(lever["secondary_impacts_json"]).items():
            inter[k] = clamp(inter.get(k, 1.0) + sat_penalty(norm) * float(v) * 0.5, 0.5, 1.6)
        drivers[lever_id] = round(impact, 4)

    penalties = dependency_penalties(scenario.lever_values)
    inter["travel_time_index"] = clamp(inter["travel_time_index"] + penalties["travel"], 0.5, 1.7)
    inter["congestion_index"] = clamp(inter["congestion_index"] + penalties["congestion"], 0.5, 1.7)
    inter["replenishment_interference_index"] = clamp(inter["replenishment_interference_index"] + penalties["replenishment"], 0.5, 1.7)
    inter["usable_space_index"] = clamp(inter["usable_space_index"] - penalties["space"], 0.5, 1.7)

    b = {
        "Travel & Accessibility": (inter["travel_distance_index"] + inter["accessibility_index"] + inter["route_complexity_index"]) / 3,
        "Slotting & Pick Density": (inter["slotting_quality_index"] + inter["pick_density_index"] + inter["forward_pick_effectiveness_index"]) / 3,
        "Congestion & Flow Interference": (inter["congestion_index"] + inter["flow_separation_index"] + inter["hotspot_concentration_index"]) / 3,
        "Replenishment Interaction": (inter["replenishment_interference_index"] + inter["reserve_pressure_index"]) / 2,
        "Dock & Staging Efficiency": (inter["dock_adjacency_index"] + inter["staging_efficiency_index"]) / 2,
        "Space & Cube Utilization": (inter["usable_space_index"] + inter["cube_utilization_index"]) / 2,
        "Temperature / Zone Integrity": (inter["temperature_integrity_risk_index"] + inter["zone_balance_index"]) / 2,
        "Flexibility / Resilience": (inter["zone_balance_index"] + inter["service_risk_index"] + inter["flow_separation_index"]) / 3,
    }

    pos = sat_gain(inter["slotting_quality_index"] - 1 + inter["dock_adjacency_index"] - 1 + inter["usable_space_index"] - 1)
    neg = sat_penalty(inter["congestion_index"] - 1 + inter["replenishment_interference_index"] - 1 + inter["route_complexity_index"] - 1)

    kpis = {
        "layout_utilization_pct": indexed_kpi(100, sat_gain(inter["usable_space_index"] - 1), sat_penalty(inter["congestion_index"] - 1), 70, 140),
        "usable_cube_pct": indexed_kpi(100, sat_gain(inter["cube_utilization_index"] - 1), sat_penalty(inter["accessibility_index"] - 1), 70, 140),
        "accessibility_score": indexed_kpi(100, sat_gain(inter["accessibility_index"] - 1), sat_penalty(inter["congestion_index"] - 1)),
        "estimated_travel_distance_per_pick": indexed_kpi(100, sat_gain(1 - inter["travel_distance_index"]), sat_penalty(inter["travel_distance_index"] - 1)),
        "estimated_pick_time_index": indexed_kpi(100, sat_gain(1 - inter["travel_time_index"]), sat_penalty(inter["travel_time_index"] - 1)),
        "estimated_lines_per_labor_hour_index": indexed_kpi(100, pos, neg),
        "congestion_risk_score": indexed_kpi(100, sat_gain(1 - inter["congestion_index"]), sat_penalty(inter["congestion_index"] - 1)),
        "replenishment_burden_index": indexed_kpi(100, sat_gain(1 - inter["replenishment_interference_index"]), sat_penalty(inter["replenishment_interference_index"] - 1)),
        "dock_staging_efficiency_score": indexed_kpi(100, sat_gain(inter["dock_adjacency_index"] - 1 + inter["staging_efficiency_index"] - 1), sat_penalty(inter["flow_separation_index"] - 1)),
        "order_flow_smoothness_score": indexed_kpi(100, sat_gain(inter["flow_separation_index"] - 1), sat_penalty(inter["route_complexity_index"] - 1 + inter["hotspot_concentration_index"] - 1)),
        "backlog_risk_index": indexed_kpi(100, sat_gain(1 - inter["service_risk_index"]), sat_penalty(inter["service_risk_index"] - 1)),
        "service_risk_index": indexed_kpi(100, sat_gain(1 - inter["service_risk_index"]), sat_penalty(inter["service_risk_index"] - 1)),
        "flexibility_score": indexed_kpi(100, sat_gain(inter["zone_balance_index"] - 1 + inter["flow_separation_index"] - 1), sat_penalty(inter["reserve_pressure_index"] - 1)),
    }
    kpis["scenario_overall_score"] = overall_score(kpis)

    return ScenarioResult(
        scenario_name=scenario.name,
        intermediate=IntermediateState(values={k: round(v, 3) for k, v in inter.items()}),
        bottlenecks=BottleneckState(values={k: round(v * 100, 2) for k, v in b.items()}),
        kpis=KPIState(values={k: round(v, 2) for k, v in kpis.items()}),
        drivers=drivers,
    )
