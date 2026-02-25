import numpy as np


class Interceptor:
    def __init__(self, x: float, y: float, speed: float) -> None:
        self.position = np.array([x, y], dtype=float)
        self.speed = float(speed)
        self.trajectory: list[np.ndarray] = [self.position.copy()]

    def pursue(self, target_position: np.ndarray) -> None:
        dir_vec = target_position - self.position
        dist = np.linalg.norm(dir_vec)
        if dist > 1e-6:
            self.position += (dir_vec / dist) * self.speed
        self.trajectory.append(self.position.copy())

    def get_position(self) -> np.ndarray:
        return self.position.copy()
