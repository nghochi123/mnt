import serial
import time
import math
import numpy as np

from constants.delta import *
from constants.limits import S_MAX, S_MIN
from constants.screws import screwtypes


def ensure_radius(x, y):
    if math.sqrt(x * x + y * y) <= RADIUS:
        return True
    else:
        return False


def cartesian_to_polar(x, y):
    r = math.sqrt(x * x + y * y)
    theta = np.arctan2(y, x)
    return r, theta


def polar_to_cartesian(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


class DeltaController():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 345
        self.step = STEP
        self.servos = {
            S_SPINNER: 0,
            S_GRIPPER: G_CLOSE
        }
        self.serial = serial.Serial(
            port=PORT, baudrate=BAUDRATE, timeout=TIMEOUT)

        time.sleep(2)

    # Send a serial command
    def command(self, command):
        self.serial.write(str.encode(command))
        time.sleep(0.1)

        while True:
            line = self.serial.readline()
            if line == b'ok\n':
                break

    # Home
    def home(self):
        self.x = 0
        self.y = 0
        self.z = Z_HOME
        self.command('G28\r\n')
        self.spin_to_angle(np.pi / 2)
        self.close_grip()

    # MOTION CONTROLS

    def allow_vision(self):
        self.x = 0
        self.y = VISION_Y
        self.z = VISION_Z
        self.move(self.x, self.y, self.z)

    def move(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        if ensure_radius(x, y):
            self.command(
                f'G0 X{self.x:.6f} Y{self.y:.6f} Z{self.z:.6f} F{STEP}\r\n')
        else:
            print('Coordinates off circle!')

    def move_to_rect(self, coords):
        yco = [2.933E-10, -1.374E-08, -2.025E-06, 0.0009975, 0.003818, 76.54]
        xco = [-2.168E-8, 3.166E-07, 0.001091, 0.000957, 76.46]
        z_correct = np.poly1d(yco)(coords[0])+np.poly1d(xco)(coords[1])-76.5

        self.open_grip()
        self.move(coords[0], coords[1]-43, z_correct)
        self.close_grip()
        self.hover_upwards()

    def hover_upwards(self):
        self.move(self.x, self.y, HOVER)

    # Arc movement to output location

    def move_to_output(self, output_angle):
        _, theta = cartesian_to_polar(self.x, self.y)
        for angle in np.linspace(theta, output_angle, ARC_STEPS):
            x, y = polar_to_cartesian(RADIUS - 20, angle)
            self.move(x, y, self.z)

    # SERVO CONTROLS

    def rotate_servo(self, servo, angle):
        assert angle < 200
        self.servos[servo] = angle
        self.command(f'M280 {servo} S{angle}\r\n')

    # Spinner

    def spin_to_angle(self, angle):  # ANGLE IS IN RADIANS
        s_range = S_MAX - S_MIN
        fr = angle / np.pi
        self.rotate_servo(S_SPINNER, 180 - ((fr * s_range) + S_MIN))

    # Gripper

    def open_grip(self, diff=False):
        if diff:
            self.rotate_servo(S_GRIPPER, G_OPEN2)
        else:
            self.rotate_servo(S_GRIPPER, G_OPEN)

    def close_grip(self):
        self.rotate_servo(S_GRIPPER, G_CLOSE)

    # move to different specific locations
    def move_to_place(self, stype, num):
        self.spin_to_angle(np.pi/2)
        self.open_grip()
        for s in screwtypes[stype[0]-2]:
            if stype[1] == s[1]:
                self.move(s[num+3][0], s[num+3][1], s[num+3][2])
                break
        time.sleep(1)
        self.close_grip()

    def ramp(self):
        self.move(-20, 0, 170)
        self.move(0, -115, 200)
        time.sleep(1)
        self.open_grip()

    # Turntable

    def allow_turntable_movement(self):
        self.command(f'M302 S0\r\n')

    def move_turntable(self, angle):
        assert angle < 360 and angle >= 0
        self.command(f'G0 E{angle}\r\n')

    def home_turntable(self):
        self.move_turntable(0)

    # END CONNECTION

    def end_connection(self):
        time.sleep(2)
        self.serial.close()
