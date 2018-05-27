import os


os.environ["VREP"] = "/home/anjd/github/V-REP_PRO_EDU_V3_5_0_Linux"
os.environ[
    "VREP_LIBRARY"] = "/home/anjd/github/V-REP_PRO_EDU_V3_5_0_Linux/programming/remoteApiBindings/lib/lib/Linux/64Bit/"


from pyrep import VRep

from hardware.robot import Robot
from moo_system import MooSystem
from naive_system import NaiveSystem
from simple_system import SimpleSystem

if __name__ == '__main__':
    # run
    with VRep.connect("127.0.0.1", 19997) as api:
        r = Robot(api)
        # cs = NaiveSystem(r)
        # cs = SimpleSystem(r)
        cs = MooSystem(r)
        cs.run()
