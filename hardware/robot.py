import math
import time

from fuzzy_system.simple_fuzzy_system import SimpleFuzzySystem
from hardware.sensors import Sensors
from v_rep import vrep
from v_rep.vrepConst import simx_opmode_oneshot_wait, simx_opmode_streaming, simx_opmode_blocking

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

        self.left_sensors = Sensors(
            ["Pioneer_p3dx_ultrasonicSensor1", "Pioneer_p3dx_ultrasonicSensor2", "Pioneer_p3dx_ultrasonicSensor3"],
            clientID,
            self.fuzzy_system.max_distance)
        self.front_sensors = Sensors(["Pioneer_p3dx_ultrasonicSensor4", "Pioneer_p3dx_ultrasonicSensor5"], clientID,
                                     self.fuzzy_system.max_distance)
        self.right_sensors = Sensors(
            ["Pioneer_p3dx_ultrasonicSensor6", "Pioneer_p3dx_ultrasonicSensor7", "Pioneer_p3dx_ultrasonicSensor8"],
            clientID,
            self.fuzzy_system.max_distance)
        _, self.robot_handle = vrep.simxGetObjectHandle(self.clientID, "Pioneer_p3dx", simx_opmode_blocking)

    def move(self, v, w):
        vl = 5
        vr = 6
        vrep.simxSetJointTargetVelocity(self.clientID, self.left_motor_handle, vl, simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(self.clientID, self.right_motor_handle, vr, simx_opmode_streaming)

    def getPosOrient(self):
        code, pos = vrep.simxGetObjectPosition(self.clientID, self.robot_handle, -1, simx_opmode_blocking)
        code, orient = vrep.simxGetObjectOrientation(self.clientID, self.robot_handle, -1, simx_opmode_blocking)
        return pos, orient

    def run(self):
        t = time.time()
        while (time.time() - t) < 60:
            # pos, orient = self.getPosOrient()
            # print(pos)
            # print(math.degrees(orient[2]))
            front = self.front_sensors.read()
            left = self.left_sensors.read()
            right = self.right_sensors.read()
            print(f"front:{front}")
            print(f"left:{left}")
            print(f"right:{right}")
            # values = {
            #     "front": front * 100,
            #     "left": left * 100,
            #     "right": right * 100
            # }
            # v, theta = self.fuzzy_system.run(values)
            # theta = math.radians(theta)
            # v /= 10
            # w = theta / self.time_step
            # print(f"v:{v}")
            # print(f"theta:{theta}")
            # self.move(v, w)
            time.sleep(0.2)
