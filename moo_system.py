import time
from math import hypot

from fuzzy_system.simple_fuzzy_system import SimpleFuzzySystem
from hardware.robot import Robot


class MooSystem:
    def __init__(self, robot: Robot, destination=None):
        self.fuzzy_system = SimpleFuzzySystem()
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

    def run(self):
        u, w = 0, 0
        while self._distance(self.r_destination, self.pos) > self.goal_threshold:
            # update distance sensors
            left = self.r.left_length()
            front = self.r.front_length()
            right = self.r.right_length()

            # Map Values
            front = min(max(front * 100, 0), 70)
            left = min(max(left * 100, 0), 70)
            right = min(max(right * 100, 0), 70)
            self.pos = self.r.get_position()

            values = {
                "dl": left,
                "df": front,
                "dr": right,
                "alpha": 0,
                "p": 0,
                "ed": 0
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
            time.sleep(0.1)
