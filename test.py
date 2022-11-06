from stable_baselines3 import PPO
from env import ParkingENV

model = PPO.load("trained")
env = ParkingENV()
obs = env.reset()

for i in range(10000):
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action)
    env.render()
