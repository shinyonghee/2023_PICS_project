import gym
from stable_baselines3 import A2C
import os
import time
from custom_env import CustomEnv
import warnings
warnings.filterwarnings(action='ignore')
models_dir = "models/A2C"
logdir=f"logs/A2C-{int(time.time())}"
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)    
env = CustomEnv()
env.reset()

model= A2C("MlpPolicy", env, verbose=1,tensorboard_log=logdir)

TIMESTEPS=1000

for i in range(50):
    model.learn(total_timesteps=TIMESTEPS, progress_bar=True, reset_num_timesteps=False, tb_log_name="A2C")
    model.save(f"{models_dir}/{TIMESTEPS*(i+1)}")

episodes=10

# for ep in range(episodes):
#     obs = env.reset()
#     done = False
#     while not done:
#         action, _states = model.predict(obs, deterministic=True)
#         obs, rewards, dones, info = env.step(action)
#         print(rewards)
