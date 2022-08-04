from scipy.spatial import distance as dist
import numpy as np
import argparse
import cv2
import math
import time

def resize(img):
    return cv2.resize(img, (1024, 576))


cap = cv2.VideoCapture(2, cv2.CAP_V4L)

# set new dimensionns to cap object (not cap)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if cap.read() == False:
    cap.open()

time.sleep(2)

while(True):
    ret, frame = cap.read()
    print(ret)
    cv2.imshow("Test", resize(frame))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
