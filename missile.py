# missile.py

import numpy as np
import math

class Missile:
    def __init__(self, x, y, speed, heading_deg, max_turn_deg_per_step=25):
        self.position = np.array([x, y], dtype=float)
        self.speed = speed
        self.heading = math.radians(heading_deg)
        self.max_turn = math.radians(max_turn_deg_per_step)
        self.trajectory = [self.position.copy()]

        # --- thrust state ---
        self._thrust_vec = np.zeros(2, dtype=float)
        self._thrust_timer = 0
        self._thrust_cooldown = 0

    def apply_thrust(self, direction_vec, magnitude, duration, cooldown):
        """
        direction_vec: unit vector giving thrust direction
        magnitude: scalar thrust speed added
        duration: how many steps this thrust lasts
        cooldown: steps before you can thrust again
        """
        if self._thrust_cooldown == 0:
            self._thrust_vec = direction_vec * magnitude
            self._thrust_timer = duration
            self._thrust_cooldown = cooldown

    def move(self):
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

    def update_heading(self, new_heading):
        diff = new_heading - self.heading
        diff = math.atan2(math.sin(diff), math.cos(diff))
        diff = np.clip(diff, -self.max_turn, self.max_turn)
        self.heading += diff

    def get_position(self):
        return self.position.copy()
