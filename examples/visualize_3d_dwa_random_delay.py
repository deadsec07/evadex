# visualize_3d_dwa_random_delay.py

import random

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

# ─── Configuration ───────────────────────────────────────────────────────────
DT                = 0.5
HORIZON_STEPS     = 10
HEADING_SAMPLES   = 50
SPEED             = 1.0

GOAL              = np.array([100.0, 0.0, 0.0])
START             = -GOAL.copy()               # Opposite direction start

NUM_INTERCEPTORS  = 10
INTERCEPTOR_RADIUS= 30.0
MAX_LAUNCH_DELAY  = 100    # in frames

COLLISION_DIST    = 2.0
GOAL_DIST         = 2.0

# ─── DWA‐style heading sampler ───────────────────────────────────────────────
def sample_headings(n):
    vecs = np.random.normal(size=(n, 3))
    vecs /= np.linalg.norm(vecs, axis=1)[:, None]
    return vecs

def dwa_heading_3d(pos, vel, interceptor_positions):
    best_score = -np.inf
    best_dir   = vel / np.linalg.norm(vel)
    for d in sample_headings(HEADING_SAMPLES):
        sim_pos = pos.copy()
        score   = 0.0
        for _ in range(HORIZON_STEPS):
            sim_pos += d * SPEED * DT
            score  -= np.linalg.norm(GOAL - sim_pos)
            dists   = [np.linalg.norm(sim_pos - ip) for ip in interceptor_positions]
            score  += min(dists)
        if score > best_score:
            best_score = score
            best_dir   = d
    return best_dir

# ─── Entity classes ─────────────────────────────────────────────────────────
class Evadex3D:
    def __init__(self, start, goal):
        self.pos  = np.array(start, dtype=float)
        self.goal = np.array(goal, dtype=float)
        dir0      = (self.goal - self.pos)
        dir0     /= np.linalg.norm(dir0)
        self.vel  = dir0 * SPEED
        self.traj = [self.pos.copy()]

    def step(self, interceptors):
        ips       = [ic.pos.copy() for ic in interceptors]
        new_dir   = dwa_heading_3d(self.pos, self.vel, ips)
        self.vel  = new_dir * SPEED
        self.pos += self.vel * DT
        self.traj.append(self.pos.copy())

class Interceptor3D:
    def __init__(self, start, launch_frame):
        self.pos          = np.array(start, dtype=float)
        self.launch_frame = launch_frame
        self.traj         = [self.pos.copy()]

    def step(self, missile, frame):
        if frame < self.launch_frame:
            # not yet launched: stay in place
            self.traj.append(self.pos.copy())
            return
        # chase once launched
        diff = missile.pos - self.pos
        if np.linalg.norm(diff) > 0:
            dirv = diff / np.linalg.norm(diff)
        else:
            dirv = np.zeros(3)
        self.pos += dirv * SPEED * DT
        self.traj.append(self.pos.copy())

# ─── Initialize entities ────────────────────────────────────────────────────
missile = Evadex3D(START, GOAL)

# sample interceptor spawn directions & launch times
dirs        = np.random.normal(size=(NUM_INTERCEPTORS, 3))
dirs       /= np.linalg.norm(dirs, axis=1)[:, None]
interceptors = []
for d in dirs:
    start_pt     = GOAL + d * INTERCEPTOR_RADIUS
    launch_frame = random.randint(0, MAX_LAUNCH_DELAY)
    interceptors.append(Interceptor3D(start_pt, launch_frame))

# ─── Plot setup ─────────────────────────────────────────────────────────────
fig = plt.figure()
ax  = fig.add_subplot(111, projection='3d')
# draw goal as green star
ax.scatter(*GOAL, marker='*', color='g', s=100, label='Goal')

mis_line,   = ax.plot([], [], [], lw=2, label='Evadex')
int_lines   = [ax.plot([], [], [], lw=1, label=f'Interceptor {i+1}')[0]
               for i in range(NUM_INTERCEPTORS)]

lim = INTERCEPTOR_RADIUS + np.linalg.norm(GOAL) + 10
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_zlim(-lim, lim)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend(loc='upper left')

# ─── Animation callbacks ────────────────────────────────────────────────────
def init():
    mis_line.set_data([], [])
    mis_line.set_3d_properties([])
    for ln in int_lines:
        ln.set_data([], [])
        ln.set_3d_properties([])
    return [mis_line] + int_lines

def update(frame):
    missile.step(interceptors)
    for idx, ic in enumerate(interceptors):
        ic.step(missile, frame)

    # collision check
    for ic in interceptors:
        if np.linalg.norm(missile.pos - ic.pos) < COLLISION_DIST:
            ax.text2D(0.5, 0.5, "GAME OVER", transform=ax.transAxes,
                      color='red', fontsize=20, ha='center')
            ani.event_source.stop()
            break

    # goal check
    if np.linalg.norm(missile.pos - GOAL) < GOAL_DIST:
        ax.text2D(0.5, 0.5, "SUCCESS!", transform=ax.transAxes,
                  color='green', fontsize=20, ha='center')
        ani.event_source.stop()

    # update trajectory lines
    mts = np.array(missile.traj)
    mis_line.set_data(mts[:,0], mts[:,1])
    mis_line.set_3d_properties(mts[:,2])
    for idx, ic in enumerate(interceptors):
        its = np.array(ic.traj)
        int_lines[idx].set_data(its[:,0], its[:,1])
        int_lines[idx].set_3d_properties(its[:,2])

    return [mis_line] + int_lines

# ─── Run animation ─────────────────────────────────────────────────────────
ani = FuncAnimation(fig, update, frames=500, init_func=init, interval=100)
plt.show()
