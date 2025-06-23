import numpy as np

class EvasionRLAgent:
    def decide_heading(self, obs):
        return obs[2] + (np.random.rand() - 0.5) * 0.5  # placeholder
