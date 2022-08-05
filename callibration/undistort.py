import cv2
import ast
import numpy as np


def resize(img):
    return cv2.resize(img, (1024, 576))


dist = np.load('dist.npy')
cameraMatrix = np.load('camera_matrix.npy')
newCameraMatrix = np.load('new_camera_matrix.npy')
roi = ()
with open('f', 'r') as f:
    roi = f.readline()
    roi = ast.literal_eval(roi)
cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# set new dimensionns to cap object (not cap)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while(True):
    ret, frame = cam.read()
    h,  w = frame.shape[:2]
    dst = cv2.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imshow("Test", resize(dst))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
