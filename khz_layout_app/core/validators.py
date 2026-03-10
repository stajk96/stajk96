from __future__ import annotations

from core.models import BaselineOperationalInputs, KHZTemplateParseResult, LayoutGeometry, ValidationIssue


def validate_inputs(geometry: LayoutGeometry, ops: BaselineOperationalInputs) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if geometry.usable_area > geometry.total_area:
        issues.append(ValidationIssue(field="usable_area", severity="error", message="Usable area exceeds total area."))
    if abs((ops.abc_a_share + ops.abc_b_share + ops.abc_c_share) - 1.0) > 0.01:
        issues.append(ValidationIssue(field="abc_shares", severity="warning", message="ABC shares should sum to 1.0."))
    if geometry.aisle_width_m < 2.2:
        issues.append(ValidationIssue(field="aisle_width_m", severity="warning", message="Very narrow aisles may increase safety and congestion risk."))
    return issues


def validate_khz_parse_result(result: KHZTemplateParseResult) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not result.detected:
        issues.append(ValidationIssue(field="workbook_mode", severity="warning", message="Workbook does not strongly match KHZ template naming."))
    if not result.recognized_sheets:
        issues.append(ValidationIssue(field="recognized_sheets", severity="error", message="No KHZ structured sheets were recognized."))
    if result.unmapped_observations:
        issues.append(ValidationIssue(field="unmapped_observations", severity="warning", message=f"{len(result.unmapped_observations)} observations need manual review."))
    return issues
