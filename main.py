# main.py

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
import math

from missile import Missile
from interceptor import Interceptor
from evasion_ai import evasive_heading, get_noisy_interceptor_position

# === Simulation parameters ===
MISSILE_DESTINATION = np.array([100, 100], dtype=float)
HIT_DISTANCE        = 2.0
MAX_STEPS           = 500
BOOST_COOLDOWN_TIME = 5    # steps of cooldown after a boost

# === Initialize missile & interceptors ===
missile = Missile(5, -10, 2.0, 30)
# ensure missile has a cooldown counter
if not hasattr(missile, "_thrust_cooldown"):
    missile._thrust_cooldown = 0

interceptors = [
    Interceptor(60,  60, 2.0), Interceptor(-40, 70, 2.0),
    Interceptor(70, -20, 2.0), Interceptor(50, -50,2.0),
    Interceptor(-50,-50, 2.0), Interceptor(30,  80,2.0),
    Interceptor(-60, 30, 2.0), Interceptor(0,   90,2.0),
    Interceptor(90,   0, 2.0), Interceptor(-90,  0,2.0),
]

hit = False

# === Main simulation loop ===
for t in range(MAX_STEPS):
    # 1) Current missile position
    m_pos = missile.get_position()

    # 2) Sense interceptors (with optional noise)
    noisy_ips = [
        get_noisy_interceptor_position(ip.get_position())
        for ip in interceptors
    ]

    # 3) Compute evasion maneuver via DWA
    new_heading, new_speed, used_boost = evasive_heading(
        current_pos          = m_pos,
        interceptor_positions = noisy_ips,
        current_heading      = missile.heading,
        base_speed           = missile.speed,
        max_turn             = missile.max_turn,
        boost_cooldown       = missile._thrust_cooldown
    )

    # 4) Apply heading & speed
    missile.update_heading(new_heading)
    missile.speed = new_speed
    if used_boost:
        missile._thrust_cooldown = BOOST_COOLDOWN_TIME

    # 5) Move the missile
    missile.move()

    # 6) Move all interceptors (pure pursuit)
    for intr in interceptors:
        intr.pursue(missile.get_position())

    # 7) Check for interception
    for idx, intr in enumerate(interceptors):
        if np.linalg.norm(intr.get_position() - missile.get_position()) < HIT_DISTANCE:
            print(f"💥 Intercepted by interceptor #{idx+1} at step {t}")
            hit = True
            break
    if hit:
        break

if not hit:
    print("\n✅ Mission Success: Missile evaded all interceptors!")

# === Write telemetry.csv ===
with open("telemetry.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        ["Time", "M_X", "M_Y"] +
        [f"I{j+1}_X" for j in range(len(interceptors))] +
        [f"I{j+1}_Y" for j in range(len(interceptors))]
    )
    for step in range(len(missile.trajectory)):
        row = [step] + list(missile.trajectory[step])
        for intr in interceptors:
            # trajectories are synchronized in length
            row += list(intr.trajectory[step])
        writer.writerow(row)

# === Animate the result ===
fig, ax = plt.subplots()
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
ax.set_title("EvadeX: Dynamic Window Evasion vs 10 Interceptors")
ax.set_xlabel("X Distance")
ax.set_ylabel("Y Distance")
ax.grid(True)

m_line, = ax.plot([], [], 'b-', linewidth=2, label="Missile")
i_lines = [
    ax.plot([], [], 'r--', linewidth=1.5, label=f"Interceptor #{i+1}")[0]
    for i in range(len(interceptors))
]
ax.legend(loc="upper left")

def update(frame):
    mx, my = zip(*missile.trajectory[:frame+1])
    m_line.set_data(mx, my)
    for idx, intr in enumerate(interceptors):
        ix, iy = zip(*intr.trajectory[:frame+1])
        i_lines[idx].set_data(ix, iy)
    return [m_line] + i_lines

ani = animation.FuncAnimation(
    fig, update,
    frames=len(missile.trajectory),
    interval=200,    # slowed for clarity
    blit=True
)
plt.show()
