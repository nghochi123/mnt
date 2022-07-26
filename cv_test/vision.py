from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import math


def resize(img):
    return cv2.resize(img, (1024, 576))


cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# set new dimensionns to cap object (not cap)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

r, frame = cap.read()

print('Resolution: ' + str(frame.shape[0]) + ' x ' + str(frame.shape[1]))


while(True):
    ret, frame = cap.read()
    cv2.imshow("Test", resize(frame))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
