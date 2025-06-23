import numpy as np

class Missile:
    def __init__(self, x, y, speed, heading_deg, max_turn_deg_per_step=25):
        self.position = np.array([x, y], dtype=np.float32)
        self.speed = speed
        self.heading = np.radians(heading_deg)
        self.trajectory = [self.position.copy()]
        self.max_turn = np.radians(max_turn_deg_per_step)

    def move(self):
        dx = self.speed * np.cos(self.heading)
        dy = self.speed * np.sin(self.heading)
        self.position += np.array([dx, dy])
        self.trajectory.append(self.position.copy())

    def update_heading(self, new_heading):
        diff = new_heading - self.heading
        diff = np.arctan2(np.sin(diff), np.cos(diff))  # normalize
        diff = np.clip(diff, -self.max_turn, self.max_turn)
        self.heading += diff

    def get_position(self):
        return self.position
