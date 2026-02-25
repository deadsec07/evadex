from stable_baselines3 import PPO
from evadex.env import MissileEvasionEnv


def main() -> None:
    env = MissileEvasionEnv()
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=100_000)
    model.save("ppo_evader")


if __name__ == "__main__":
    main()
