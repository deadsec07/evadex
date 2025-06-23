import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv

from missile import Missile
from interceptor import Interceptor
from evasion_ai import evasive_heading, get_noisy_interceptor_position

missiles = [
    Missile(0, 0, 2, 45),
    Missile(-10, 5, 2, 60),
    Missile(5, -10, 2, 30)
]

interceptors = [
    Interceptor(60, 60, 2),
    Interceptor(-40, 70, 2),
    Interceptor(70, -20, 2)
]

HIT_DISTANCE = 2
MAX_STEPS = 100
intercepted_flags = [False] * len(missiles)
interceptor_busy = [False] * len(interceptors)

for t in range(MAX_STEPS):
    for idx, missile in enumerate(missiles):
        if intercepted_flags[idx]:
            continue

        m_pos = missile.get_position()
        closest_idx = np.argmin([np.linalg.norm(i.get_position() - m_pos) for i in interceptors])
        threat_distance = np.linalg.norm(interceptors[closest_idx].get_position() - m_pos)

        if threat_distance < 10:
            print(f"⚠️  Missile #{idx+1} is under threat! Distance: {threat_distance:.2f}")
        elif threat_distance < 20:
            print(f"🔶 Missile #{idx+1} is tracking interceptor...")

        threat_pos = get_noisy_interceptor_position(interceptors[closest_idx].get_position())
        new_heading = evasive_heading(m_pos, threat_pos, missile.heading)
        missile.update_heading(new_heading)
        missile.move()

    for i_idx, interceptor in enumerate(interceptors):
        if interceptor_busy[i_idx]:
            continue

        active_missiles = [m for j, m in enumerate(missiles) if not intercepted_flags[j]]
        if not active_missiles:
            continue

        nearest = min(active_missiles, key=lambda m: np.linalg.norm(interceptor.get_position() - m.get_position()))
        interceptor.pursue(nearest.get_position())

    for idx, m in enumerate(missiles):
        if intercepted_flags[idx]:
            continue
        for i_idx, i in enumerate(interceptors):
            if np.linalg.norm(m.get_position() - i.get_position()) < HIT_DISTANCE:
                print(f"💥 Missile #{idx+1} Intercepted!")
                intercepted_flags[idx] = True
                interceptor_busy[i_idx] = True  # That interceptor stops pursuing others
                break

if not any(intercepted_flags):
    print("\n✅ Mission Success: All missiles evaded tracking!")
else:
    survived = sum(1 for i in intercepted_flags if not i)
    print(f"\n⚠️  {survived}/{len(missiles)} missiles survived.")

# CSV Telemetry
with open("telemetry.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["TimeStep", *[f"M{i+1}_X" for i in range(len(missiles))], *[f"M{i+1}_Y" for i in range(len(missiles))], *[f"I{i+1}_X" for i in range(len(interceptors))], *[f"I{i+1}_Y" for i in range(len(interceptors))]])
    for t in range(MAX_STEPS):
        row = [t]
        for m in missiles:
            if t < len(m.trajectory):
                row.extend(m.trajectory[t])
            else:
                row.extend([None, None])
        for i in interceptors:
            if t < len(i.trajectory):
                row.extend(i.trajectory[t])
            else:
                row.extend([None, None])
        writer.writerow(row)

# Animation
fig, ax = plt.subplots()
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
ax.set_title("EvadeX: Missile Evasion vs Interceptors")
ax.set_xlabel("X Distance (km)")
ax.set_ylabel("Y Distance (km)")
ax.grid(True)

lines_m = [ax.plot([], [], 'b-', linewidth=2)[0] for _ in missiles]
lines_i = [ax.plot([], [], 'r--', linewidth=1.5)[0] for _ in interceptors]

plt.legend(lines_m + lines_i, [f"Missile #{i+1}" for i in range(len(missiles))] +
           [f"Interceptor #{i+1}" for i in range(len(interceptors))])

def update(frame):
    for idx, m in enumerate(missiles):
        if frame < len(m.trajectory):
            traj = list(zip(*m.trajectory[:frame+1]))
            lines_m[idx].set_data(traj[0], traj[1])
    for idx, i in enumerate(interceptors):
        if frame < len(i.trajectory):
            traj = list(zip(*i.trajectory[:frame+1]))
            lines_i[idx].set_data(traj[0], traj[1])
    return lines_m + lines_i

ani = animation.FuncAnimation(fig, update, frames=MAX_STEPS, blit=True)
plt.show()
