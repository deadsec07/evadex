import numpy as np
import math


class Missile:
    def __init__(self, x: float, y: float, speed: float, heading_deg: float,
                 max_turn_deg_per_step: float = 25) -> None:
        self.position = np.array([x, y], dtype=float)
        self.speed = float(speed)
        self.heading = math.radians(heading_deg)
        self.max_turn = math.radians(max_turn_deg_per_step)
        self.trajectory: list[np.ndarray] = [self.position.copy()]

        # thrust state
        self._thrust_vec = np.zeros(2, dtype=float)
        self._thrust_timer = 0
        self._thrust_cooldown = 0

    def apply_thrust(self, direction_vec: np.ndarray, magnitude: float,
                     duration: int, cooldown: int) -> None:
        """Apply a short burst of thrust if cooldown allows."""
        if self._thrust_cooldown == 0:
            self._thrust_vec = direction_vec * float(magnitude)
            self._thrust_timer = int(duration)
            self._thrust_cooldown = int(cooldown)

    def move(self) -> None:
        # baseline velocity
        vx = math.cos(self.heading) * self.speed
        vy = math.sin(self.heading) * self.speed
        vel = np.array([vx, vy], dtype=float)

        # add thrust if active
        if self._thrust_timer > 0:
            vel += self._thrust_vec
            self._thrust_timer -= 1
        else:
            # clear thrust when expired
            self._thrust_vec[:] = 0.0

        # update position
        self.position += vel
        self.trajectory.append(self.position.copy())

        # handle cooldown
        if self._thrust_cooldown > 0:
            self._thrust_cooldown -= 1

    def update_heading(self, new_heading: float) -> None:
        diff = new_heading - self.heading
        diff = math.atan2(math.sin(diff), math.cos(diff))
        diff = np.clip(diff, -self.max_turn, self.max_turn)
        self.heading += diff

    def get_position(self) -> np.ndarray:
        return self.position.copy()
