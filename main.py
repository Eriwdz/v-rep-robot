import sys

from v_rep import vrep
from hardware.robot import Robot

vrep.simxFinish(-1)

# simRemoteApi.start(19999)
clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if clientID != -1:
    print('Connected to remote API server')

else:
    sys.exit('Could not connect')

if __name__ == '__main__':
    robot = Robot(clientID)
    robot.run()
