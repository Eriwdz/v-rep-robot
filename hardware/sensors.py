import numpy as np

from v_rep import vrep
from v_rep.vrepConst import simx_opmode_buffer, simx_opmode_oneshot_wait


class Sensors:
    def __init__(self, sensors, clientID):
        self.clientID = clientID
        self.sensors = []
        for name in sensors:
            _, sensor_handle = vrep.simxGetObjectHandle(clientID, name, simx_opmode_oneshot_wait)
            self.sensors.append(sensor_handle)

    def read(self):
        return min([self.read_from_sensor(sensor) for sensor in self.sensors])

    def read_from_sensor(self, sensor):
        _, _, detectedPoint, _, _ = vrep.simxReadProximitySensor(self.clientID, sensor,
                                                                 simx_opmode_buffer)
        return np.linalg.norm(detectedPoint)
