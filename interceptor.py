import numpy as np

class Interceptor:
    def __init__(self, x, y, speed):
        self.position = np.array([x, y], dtype=np.float32)
        self.speed = speed
        self.trajectory = [self.position.copy()]

    def pursue(self, target_position):
        direction = target_position - self.position
        direction /= np.linalg.norm(direction)
        self.position += direction * self.speed
        self.trajectory.append(self.position.copy())

    def get_position(self):
        return self.position
