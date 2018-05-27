import numpy as np

from v_rep import vrep
from v_rep.vrepConst import simx_opmode_blocking


class Sensors:
    def __init__(self, sensors, clientID):
        self.clientID = clientID
        self.sensors = []
        for name in sensors:
            _, sensor_handle = vrep.simxGetObjectHandle(clientID, name, simx_opmode_blocking)
            self.sensors.append(sensor_handle)

    def read(self):
        x = [self.read_from_sensor(sensor) for sensor in self.sensors]
        print(x)
        return min(x)

    def read_from_sensor(self, sensor):
        errorCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector \
            = vrep.simxReadProximitySensor(self.clientID, sensor, simx_opmode_blocking)
        return np.linalg.norm(detectedPoint)
