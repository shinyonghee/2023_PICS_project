import gym
from stable_baselines3 import PPO
import os
from custom_env import CustomEnv

env = CustomEnv()
env.reset()

models_dir = "models/A2C"
model_path = f"{models_dir}/12000.zip"
model = PPO.load(model_path, env = env)
TIMESTEPS=3000

episodes=1000

vec_env = model.get_env()
obs = vec_env.reset()
print(f"initial obs:{obs}")
for ep in range(episodes):
    action, _states = model.predict(obs, deterministic=True)
    # print(action)
    obs, reward, dones, info = vec_env.step(action)
    # strFormat='%-30s%-50s[ %-30s, %-30s, %-30s]\n'
    # print(strFormat%(str(reward), str(action), str(obs[0]),str(obs[1]),str(obs[2])))
    # print(action, end='    ')
    # print(reward, end='    ')
    # print(obs)