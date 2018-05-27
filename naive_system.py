import time

from hardware.robot import Robot


class NaiveSystem:
    def __init__(self, robot: Robot):
        self.r = robot

    def run(self):
        while True:
            # update distance sensors
            left = self.r.left_length()
            right = self.r.right_length()
            print(f'Left: {left} Right: {right}')
            if 0.01 < right < 5:
                self.r.rotate_left()
            elif 0.01 < left < 5:
                self.r.rotate_right()
            else:
                self.r.move_forward()
            time.sleep(0.1)
