import gym
from gym.envs.registration import register

register(id='GameOfDrones-v0',
         entry_point='gameofdrones.envs.game_of_drones:GameOfDrone')

