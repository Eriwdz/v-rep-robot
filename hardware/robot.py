from pyrep import VRep

from hardware.sensors import Sensors


class Robot:

    def __init__(self, api: VRep):
        self._api = api
        self._left_motor = api.joint.with_velocity_control("Pioneer_p3dx_leftMotor")
        self._right_motor = api.joint.with_velocity_control("Pioneer_p3dx_rightMotor")
        self.position_sensor = api.sensor.position('Pioneer_p3dx')
        self.orientation_sensor = api.sensor.position('Pioneer_p3dx')
        self._left_sensors = Sensors(api, ["Pioneer_p3dx_ultrasonicSensor1",
                                           "Pioneer_p3dx_ultrasonicSensor2",
                                           "Pioneer_p3dx_ultrasonicSensor3",
                                           ])
        self._front_sensors = Sensors(api, ["Pioneer_p3dx_ultrasonicSensor4",
                                            "Pioneer_p3dx_ultrasonicSensor5",
                                            ])
        self._right_sensors = Sensors(api, ["Pioneer_p3dx_ultrasonicSensor6",
                                            "Pioneer_p3dx_ultrasonicSensor7",
                                            "Pioneer_p3dx_ultrasonicSensor8",
                                            ])

    def rotate_right(self, speed=2.0):
        self._set_two_motor(speed, -speed)

    def rotate_left(self, speed=2.0):
        self._set_two_motor(-speed, speed)

    def move_forward(self, speed=2.0):
        self._set_two_motor(speed, speed)

    def move_backward(self, speed=2.0):
        self._set_two_motor(-speed, -speed)

    def stop_motors(self):
        self._set_two_motor(0, 0)

    def _set_two_motor(self, left: float, right: float):
        self._left_motor.set_target_velocity(left)
        self._right_motor.set_target_velocity(right)

    def right_length(self):
        return self._right_sensors.read()

    def left_length(self):
        return self._left_sensors.read()

    def front_length(self):
        return self._front_sensors.read()

    # x , y , theta
    def get_position(self):
        position = self.position_sensor.get_position()
        orientation = self.orientation_sensor.get_orientation()
        return {
            'x': position.get_x(),
            'y': position.get_y(),
            'theta': orientation.get_gamma(),
        }

    def get_orientation(self):
        orientation = self.orientation_sensor.get_orientation()
        return orientation
