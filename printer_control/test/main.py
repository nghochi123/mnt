import serial
import time
from datetime import datetime
from pynput import keyboard

from constants import MAX_X, MAX_Y, MAX_Z, MIN_X, MIN_Y, MIN_Z

x = 0
y = 0
z = 345

STEP = 10

ser = serial.Serial(port='COM6', baudrate=250000, timeout=.1)


def command(ser, command):
    start_time = datetime.now()
    ser.write(str.encode(command))
    time.sleep(0.1)

    while True:
        line = ser.readline()

        if line == b'ok\n':
            break
    print(command)


def home():
    global x, y, z
    command(ser, "G28\r\n")
    print("Going Home!")
    x = 0
    y = 0
    z = 300


def keypress(key):
    global x, y, z, STEP
    if key == keyboard.Key.esc:
        return False
    elif key == keyboard.Key.up:
        z += STEP
    elif key == keyboard.Key.down:
        z -= STEP
    elif key == keyboard.Key.shift:
        if STEP == 1:
            STEP = 10
        else:
            STEP = 1
    elif type(key) != keyboard.Key:
        if key.char == 'w':
            y += STEP
        elif key.char == 's':
            y -= STEP
        elif key.char == 'd':
            x += STEP
        elif key.char == 'a':
            x -= STEP
        elif key.char == 'h':
            home()
    if x > MAX_X:
        x = MAX_X
    if x < MIN_X:
        x = MIN_X
    if y > MAX_Y:
        y = MAX_Y
    if y < MIN_Y:
        y = MIN_Y
    if z > MAX_Z:
        z = MAX_Z
    if z < MIN_Z:
        z = MIN_Z

    command(ser, f"G0 X{x} Y{y} Z{z}\r\n")


with keyboard.Listener(on_press=keypress) as listener:
    listener.join()

time.sleep(2)
print("Don't kill me!")
ser.close()
