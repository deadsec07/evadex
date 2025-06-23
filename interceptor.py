# interceptor.py

import numpy as np

class Interceptor:
    def __init__(self, x, y, speed):
        self.position = np.array([x, y], dtype=float)
        self.speed = speed
        self.trajectory = [self.position.copy()]

    def pursue(self, target_position):
        dir_vec = target_position - self.position
        dist = np.linalg.norm(dir_vec)
        if dist > 1e-6:
            self.position += (dir_vec / dist) * self.speed
        self.trajectory.append(self.position.copy())

    def get_position(self):
        return self.position.copy()
