class Sensors:
    def __init__(self, api, sensors_names, val_if_not_exist=70, use_min=True):
        self.val_if_not_exist = val_if_not_exist
        self.use_min = use_min
        self.sensors = [api.sensor.proximity(i) for i in sensors_names]

    def read(self):
        x = [self.read_from_sensor(sensor) for sensor in self.sensors]
        return min(x) if self.use_min else max(x)

    def read_from_sensor(self, sensor):
        temp = sensor.read()[1].distance()
        # temp = math.sqrt(detectedPoint[0] ** 2 + detectedPoint[1] ** 2 + detectedPoint[2] ** 2)
        return self.val_if_not_exist if temp == 0 else temp
