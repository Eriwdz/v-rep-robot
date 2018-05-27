import math
import time

from fuzzy_system.simple_fuzzy_system import SimpleFuzzySystem
from hardware.sensors import Sensors
from v_rep import vrep
from v_rep.vrepConst import simx_opmode_oneshot_wait, simx_opmode_streaming

PI = math.pi


class Robot:
    def __init__(self, clientID):
        self.clientID = clientID
        self.time_step = 0.2
        self.fuzzy_system = SimpleFuzzySystem()
        _, self.left_motor_handle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor',
                                                             simx_opmode_oneshot_wait)
        _, self.right_motor_handle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor',
                                                              simx_opmode_oneshot_wait)
        self.front_sensors = Sensors(["Pioneer_p3dx_ultrasonicSensor8", "Pioneer_p3dx_ultrasonicSensor9"], clientID)
        self.left_sensors = Sensors(
            ["Pioneer_p3dx_ultrasonicSensor5", "Pioneer_p3dx_ultrasonicSensor6", "Pioneer_p3dx_ultrasonicSensor7"],
            clientID)
        self.right_sensors = Sensors(
            ["Pioneer_p3dx_ultrasonicSensor10", "Pioneer_p3dx_ultrasonicSensor11", "Pioneer_p3dx_ultrasonicSensor12"],
            clientID)

    def run(self):
        t = time.time()
        while (time.time() - t) < 60:
            front = self.front_sensors.read()
            left = self.left_sensors.read()
            right = self.right_sensors.read()
            print(f"front:{front}")
            print(f"left:{left}")
            print(f"right:{right}")
            values = {
                "front": front,
                "left": left,
                "right": right
            }
            v, theta = self.fuzzy_system.run(values)
            w = theta * self.time_step
            vrep.simxSetJointTargetVelocity(self.clientID, self.left_motor_handle, v, simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID, self.right_motor_handle, w, simx_opmode_streaming)
            time.sleep(0.2)
