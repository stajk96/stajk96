from enum import Enum


class WarehouseArchetype(str, Enum):
    DRY_PALLET = "Dry FMCG pallet warehouse"
    DRY_PALLET_CASE = "Dry pallet + case-pick warehouse"
    FORWARD_PICK = "Forward-pick / fast-pick warehouse"
    MULTI_TEMP = "Multi-temperature FMCG warehouse"
    PARTIAL_AUTO = "Partially automated warehouse"
    LARGE_AUTO_DC = "Large automated dry-goods DC archetype"


class TemperatureType(str, Enum):
    DRY = "dry"
    CHILLED = "chilled"
    FROZEN = "frozen"
    MIXED = "mixed"


class AutomationLevel(str, Enum):
    MANUAL = "manual"
    PARTIAL = "partial"
    HIGH = "high"


class DirectionLabel(str, Enum):
    IMPROVED = "improved"
    WORSENED = "worsened"
    NEUTRAL = "neutral"
