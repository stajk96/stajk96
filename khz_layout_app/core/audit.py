from __future__ import annotations

from core.models import ChangeLogEntry, now_iso


def log_change(site: str, scenario: str, lever_id: str, lever_label: str, old: float, new: float, reason: str, impacted_vars: list[str], impacted_bottlenecks: list[str], impacted_kpis: list[str]) -> ChangeLogEntry:
    return ChangeLogEntry(
        timestamp=now_iso(),
        site=site,
        scenario=scenario,
        lever_id=lever_id,
        lever_label=lever_label,
        old_value=old,
        new_value=new,
        reason_text=reason,
        impacted_variables=impacted_vars,
        impacted_bottlenecks=impacted_bottlenecks,
        impacted_kpis=impacted_kpis,
    )
