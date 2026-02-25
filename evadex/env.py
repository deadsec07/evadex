import gym
import numpy as np
from gym import spaces


class MissileEvasionEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.speed = 2.0
        self.max_turn = np.radians(15)
        self.observation_space = spaces.Box(
            low=-100, high=100, shape=(5,), dtype=np.float32
        )
        self.action_space = spaces.Box(low=-1, high=1, shape=(1,), dtype=np.float32)
        self.reset()

    def reset(self):  # type: ignore[override]
        self.m_pos = np.array([0.0, 0.0])
        self.heading = np.radians(45.0)
        self.i_pos = np.array([40.0, 40.0])
        return self._get_obs()

    def _get_obs(self):
        return np.array([*self.m_pos, self.heading, *self.i_pos], dtype=np.float32)

    def step(self, action):  # type: ignore[override]
        turn = np.clip(float(action[0]), -1, 1) * self.max_turn
        self.heading += turn
        dx = self.speed * np.cos(self.heading)
        dy = self.speed * np.sin(self.heading)
        self.m_pos += np.array([dx, dy])

        dir_to_missile = self.m_pos - self.i_pos
        dir_norm = np.linalg.norm(dir_to_missile)
        if dir_norm > 1e-8:
            dir_to_missile /= dir_norm
        self.i_pos += dir_to_missile * (self.speed * 1.2)

        dist = np.linalg.norm(self.m_pos - self.i_pos)
        done = bool(dist < 2 or np.any(np.abs(self.m_pos) > 100))
        reward = 1.0 if not done else -100.0

        return self._get_obs(), float(reward), done, {}

    def render(self, mode="human"):
        print(f"Missile: {self.m_pos}, Interceptor: {self.i_pos}")
