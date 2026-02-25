import math

import numpy as np

# Destination for the 2D demo (must match sim2d default)
MISSILE_DESTINATION = np.array([100.0, 100.0], dtype=float)

# DWA hyperparameters
HORIZON_STEPS = 3
HEADING_SAMPLES = 11  # odd for symmetry
SPEED_OPTIONS = [
    lambda base: base,
    lambda base: base + 1.0,  # optional burst
]
GOAL_WEIGHT = 0.1
POWER_WEIGHT = 0.5
INTERCEPT_WEIGHT = 1.0


def get_noisy_interceptor_position(true_pos: np.ndarray) -> np.ndarray:
    return true_pos + np.random.normal(0, 1.0, size=2)


def evasive_heading(
    current_pos: np.ndarray,
    interceptor_positions: list[np.ndarray],
    current_heading: float,
    base_speed: float,
    max_turn: float,
    boost_cooldown: int,
) -> tuple[float, float, bool]:
    """Return (new_heading, chosen_speed, used_boost)."""
    best_score = -np.inf
    best = (current_heading, base_speed, False)

    # candidate headings within ±max_turn
    headings = np.linspace(
        current_heading - max_turn, current_heading + max_turn, HEADING_SAMPLES
    )

    # candidate speeds based on boost availability
    speed_funcs = SPEED_OPTIONS if boost_cooldown == 0 else SPEED_OPTIONS[:1]

    for h in headings:
        for use_boost, speed_fn in enumerate(speed_funcs):
            s = float(speed_fn(base_speed))

            # simulate a few steps
            mpos = current_pos.copy()
            ips = [p.copy() for p in interceptor_positions]
            min_dist = np.inf
            goal_progress = 0.0

            for _ in range(HORIZON_STEPS):
                # move missile
                mpos += np.array([math.cos(h), math.sin(h)]) * s
                # move pursuers
                for j, ip in enumerate(ips):
                    vec = mpos - ip
                    d = np.linalg.norm(vec)
                    if d > 1e-6:
                        ips[j] = ip + (vec / d) * s
                    min_dist = min(min_dist, d)
                # accumulate goal progress (how much closer to goal)
                goal_progress += np.linalg.norm(MISSILE_DESTINATION - mpos)

            # score = clearance – λ1*(goal distance) – λ2*(power penalty)
            power_pen = POWER_WEIGHT * ((s - base_speed) ** 2)
            score = (
                INTERCEPT_WEIGHT * min_dist - GOAL_WEIGHT * goal_progress - power_pen
            )

            if score > best_score:
                best_score = score
                best = (h, s, use_boost == 1)

    return best  # (heading_rad, speed, used_boost)
