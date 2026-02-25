from __future__ import annotations

import math
from typing import Callable

import numpy as np

from .evasion_ai import evasive_heading as evasive_heading_dwa


PlannerFn = Callable[
    [np.ndarray, list[np.ndarray], float, float, float, int],
    tuple[float, float, bool],
]


def greedy_clearance_heading(
    current_pos: np.ndarray,
    interceptor_positions: list[np.ndarray],
    current_heading: float,
    base_speed: float,
    max_turn: float,
    boost_cooldown: int,
) -> tuple[float, float, bool]:
    """Pick the heading within the allowed turn that maximizes one-step clearance.

    No boost is used; speed remains at base_speed.
    """
    samples = 21
    headings = np.linspace(current_heading - max_turn, current_heading + max_turn, samples)
    best_h = current_heading
    best_score = -np.inf
    for h in headings:
        # one-step projected position
        next_pos = current_pos + np.array([math.cos(h), math.sin(h)]) * base_speed
        min_dist = min(float(np.linalg.norm(next_pos - ip)) for ip in interceptor_positions)
        # small bias toward forward continuity (less turning)
        turn_mag = abs(math.atan2(math.sin(h - current_heading), math.cos(h - current_heading)))
        score = min_dist - 0.05 * turn_mag
        if score > best_score:
            best_score = score
            best_h = h
    return best_h, float(base_speed), False


def get_planner(name: str) -> PlannerFn:
    key = name.strip().lower()
    if key in {"dwa", "evasion_ai", "default"}:
        return evasive_heading_dwa
    if key in {"greedy", "clearance"}:
        return greedy_clearance_heading
    raise ValueError(f"Unknown planner '{name}'")

