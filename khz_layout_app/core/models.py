from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from core.enums import AutomationLevel, DirectionLabel, TemperatureType, WarehouseArchetype


class SiteProfile(BaseModel):
    site_name: str = "Sample Site"
    country: str = "UK"
    region: str = "EMEA"
    business_unit: str = "Meals"
    warehouse_archetype: WarehouseArchetype = WarehouseArchetype.DRY_PALLET_CASE
    temperature_type: TemperatureType = TemperatureType.DRY
    automation_level: AutomationLevel = AutomationLevel.PARTIAL


class LayoutGeometry(BaseModel):
    total_area: float = 20000
    usable_area: float = 16000
    clear_height: float = 11
    storage_rows: int = 30
    row_length_m: float = 70
    aisle_count: int = 28
    aisle_width_m: float = 3.5
    cross_aisle_count: int = 3
    cross_aisle_placement_quality: float = 0.6
    lane_depth: int = 4
    pallet_positions: int = 15000
    rack_share: float = 0.7
    floor_stack_share: float = 0.3
    forward_pick_area: float = 1800
    reserve_area: float = 9000
    dock_door_count: int = 24
    inbound_door_count: int = 10
    outbound_door_count: int = 14
    staging_area_size: float = 2200
    staging_lane_count: int = 26


class BaselineOperationalInputs(BaseModel):
    receiving_shipping_adjacency: float = 0.5
    zone_separation_quality: float = 0.6
    replenishment_overlap: float = 0.4
    congestion_hotspots: float = 0.5
    pedestrian_mhe_conflict: float = 0.4
    end_aisle_clutter: float = 0.4
    family_grouping_quality: float = 0.6
    abc_slotting_compliance: float = 0.6
    affinity_slotting_quality: float = 0.5
    fast_mover_proximity: float = 0.6
    heavy_sku_placement_quality: float = 0.5
    seasonality_zoning_quality: float = 0.5
    fp_replenishment_isolation: float = 0.5
    case_pallet_segregation: float = 0.6
    route_cutthrough_availability: float = 0.4
    one_way_aisle_discipline: float = 0.5
    pick_zone_balance: float = 0.5
    sku_count: int = 12000
    abc_a_share: float = 0.2
    abc_b_share: float = 0.3
    abc_c_share: float = 0.5
    pallet_share: float = 0.6
    case_share: float = 0.3
    split_case_share: float = 0.1
    lines_per_order: float = 8
    picks_per_day: int = 18000
    fast_pick_sku_count: int = 1200




class StorageZone(BaseModel):
    zone_id: str = "Z1"
    temperature_class: str = "dry"
    area_type: str = "pick"


class DockStagingConfig(BaseModel):
    inbound_lanes: int = 10
    outbound_lanes: int = 14
    staging_to_door_mapping_quality: float = 0.6


class FlowConstraint(BaseModel):
    bottleneck_area: str
    severity: float = 0.5


class LeverImpactProfile(BaseModel):
    direct: dict[str, float] = Field(default_factory=dict)
    secondary: dict[str, float] = Field(default_factory=dict)


class LayoutLever(BaseModel):
    lever_id: str
    group: str
    subgroup: str
    label: str
    description: str
    input_type: str
    min: float
    max: float
    default: float
    step: float
    unit: str
    direct_impacts_json: str
    secondary_impacts_json: str
    dependencies_json: str
    conflicts_json: str
    explanation_template: str
    direction_rule: str
    effort_level: str
    weight: float


class LeverInputValue(BaseModel):
    lever_id: str
    value: float


class IntermediateState(BaseModel):
    values: dict[str, float]


class BottleneckState(BaseModel):
    values: dict[str, float]


class KPIState(BaseModel):
    values: dict[str, float]


class Scenario(BaseModel):
    name: str
    site: SiteProfile
    geometry: LayoutGeometry
    operational: BaselineOperationalInputs
    lever_values: dict[str, float] = Field(default_factory=dict)


class ScenarioResult(BaseModel):
    scenario_name: str
    intermediate: IntermediateState
    bottlenecks: BottleneckState
    kpis: KPIState
    drivers: dict[str, float]


class ScenarioComparison(BaseModel):
    baseline: ScenarioResult
    scenarios: list[ScenarioResult]


@dataclass
class ChangeLogEntry:
    timestamp: str
    site: str
    scenario: str
    lever_id: str
    lever_label: str
    old_value: float
    new_value: float
    reason_text: str
    impacted_variables: list[str] = field(default_factory=list)
    impacted_bottlenecks: list[str] = field(default_factory=list)
    impacted_kpis: list[str] = field(default_factory=list)


class ExplanationBlock(BaseModel):
    metric_name: str
    old_value: float
    new_value: float
    absolute_delta: float
    percent_delta: float
    direction_label: DirectionLabel
    direct_driver_rank_1: str
    direct_driver_rank_2: str
    direct_driver_rank_3: str
    secondary_effect_rank_1: str
    secondary_effect_rank_2: str
    secondary_effect_rank_3: str
    interpretation_text: str
    management_implication: str
    recommendation_text: str
    caution_note: str


class Recommendation(BaseModel):
    title: str
    priority: str
    action: str


class ImportMappingProfile(BaseModel):
    name: str
    mappings: dict[str, str]
    units: dict[str, str] = Field(default_factory=dict)


class ValidationIssue(BaseModel):
    field: str
    severity: str
    message: str


def now_iso() -> str:
    return datetime.utcnow().isoformat()
