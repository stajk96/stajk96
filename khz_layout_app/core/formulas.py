"""Deterministic, explainable indexed formulas used by the simulator."""

from __future__ import annotations

import numpy as np


def clamp(v: float, low: float = 0.0, high: float = 1.0) -> float:
    return float(max(low, min(high, v)))


def sat_gain(x: float, k: float = 1.5) -> float:
    """Diminishing returns transform, output in [0, 1)."""
    return float(1 - np.exp(-k * max(0.0, x)))


def sat_penalty(x: float, k: float = 1.2) -> float:
    """Saturating penalty for downside pressure."""
    return float(np.tanh(k * max(0.0, x)))


def indexed_kpi(base: float, pos: float, neg: float, cap_low: float = 50, cap_high: float = 150) -> float:
    """Computes capped KPI index around base=100 with explicit upside/downside."""
    value = base * (1 + pos) * (1 - neg)
    return float(max(cap_low, min(cap_high, value)))
