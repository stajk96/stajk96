from __future__ import annotations

from core.enums import DirectionLabel
from core.models import ExplanationBlock


LOWER_IS_BETTER_KEYS = ("risk", "distance", "time", "burden")


def explain_metric(metric_name: str, old: float, new: float, drivers: list[str], secondary: list[str]) -> ExplanationBlock:
    delta = new - old
    pct = 0.0 if old == 0 else (delta / old) * 100
    lower_is_better = any(k in metric_name for k in LOWER_IS_BETTER_KEYS)

    if abs(delta) < 0.01:
        direction = DirectionLabel.NEUTRAL
        quality = "mixed"
    elif lower_is_better:
        direction = DirectionLabel.IMPROVED if delta < 0 else DirectionLabel.WORSENED
        quality = "good" if delta < 0 else "caution"
    else:
        direction = DirectionLabel.IMPROVED if delta > 0 else DirectionLabel.WORSENED
        quality = "good" if delta > 0 else "caution"

    interpretation = (
        f"{metric_name.replace('_', ' ').title()} {direction.value} by {abs(pct):.1f}%. "
        f"Primary drivers: {', '.join(drivers[:3]) if drivers else 'none highlighted'}. "
        f"Secondary effects: {', '.join(secondary[:3]) if secondary else 'limited second-order effects'}."
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
        interpretation_text=interpretation,
        management_implication=f"This is a {quality} signal. Validate zone-level bottleneck behavior before rollout.",
        recommendation_text="Scale only with paired controls for expected drag variables.",
        caution_note="Check tradeoffs in congestion and replenishment interaction before implementation lock-in.",
    )
