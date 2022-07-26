import serial
import time
from pynput import keyboard
from datetime import datetime

from constants import BAUDRATE, PORT, STEP, TIMEOUT, Z_HOME


class Interface():
    def __init__(self):
        # X, Y, Z
        self.x = 0
        self.y = 0
        self.z = Z_HOME
        self.serial = serial.Serial(
            port=PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
        # self.home()
        time.sleep(2)

    def keypress(self, key):
        if key == keyboard.Key.esc:
            return False
        elif key == keyboard.Key.up:
            self.z += STEP
        elif key == keyboard.Key.down:
            self.z -= STEP
        elif type(key) != keyboard.Key:
            if key.char == 'w':
                self.y += STEP
            elif key.char == 'a':
                self.y -= STEP
            elif key.char == 's':
                self.x += STEP
            elif key.char == 'd':
                self.x -= STEP
            elif key.char == 'h':
                self.home()
        self.update()

    def home(self):
        self.x = 0
        self.y = 0
        self.z = Z_HOME
        self.command("G28\r\n")

    def update(self):
        self.command(f"G01 X{self.x:.6f} Y{self.y:.6f} Z{self.z:.6f}\r\n")

    def run(self):
        time.sleep(2)
        self.home()
        # with keyboard.Listener(on_press=self.keypress) as listener:
        #     listener.join()

    def close_serial(self):
        time.sleep(2)
        self.serial.close()

    def command(self, command):
        start_time = datetime.now()
        self.serial.write(str.encode(command))
        time.sleep(1)

        while True:
            line = self.serial.readline()
            print(line)

            if line == b'ok\n':
                break


# Testing code
def main():
    interface = Interface()
    print(interface.serial)


if __name__ == '__main__':
    main()
