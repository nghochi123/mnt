import serial
import time
import math
import numpy as np

from constants.delta import *
from constants.limits import S_MAX, S_MIN

# Make sure radius does not exceed maximum radius


def ensure_radius(x, y):
    if math.sqrt(x * x + y * y) <= RADIUS:
        return True
    else:
        return False

# Convert cartesian coordinates to polar coordinates


def cartesian_to_polar(x, y):
    r = math.sqrt(x * x + y * y)
    theta = np.arctan2(y, x)
    return r, theta

# Convert polar coordinates to cartesian coordinates


def polar_to_cartesian(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


class DeltaController():
    # Set up the initial variables for the delta controller class. When you create an object with the class, it will come with these predetermined variables.
    # You can find most of the variables in the constants folder, and set it there.
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

    # Send a serial command (Gcode) You can learn more about Gcode here: https://reprap.org/wiki/G-code
    def command(self, command):
        self.serial.write(str.encode(command))
        time.sleep(1)

    # Home the machine
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
        self.command(
            f'G0 X{self.x:.6f} Y{self.y:.6f} Z{self.z:.6f} F{STEP}\r\n')

    def move_to_rect(self, coords):
        self.open_grip()
        print(coords)
        self.move(coords[0], coords[1] - 20, 80)
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

    def open_grip(self):
        self.rotate_servo(S_GRIPPER, G_OPEN)

    def close_grip(self):
        self.rotate_servo(S_GRIPPER, G_CLOSE)

    # Turntable
    def allow_turntable_movement(self):
        self.command(f'M302 S0\r\n')

    def move_turntable(self, angle):
        assert angle < 360 and angle >= 0
        # ADD CALCULATE ANGLE FUNCTION
        self.command(f'G0 E{angle}\r\n')

    def home_turntable(self):
        self.move_turntable(0)

    # END CONNECTION

    def end_connection(self):
        time.sleep(2)
        self.serial.close()

# New motion
# G0 X0 Y45 Z320 F500
