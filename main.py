import time

from pyrep import VRep

from hardware.robot import Robot

if __name__ == '__main__':

    with VRep.connect("127.0.0.1", 19997) as api:
        r = Robot(api)
        while True:
            dl = r.left_length()
            df = r.front_length()
            dr = r.right_length()
            pos = r.get_position()
            theta = r.get_orientation().get_gamma()
            print(f'dl = {dl} df = {df} dr = {dr} pos = {pos} theta= {theta}')

            if 0.01 < dl < 1:
                print('rotating left')
                r.rotate_left()
            elif 0.01 < dr < 1:
                print('rotating left')
                r.rotate_right()
            else:
                print('forward')
                r.move_forward()
            time.sleep(0.1)
