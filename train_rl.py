# Add this in a new file called `train_rl.py`
from stable_baselines3 import PPO
from missile_env import MissileEvasionEnv

env = MissileEvasionEnv()
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100_000)
model.save("ppo_evader")
