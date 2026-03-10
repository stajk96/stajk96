from __future__ import annotations

from core.enums import DirectionLabel
from core.models import ExplanationBlock


def explain_metric(metric_name: str, old: float, new: float, drivers: list[str], secondary: list[str]) -> ExplanationBlock:
    delta = new - old
    pct = 0.0 if old == 0 else (delta / old) * 100
    if abs(delta) < 0.01:
        direction = DirectionLabel.NEUTRAL
    elif metric_name.endswith("risk_index") or "distance" in metric_name or "time" in metric_name or "burden" in metric_name:
        direction = DirectionLabel.IMPROVED if delta < 0 else DirectionLabel.WORSENED
    else:
        direction = DirectionLabel.IMPROVED if delta > 0 else DirectionLabel.WORSENED
    text = (
        f"{metric_name} {'improved' if direction == DirectionLabel.IMPROVED else 'worsened' if direction == DirectionLabel.WORSENED else 'was stable'} "
        f"by {abs(pct):.1f}% because of {', '.join(drivers[:3])}."
    )
    return ExplanationBlock(
        metric_name=metric_name,
        old_value=old,
        new_value=new,
        absolute_delta=delta,
        percent_delta=pct,
        direction_label=direction,
        direct_driver_rank_1=drivers[0] if len(drivers) > 0 else "n/a",
        direct_driver_rank_2=drivers[1] if len(drivers) > 1 else "n/a",
        direct_driver_rank_3=drivers[2] if len(drivers) > 2 else "n/a",
        secondary_effect_rank_1=secondary[0] if len(secondary) > 0 else "n/a",
        secondary_effect_rank_2=secondary[1] if len(secondary) > 1 else "n/a",
        secondary_effect_rank_3=secondary[2] if len(secondary) > 2 else "n/a",
        interpretation_text=text,
        management_implication="Prioritize changes with net-positive impact and low drag.",
        recommendation_text="Pilot in one zone before scale-up.",
        caution_note="Check congestion and replenishment side-effects.",
    )
