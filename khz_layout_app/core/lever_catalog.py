from __future__ import annotations

from pathlib import Path

import yaml

from core.models import EnhancedLayoutLever


CATALOG_PATH = Path("data/layout_lever_catalog.yaml")


def load_lever_catalog(path: str | Path = CATALOG_PATH) -> list[EnhancedLayoutLever]:
    with open(path, "r", encoding="utf-8") as f:
        payload = yaml.safe_load(f)
    return [EnhancedLayoutLever.model_validate(item) for item in payload["levers"]]


def lever_default_inputs(lever: EnhancedLayoutLever) -> dict[str, float | str | bool]:
    defaults: dict[str, float | str | bool] = {}
    for p in lever.input_parameters:
        defaults[p.name] = p.default
    return defaults


def lever_intensity(lever: EnhancedLayoutLever, values: dict[str, float | str | bool]) -> float:
    """Normalize parameterized lever inputs into a single intensity score [0..1]."""
    if not lever.input_parameters:
        return 0.0
    scores: list[float] = []
    for p in lever.input_parameters:
        v = values.get(p.name, p.default)
        if p.input_type == "toggle":
            scores.append(1.0 if bool(v) else 0.0)
        elif p.input_type == "selectbox":
            if not p.options:
                scores.append(0.0)
            else:
                idx = p.options.index(v) if v in p.options else 0
                denom = max(len(p.options) - 1, 1)
                scores.append(idx / denom)
        else:
            if p.min is None or p.max is None or float(p.max) == float(p.min):
                scores.append(0.0)
            else:
                scores.append((float(v) - float(p.min)) / (float(p.max) - float(p.min)))
    bounded = [max(0.0, min(1.0, s)) for s in scores]
    return sum(bounded) / len(bounded)
