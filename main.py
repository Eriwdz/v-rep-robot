from math import hypot

from pyrep import VRep

from fuzzy_system.moo_fuzzy_system import MooFuzzySystem
from fuzzy_system.simple_fuzzy_system import SimpleFuzzySystem
from hardware.robot import Robot

x_d, y_d, theta_d = 0, 0, 0


def distance(destination, position):
    return hypot(destination['x'] - position['x'], destination['y'] - position['y'])


if __name__ == '__main__':
    method = "simple"
    fuzzy_system = SimpleFuzzySystem()
    if method == "moo":
        fuzzy_system = MooFuzzySystem(True)

    r_destination = {
        'x': 5,
        'y': 5,
        'theta': 0,
    }

    # initialize
    goal_threshold = 0.5
    velocity = 0
    # run
    with VRep.connect("127.0.0.1", 19997) as api:
        r = Robot(api)
        r.stop_motors()
        pos = r.get_position()
        while distance(r_destination, pos) > goal_threshold:
            # update distance sensors
            left = r.left_length()
            front = r.front_length()
            right = r.right_length()

            front = min(max(front * 100, 0), 70)
            left = min(max(left * 100, 0), 70)
            right = min(max(right * 100, 0), 70)

            pos = r.get_position()
            values = {
                "left": left,
                "front": front,
                "right": right,
                "velocity": velocity
            }
            print(values)
            velocity, angle = fuzzy_system.run(values)

            if angle is not None and angle != 0 and abs(angle) > 25:
                print('LR angle')
                if angle > 0:
                    r.rotate_left()
                elif angle < 0:
                    r.rotate_right()
                continue
            if velocity is not None and velocity != 0:
                r.move_forward()
