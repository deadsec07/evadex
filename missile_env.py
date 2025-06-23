import gym
from gym import spaces
import numpy as np

class MissileEvasionEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.speed = 2
        self.max_turn = np.radians(15)
        self.reset()
        self.observation_space = spaces.Box(low=-100, high=100, shape=(5,), dtype=np.float32)
        self.action_space = spaces.Box(low=-1, high=1, shape=(1,), dtype=np.float32)

    def reset(self):
        self.m_pos = np.array([0.0, 0.0])
        self.heading = np.radians(45)
        self.i_pos = np.array([40.0, 40.0])
        return self._get_obs()

    def _get_obs(self):
        return np.array([*self.m_pos, self.heading, *self.i_pos], dtype=np.float32)

    def step(self, action):
        turn = np.clip(action[0], -1, 1) * self.max_turn
        self.heading += turn
        dx = self.speed * np.cos(self.heading)
        dy = self.speed * np.sin(self.heading)
        self.m_pos += np.array([dx, dy])

        dir_to_missile = self.m_pos - self.i_pos
        dir_to_missile /= np.linalg.norm(dir_to_missile)
        self.i_pos += dir_to_missile * (self.speed * 1.2)

        dist = np.linalg.norm(self.m_pos - self.i_pos)
        done = dist < 2 or np.any(np.abs(self.m_pos) > 100)
        reward = 1.0 if not done else -100

        return self._get_obs(), reward, done, {}

    def render(self, mode='human'):
        print(f"Missile: {self.m_pos}, Interceptor: {self.i_pos}")
