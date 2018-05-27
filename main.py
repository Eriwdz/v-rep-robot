from pyrep import VRep

from hardware.robot import Robot
from moo_system import MooSystem

if __name__ == '__main__':
    # run
    with VRep.connect("127.0.0.1", 19997) as api:
        r = Robot(api)
        # cs = NaiveSystem(r)
        # cs = SimpleSystem(r)
        cs = MooSystem(r)
        cs.run()
