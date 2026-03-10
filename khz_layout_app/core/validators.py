from __future__ import annotations

from core.models import BaselineOperationalInputs, LayoutGeometry, ValidationIssue


def validate_inputs(geometry: LayoutGeometry, ops: BaselineOperationalInputs) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if geometry.usable_area > geometry.total_area:
        issues.append(ValidationIssue(field="usable_area", severity="error", message="Usable area exceeds total area."))
    if abs((ops.abc_a_share + ops.abc_b_share + ops.abc_c_share) - 1.0) > 0.01:
        issues.append(ValidationIssue(field="abc_shares", severity="warning", message="ABC shares should sum to 1.0."))
    if geometry.aisle_width_m < 2.2:
        issues.append(ValidationIssue(field="aisle_width_m", severity="warning", message="Very narrow aisles may increase safety and congestion risk."))
    return issues
