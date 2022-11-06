from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.results_plotter import load_results, ts2xy
import numpy as np
import os

class LogCallback(BaseCallback):
    def __init__(self, check_freq, save_path, verbose=1):
        super(LogCallback,self).__init__(verbose)
        self.check_freq = check_freq
        self.save_path = save_path

    def _init_callback(self):
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)
    
    def _on_step(self):
        if self.n_calls % self.check_freq == 0:
            model_path = os.path.join(self.save_path, f'thebestmodel{self.n_calls}')
            self.model.save(model_path)
        return True

log_dir = "tmp/"
os.makedirs(log_dir, exist_ok=True)
env = ParkingENV()
env = Monitor(env, log_dir)
env._max_episode_steps = 5000
model = PPO('MlpPolicy', env,verbose=1)
callback = LogCallback(check_freq=1000, save_path=log_dir)
model.learn(total_timesteps=1000000,callback=callback)
model.save("ParkingModel")