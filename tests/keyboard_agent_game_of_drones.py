#!/usr/bin/env python
import sys
import time
import gym

import gameofdrones
from gameofdrones.envs.utils_game_of_drones.states_drone import Actions

# --------------------------------------------------------------------
#  Human keyboard based agent, which allows the user to test dynamic
#  of the environment by keyboard inputs.
#  The Drone can be controlled by the keys [0, 1, 2, 3], which represent
#  the action space equivalents:
#     ENGINES_OFF = 0
#     RIGHT_ENGINE_ON = 1
#     LEFT_ENGINE_ON = 2
#     BOTH_ENGINES_ON = 3
#
#   With the 'spacebar' the environment can be paused
#   and with 'enter' the environment will be reseted.
# --------------------------------------------------------------------

env_name = 'GameOfDrones-v0'
env = gym.make(env_name).unwrapped
state = env.reset()
print("Starting state of the environment: ", state)

if not hasattr(env.action_space, 'n'):
  raise Exception('Keyboard agent only supports discrete action spaces')
ACTIONS = env.action_space.n
SKIP_CONTROL = 0  # Use previous control decision SKIP_CONTROL times, that's how you
# can test what skip is still usable.

human_agent_action = 0
human_wants_restart = False
human_sets_pause = False

def key_press(key, mod):
  global human_agent_action, human_wants_restart, human_sets_pause
  if key == 0xff0d:
    human_wants_restart = True
  if key == 32:
    human_sets_pause = not human_sets_pause
  a = int(key - ord('0'))
  if a <= 0 or a >= ACTIONS:
    return
  human_agent_action = a

def key_release(key, mod):
  global human_agent_action
  a = int(key - ord('0'))
  if a <= 0 or a >= ACTIONS:
    return
  if human_agent_action == a:
    human_agent_action = 0

env.render(mode='rgb_array')
env.viewer.window.on_key_press = key_press
env.viewer.window.on_key_release = key_release

def rollout(env):
  global human_agent_action, human_wants_restart, human_sets_pause
  human_wants_restart = False
  obser = env.reset()
  skip = 0
  total_reward = 0
  total_timesteps = 0
  while True:

    if not skip:
      print("taking action {}".format(Actions(human_agent_action)))
      a = human_agent_action
      total_timesteps += 1
      skip = SKIP_CONTROL
    else:
      skip -= 1

    state, reward, done, _ = env.step(Actions(a))

    if reward != 0:
      # print("reward %0.3f" % r)
      print("Resulting reward: ", reward, " ----> current state: ", state)
    total_reward += reward
    env.render()

    if done or human_wants_restart:
      break

    while human_sets_pause:
      env.render()
      time.sleep(0.1)
    time.sleep(0.1)

  print("timesteps %i reward %0.2f" % (total_timesteps, total_reward))


  return

if __name__ == "__main__":

  print("ACTIONS={}".format(ACTIONS))
  print("Press keys 1 2 3 ... to take actions 1 2 3 ...")
  print("No keys pressed is taking action 0")

  while True:
    rollout(env)
