import time
from math import hypot, atan2, pi

from fuzzy_system.moo_fuzzy_system import MooFuzzySystem
from hardware.robot import Robot


class MooSystem:
    def __init__(self, robot: Robot, use_lex=True, destination=None):
        self.fuzzy_system = MooFuzzySystem(use_lex=use_lex)
        self.r_destination = {
            'x': 5,
            'y': 5,
            'theta': 0,
        } if destination is None else destination

        # initialize
        self.goal_threshold = 0.5
        self.r = robot
        self.pos = robot.get_position()

    @staticmethod
    def _distance(destination, position):
        return hypot(destination['x'] - position['x'], destination['y'] - position['y'])

    @staticmethod
    def _get_alpha(destination, position):
        a = atan2(destination['y'] - position['y'], destination['x'] - position['x']) - position['theta']
        return ((-a + pi) % (2.0 * pi) - pi) * -1.0

    def run(self):
        p = 0
        self.pos = self.r.get_position()
        self.r.stop_motors()
        while self._distance(self.r_destination, self.pos) > self.goal_threshold:
            # update distance sensors
            left = self.r.left_length()
            front = self.r.front_length()
            right = self.r.right_length()

            # Map Values
            front = min(max(front, 0), 4)
            left = min(max(left, 0), 4)
            right = min(max(right, 0), 4)

            alpha = self._get_alpha(self.r_destination, self.pos)
            p_current = self._distance(self.r_destination, self.pos)
            ed = p_current - p
            p = p_current
            values = {
                "dl": left,
                "df": front,
                "dr": right,
                "alpha": alpha,
                "p": p,
                "ed": ed
            }
            print(values)
            u, w = self.fuzzy_system.run(values)

            if w is not None and w != 0 and abs(w) > 25:
                print('LR angle')
                if w > 0:
                    self.r.rotate_left()
                elif w < 0:
                    self.r.rotate_right()
                continue
            if u is not None and u != 0:
                self.r.move_forward()
            self.r.stop_motors()
            time.sleep(0.2)
            self.pos = self.r.get_position()
