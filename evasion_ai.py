# evasion_ai.py

import numpy as np
import math

# must match your main.py goal
MISSILE_DESTINATION = np.array([100, 100], dtype=float)

# DWA hyperparameters
HORIZON_STEPS     = 3            # how many steps ahead to simulate
HEADING_SAMPLES   = 11           # odd number for symmetry
SPEED_OPTIONS     = [            # base speed and 1x boost
    lambda base: base,
    lambda base: base + 1.0      # optional one‐unit burst
]
GOAL_WEIGHT       = 0.1          # trade‐off: goal progress vs. clearance
POWER_WEIGHT      = 0.5          # penalty per (speed−base_speed)²
INTERCEPT_WEIGHT  = 1.0          # weight on staying away from pursuers

def get_noisy_interceptor_position(true_pos):
    # keep your existing noise model
    return true_pos + np.random.normal(0, 1.0, size=2)

def evasive_heading(current_pos, interceptor_positions,
                    current_heading, base_speed, max_turn, boost_cooldown):
    """
    Returns (new_heading, chosen_speed, used_boost_bool).
    main.py can then do:
        missile.update_heading(new_heading)
        missile.set_speed(chosen_speed)
    and decrement boost_cooldown if used.
    """
    best_score = -np.inf
    best = (current_heading, base_speed, False)

    # generate candidate headings within ±max_turn
    headings = np.linspace(current_heading - max_turn,
                           current_heading + max_turn,
                           HEADING_SAMPLES)

    # generate candidate speeds based on boost availability
    speed_funcs = SPEED_OPTIONS if boost_cooldown == 0 else SPEED_OPTIONS[:1]

    for h in headings:
        for use_boost, speed_fn in enumerate(speed_funcs):
            s = speed_fn(base_speed)
            # simulate a few steps
            mpos = current_pos.copy()
            ips = [p.copy() for p in interceptor_positions]
            min_dist = np.inf
            goal_progress = 0.0

            for step in range(HORIZON_STEPS):
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

            # cost = (clearance) – λ1*(sum goal dist) – λ2*(power penalty)
            power_pen = POWER_WEIGHT * ((s - base_speed) ** 2)
            cost = INTERCEPT_WEIGHT * min_dist \
                   - GOAL_WEIGHT * goal_progress \
                   - power_pen

            if cost > best_score:
                best_score = cost
                best = (h, s, use_boost == 1)

    return best  # (heading_rad, speed, used_boost)
