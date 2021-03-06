import time
import numpy as np
from .world_settings import *
from .states_drone import States, Actions


class PID:
    """PID controller from https://github.com/korfuri/PIDController."""
    def __init__(self, kp: float, ki: float, kd: float, origin_time=None):
        if origin_time is None:
            origin_time = time.time()

        # Gains for each term
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd

        # Corrections (outputs)
        self.Cp = 0.0
        self.Ci = 0.0
        self.Cd = 0.0

        self.previous_time = origin_time
        self.previous_error_angle = 0.0
        self.previous_error_y = 0.0

        # Init target parameter to hold for the PID controller
        self.target_y = 0.0
        self.target_angle = 0.0

    def set_target_position(self, target_pos):
        """
        Setting the drone target position for the PID controller.
        :param target_pos: Position of the drone
        """
        self.target_y = np.abs(target_pos.y).copy() * H

    def update_targets(self, state: States):
        """
        Setting the drone target position for the PID controller.
        :param target_pos: Position of the drone
        """
        self.target_y = state.drone_position.y * H
        self.target_angle = state.distance_vector.optimal_heading * (np.pi * 2)

    def pid_control(self, state: States, current_time=None):
        """
        PID controller for stabilizing the drone in the air, the code structure was inspired by the heuristic function
        of the lunar lander from OpenAi Gym.
        Parameters
        ----------
        state: Current state space values of the environment. The state space contains every necessary drone property for
                the PID controller equations. Like: the position of the drone, the velocity of the drone, angle +
                angle velocity.

        kp, kd, ki: PID controller parameters to weight the influence of the proportional component or integral component to
                the result of the function.

        Returns
        -------
            Suggested Action to hold the drone stable from the PID controller.

        """
        if current_time is None:
            current_time = time.time()

        self.target_angle = 0
        target_angle_vel = 0  # drone should be stable in the air

        # Drone position should be stable
        # target_y = np.abs(state.drone_position.y)
        target_vel = 0

        angle_error = (self.target_angle - (state.angle * np.pi * 2))
        position_error = (self.target_y - (state.drone_position.y * H))

        dt = (current_time - self.previous_time)
        if dt <= 0.0:
            return 0
        de_angle = angle_error - self.previous_error_angle
        de_position = position_error - self.previous_error_y

        # PD control for angle:
        angle_PID = angle_error * self.Kp + (target_angle_vel - state.angle_vel) * self.Kd + (de_angle / dt) * self.Ki

        # PD control for descent:
        y_PID = position_error * self.Kp + (target_vel - state.velocity.y) * self.Kd + (de_position / dt) * self.Ki

        # Selecting action from action_space
        if abs(y_PID) > abs(angle_PID) and y_PID > 0.01:
            return Actions.BOTH_ENGINES_ON
        elif angle_PID < -0.02:
            return Actions.LEFT_ENGINE_ON
        elif angle_PID > +0.02:
            return Actions.RIGHT_ENGINE_ON
        return Actions.ENGINES_OFF
