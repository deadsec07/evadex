import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# 3D Missile and Interceptor Classes
class Missile3D:
    def __init__(self, position, goal, speed=1.2):
        self.pos = np.array(position, dtype=float)
        self.goal = np.array(goal, dtype=float)
        self.speed = speed
        self.traj = [self.pos.copy()]

    def step(self, interceptors):
        # Attraction toward goal
        goal_dir = self.goal - self.pos
        if np.linalg.norm(goal_dir) > 0:
            goal_dir = goal_dir / np.linalg.norm(goal_dir)
        # Repulsion from interceptors
        rep = np.zeros(3)
        for intc in interceptors:
            diff = self.pos - intc.pos
            dist = np.linalg.norm(diff)
            if dist > 0:
                rep += diff / dist**2
        if np.linalg.norm(rep) > 0:
            rep = rep / np.linalg.norm(rep)
        # Combined direction
        dir_vec = goal_dir + rep
        if np.linalg.norm(dir_vec) > 0:
            dir_vec = dir_vec / np.linalg.norm(dir_vec)
        # Move and record
        self.pos += dir_vec * self.speed
        self.traj.append(self.pos.copy())

class Interceptor3D:
    def __init__(self, position, speed=0.8):
        self.pos = np.array(position, dtype=float)
        self.speed = speed
        self.traj = [self.pos.copy()]

    def step(self, missile):
        diff = missile.pos - self.pos
        if np.linalg.norm(diff) > 0:
            dir_vec = diff / np.linalg.norm(diff)
            self.pos += dir_vec * self.speed
        self.traj.append(self.pos.copy())

# Initialize scenario
missile = Missile3D(position=[0, 0, 0], goal=[100, 0, 0])
interceptors = [
    Interceptor3D([0, 20, 20]),
    Interceptor3D([0, -20, 20]),
    Interceptor3D([0, 20, -20])
]

# Set up 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
mis_line, = ax.plot([], [], [], lw=2, label='Missile')
int_lines = [ax.plot([], [], [], lw=1, label=f'Interceptor {i+1}')[0] 
             for i in range(len(interceptors))]

ax.set_xlim(0, 110); ax.set_ylim(-30, 30); ax.set_zlim(-30, 30)
ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
ax.legend()

# Initialization for animation
def init():
    mis_line.set_data([], []); mis_line.set_3d_properties([])
    for ln in int_lines:
        ln.set_data([], []); ln.set_3d_properties([])
    return [mis_line] + int_lines

# Update function called each frame
def update(frame):
    missile.step(interceptors)
    for ic in interceptors:
        ic.step(missile)
    traj = np.array(missile.traj)
    mis_line.set_data(traj[:,0], traj[:,1])
    mis_line.set_3d_properties(traj[:,2])
    for idx, ic in enumerate(interceptors):
        t_ic = np.array(ic.traj)
        int_lines[idx].set_data(t_ic[:,0], t_ic[:,1])
        int_lines[idx].set_3d_properties(t_ic[:,2])
    return [mis_line] + int_lines

# Launch animation
ani = FuncAnimation(fig, update, frames=200, init_func=init, interval=50, blit=False)
plt.show()
