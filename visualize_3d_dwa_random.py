import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# ─── Configuration ───────────────────────────────────────────────────────────
DT = 0.5
HORIZON_STEPS = 10
HEADING_SAMPLES = 50
SPEED = 1.0

# Goal and start
GOAL = np.array([100.0, 0.0, 0.0])
START = -GOAL.copy()  # Opposite direction from goal

# Interceptors
NUM_INTERCEPTORS = 10
INTERCEPTOR_RADIUS = 30.0

# Collision and success thresholds
COLLISION_DIST = 2.0
GOAL_DIST = 2.0

# ─── Utility functions ───────────────────────────────────────────────────────
def sample_headings(n):
    vecs = np.random.normal(size=(n, 3))
    vecs /= np.linalg.norm(vecs, axis=1)[:, None]
    return vecs

def dwa_heading_3d(pos, vel, interceptor_positions):
    best_score = -np.inf
    best_dir = vel / np.linalg.norm(vel)
    candidates = sample_headings(HEADING_SAMPLES)
    for d in candidates:
        sim_pos = pos.copy()
        score = 0.0
        for _ in range(HORIZON_STEPS):
            sim_pos += d * SPEED * DT
            score -= np.linalg.norm(GOAL - sim_pos)
            dists = [np.linalg.norm(sim_pos - ip) for ip in interceptor_positions]
            score += min(dists)
        if score > best_score:
            best_score = score
            best_dir = d
    return best_dir

# ─── Entity classes ─────────────────────────────────────────────────────────
class Evadex3D:
    def __init__(self, start, goal):
        self.pos = np.array(start, dtype=float)
        self.goal = np.array(goal, dtype=float)
        dir0 = (self.goal - self.pos)
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

# ─── Initialize entities ────────────────────────────────────────────────────
missile = Evadex3D(START, GOAL)
# Place interceptors on a sphere around the goal
dirs = sample_headings(NUM_INTERCEPTORS)
interceptors = [Interceptor3D(GOAL + d * INTERCEPTOR_RADIUS) for d in dirs]

# ─── Plot setup ─────────────────────────────────────────────────────────────
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Plot goal
ax.scatter(GOAL[0], GOAL[1], GOAL[2], marker='*', color='g', s=100, label='Goal')

# Lines for trajectories
mis_line, = ax.plot([], [], [], lw=2, label='Evadex')
int_lines = [
    ax.plot([], [], [], lw=1, label=f'Interceptor {i+1}')[0]
    for i in range(NUM_INTERCEPTORS)
]

# Set axes limits and labels
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
    for ic in interceptors:
        ic.step(missile)

    # Check for collision
    for ic in interceptors:
        if np.linalg.norm(missile.pos - ic.pos) < COLLISION_DIST:
            ax.text2D(0.5, 0.5, "GAME OVER", transform=ax.transAxes,
                      color='red', fontsize=20, ha='center')
            ani.event_source.stop()
            break

    # Check if goal reached
    if np.linalg.norm(missile.pos - GOAL) < GOAL_DIST:
        ax.text2D(0.5, 0.5, "SUCCESS!", transform=ax.transAxes,
                  color='green', fontsize=20, ha='center')
        ani.event_source.stop()

    # Update lines
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
