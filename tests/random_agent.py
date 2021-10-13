#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#%% Imports
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import time
import numpy as np

import gameofdrones
import gym

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# %% Environment Creation
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

env_name = 'GameOfDrones-v0'

# unwrapped to get rid of this TimeLimitWrapper, which might reset the environment twice and thus breaks ergodicity
env = gym.make(env_name).unwrapped

print("state space", env.observation_space)
print("action space", env.action_space)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# %% Let it run
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

state = env.reset()

counter = 0
time_start = time.time()

#while True:
for i in range(500):
  env.render(mode="human")

  action = env.action_space.sample()

  state, reward, done, _ = env.step(action)

  print(reward)

  # For very fast running environments ...
  time.sleep(0.02)

  if done:
    print("Resetting")
    env.reset()
  #end
#end

env.close()

print("time consumed", time.time() - time_start)
