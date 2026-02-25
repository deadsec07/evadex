# visualize_3d_dwa.py

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# ─── Configuration ──────────────────────────────────────────────────────────
DT = 0.5  # time step
HORIZON_STEPS = 10  # how many look‐ahead steps for scoring
HEADING_SAMPLES = 50  # number of candidate headings to sample
SPEED = 1.0  # constant speed for both missile and interceptors
GOAL = np.array([100.0, 0.0, 0.0])
INTERCEPTOR_INITS = [[0.0, 20.0, 20.0], [0.0, -20.0, 20.0], [0.0, 20.0, -20.0]]


# ─── DWA‐style control (3D) ─────────────────────────────────────────────────
def sample_headings(n):
    # Uniformly sample n points on the unit sphere
    vecs = np.random.normal(size=(n, 3))
    vecs /= np.linalg.norm(vecs, axis=1)[:, None]
    return vecs


def dwa_heading_3d(pos, vel, interceptor_positions):
    """
    Sample a bunch of unit‐directions, simulate HORIZON_STEPS of motion
    in each, score by:
      + Clearance from nearest interceptor
      – Distance to goal
    Return the best unit‐direction.
    """
    best_score = -np.inf
    best_dir = vel / np.linalg.norm(vel)

    candidates = sample_headings(HEADING_SAMPLES)
    for d in candidates:
        sim_pos = pos.copy()
        score = 0.0
        for _ in range(HORIZON_STEPS):
            sim_pos += d * SPEED * DT
            # penalty for being far from goal
            score -= np.linalg.norm(GOAL - sim_pos)
            # reward for clearance
            dists = [np.linalg.norm(sim_pos - ip) for ip in interceptor_positions]
            score += min(dists)

        if score > best_score:
            best_score = score
            best_dir = d

    return best_dir


# ─── Entity Classes ────────────────────────────────────────────────────────
class Evadex3D:
    def __init__(self, start, goal):
        self.pos = np.array(start, dtype=float)
        self.goal = np.array(goal, dtype=float)
        dir0 = self.goal - self.pos
        dir0 /= np.linalg.norm(dir0)
        self.vel = dir0 * SPEED
        self.traj = [self.pos.copy()]

    def step(self, interceptors):
        ips = [ic.pos.copy() for ic in interceptors]
        new_dir = dwa_heading_3d(self.pos, self.vel, ips)
        self.vel = new_dir * SPEED
        self.pos += self.vel * DT
        self.traj.append(self.pos.copy())


class Interceptor3D:
    def __init__(self, start):
        self.pos = np.array(start, dtype=float)
        self.traj = [self.pos.copy()]

    def step(self, missile):
        diff = missile.pos - self.pos
        if np.linalg.norm(diff) > 0:
            dirv = diff / np.linalg.norm(diff)
        else:
            dirv = np.zeros(3)
        self.pos += dirv * SPEED * DT
        self.traj.append(self.pos.copy())


# ─── Setup & Animation ─────────────────────────────────────────────────────
missile = Evadex3D([0, 0, 0], GOAL)
interceptors = [Interceptor3D(p) for p in INTERCEPTOR_INITS]

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
(mis_line,) = ax.plot([], [], [], lw=2, label="Evadex")
int_lines = [
    ax.plot([], [], [], lw=1, label=f"Interceptor {i+1}")[0] for i in range(len(interceptors))
]

ax.set_xlim(0, 110)
ax.set_ylim(-30, 30)
ax.set_zlim(-30, 30)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.legend(loc="upper left")


def init():
    mis_line.set_data([], [])
    mis_line.set_3d_properties([])
    for ln in int_lines:
        ln.set_data([], [])
        ln.set_3d_properties([])
    return [mis_line] + int_lines


def update(frame):
    missile.step(interceptors)
    for ic in interceptors:
        ic.step(missile)

    mts = np.array(missile.traj)
    mis_line.set_data(mts[:, 0], mts[:, 1])
    mis_line.set_3d_properties(mts[:, 2])

    for idx, ic in enumerate(interceptors):
        its = np.array(ic.traj)
        int_lines[idx].set_data(its[:, 0], its[:, 1])
        int_lines[idx].set_3d_properties(its[:, 2])

    return [mis_line] + int_lines


ani = FuncAnimation(fig, update, frames=200, init_func=init, interval=100)
plt.show()
