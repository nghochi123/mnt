import serial
import time
import math

from constants.delta import *


def ensure_radius(x, y):
    if math.sqrt(x * x + y * y) <= RADIUS:
        return True
    else:
        return False


class DeltaController():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 345
        self.step = STEP
        self.servos = {
            SERVO0: 0,
            SERVO1: 0
        }
        self.serial = serial.Serial(
            port=PORT, baudrate=BAUDRATE, timeout=TIMEOUT)

        time.sleep(2)

    def command(self, command):
        self.serial.write(str.encode(command))
        time.sleep(0.1)

        while True:
            line = self.serial.readline()

            if line == b'ok\n':
                break

    def home(self):
        self.x = 0
        self.y = 0
        self.z = Z_HOME
        self.command('G28\r\n')

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
        self.move(*coords, 20)
        self.hover_upwards()

    def hover_upwards(self):
        self.move(self.x, self.y, HOVER)

    # TODO: 1. Approx arc with radians

    # SERVO CONTROLS

    def rotate_servo(self, servo, angle):
        assert angle < 200
        self.servos[servo] = angle
        self.command(f'M280 {servo} S{angle}\r\n')

    def end_connection(self):
        time.sleep(2)
        self.serial.close()

# New motion
# G0 X0 Y45 Z320 F500