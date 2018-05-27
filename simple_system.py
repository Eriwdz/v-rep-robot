import time

from fuzzy_system.simple_fuzzy_system import SimpleFuzzySystem
from hardware.robot import Robot


class SimpleSystem:
    def __init__(self, robot: Robot):
        self.fuzzy_system = SimpleFuzzySystem()
        self.r = robot

    def run(self):
        velocity = 0

        while True:
            # update distance sensors
            left = self.r.left_length()
            front = self.r.front_length()
            right = self.r.right_length()

            # Map Values
            front = min(max(front * 100, 0), 70)
            left = min(max(left * 100, 0), 70)
            right = min(max(right * 100, 0), 70)

            values = {
                "left": left,
                "front": front,
                "right": right,
                "velocity": velocity
            }
            print(values)
            velocity, angle = self.fuzzy_system.run(values)

            if angle is not None and angle != 0 and abs(angle) > 25:
                print('LR angle')
                if angle > 0:
                    self.r.rotate_left()
                elif angle < 0:
                    self.r.rotate_right()
                continue
            if velocity is not None and velocity != 0:
                self.r.move_forward()
            time.sleep(0.1)
