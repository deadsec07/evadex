from __future__ import annotations

import csv
import math
import os
from typing import Optional

import numpy as np

from .missile import Missile
from .interceptor import Interceptor
from .evasion_ai import get_noisy_interceptor_position
from .config import Scenario, load_scenario
from .planners import get_planner


DEFAULT_MAX_STEPS = 500
HIT_DISTANCE = 2.0
BOOST_COOLDOWN_TIME = 5


def run_simulation(
    max_steps: int = DEFAULT_MAX_STEPS,
    telemetry_path: str = os.path.join("out", "telemetry.csv"),
    show_gui: bool = True,
    seed: Optional[int] = None,
    scenario_path: Optional[str] = None,
    planner: str = "dwa",
) -> bool:
    """Run the 2D evasion simulation.

    Returns True if the missile evades for the duration; False if intercepted.
    """
    scenario: Optional[Scenario] = None
    if scenario_path:
        scenario = load_scenario(scenario_path)
        # scenario values override args where provided
        max_steps = scenario.max_steps
        seed = scenario.seed if scenario.seed is not None else seed
        HIT = scenario.hit_distance
        COOL = scenario.boost_cooldown_time
        if scenario.planner:
            planner = scenario.planner
    else:
        HIT = HIT_DISTANCE
        COOL = BOOST_COOLDOWN_TIME

    if seed is not None:
        np.random.seed(seed)

    # missile and interceptors
    if scenario and scenario.missile is not None:
        mx, my, ms, hd = scenario.missile
        missile = Missile(mx, my, ms, hd)
    else:
        missile = Missile(5, -10, 2.0, 30)
    if not hasattr(missile, "_thrust_cooldown"):
        missile._thrust_cooldown = 0

    if scenario and scenario.interceptors is not None:
        interceptors = [Interceptor(ix, iy, ispd) for (ix, iy, ispd) in scenario.interceptors]
    else:
        interceptors = [
            Interceptor(60, 60, 2.0),
            Interceptor(-40, 70, 2.0),
            Interceptor(70, -20, 2.0),
            Interceptor(50, -50, 2.0),
            Interceptor(-50, -50, 2.0),
            Interceptor(30, 80, 2.0),
            Interceptor(-60, 30, 2.0),
            Interceptor(0, 90, 2.0),
            Interceptor(90, 0, 2.0),
            Interceptor(-90, 0, 2.0),
        ]

    hit = False

    for t in range(max_steps):
        m_pos = missile.get_position()
        noisy_ips = [get_noisy_interceptor_position(ip.get_position()) for ip in interceptors]

        planner_fn = get_planner(planner)
        new_heading, new_speed, used_boost = planner_fn(
            current_pos=m_pos,
            interceptor_positions=noisy_ips,
            current_heading=missile.heading,
            base_speed=missile.speed,
            max_turn=missile.max_turn,
            boost_cooldown=missile._thrust_cooldown,
        )

        missile.update_heading(new_heading)
        missile.speed = new_speed
        if used_boost:
            missile._thrust_cooldown = COOL

        missile.move()

        for intr in interceptors:
            intr.pursue(missile.get_position())

        for intr in interceptors:
            if np.linalg.norm(intr.get_position() - missile.get_position()) < HIT:
                hit = True
                break
        if hit:
            break

    # telemetry output
    out_dir = os.path.dirname(telemetry_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(telemetry_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Time", "M_X", "M_Y"]
            + [f"I{j+1}_X" for j in range(len(interceptors))]
            + [f"I{j+1}_Y" for j in range(len(interceptors))]
        )
        for step in range(len(missile.trajectory)):
            row = [step] + list(missile.trajectory[step])
            for intr in interceptors:
                row += list(intr.trajectory[step])
            writer.writerow(row)

    if not show_gui:
        # headless mode
        return not hit

    # animation
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    fig, ax = plt.subplots()
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_title("EvadeX: Dynamic Window Evasion vs 10 Interceptors")
    ax.set_xlabel("X Distance")
    ax.set_ylabel("Y Distance")
    ax.grid(True)

    m_line, = ax.plot([], [], "b-", linewidth=2, label="Missile")
    i_lines = [
        ax.plot([], [], "r--", linewidth=1.5, label=f"Interceptor #{i+1}")[0]
        for i in range(len(interceptors))
    ]
    ax.legend(loc="upper left")

    def update(frame: int):
        mx, my = zip(*missile.trajectory[: frame + 1])
        m_line.set_data(mx, my)
        for idx, intr in enumerate(interceptors):
            ix, iy = zip(*intr.trajectory[: frame + 1])
            i_lines[idx].set_data(ix, iy)
        return [m_line] + i_lines

    animation.FuncAnimation(
        fig, update, frames=len(missile.trajectory), interval=200, blit=True
    )
    plt.show()
    return not hit
