import math

from v_rep import vrep
from v_rep.vrepConst import simx_opmode_blocking, simx_opmode_buffer


class Sensors:
    def __init__(self, sensors, clientID, val_if_not_exist, use_min=True):
        self.val_if_not_exist = val_if_not_exist
        self.clientID = clientID
        self.use_min = use_min
        self.sensors = []
        for name in sensors:
            _, sensor_handle = vrep.simxGetObjectHandle(clientID, name, simx_opmode_blocking)
            self.sensors.append(sensor_handle)

    def read(self):
        x = [self.read_from_sensor(sensor) for sensor in self.sensors]
        return min(x) if self.use_min else max(x)

    def read_from_sensor(self, sensor):
        errorCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector \
            = vrep.simxReadProximitySensor(self.clientID, sensor, simx_opmode_buffer)
        # temp = np.linalg.norm(detectedPoint)
        temp = math.sqrt(detectedPoint[0] ** 2 + detectedPoint[1] ** 2 + detectedPoint[2] ** 2)
        return self.val_if_not_exist if temp == 0 else temp
