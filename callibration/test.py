import cv2
import ast
import numpy as np

# Resizes image


def resize(img):
    return cv2.resize(img, (960, 540))


# Set aruco parameters
parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
# Aruco Length on paper irl
aruco_length = 5
# Additional displacement because of some error
displacement = 1.5

# Load pre-saved callibration files
dist = np.load('dist.npy')
cameraMatrix = np.load('camera_matrix.npy')
newCameraMatrix = np.load('new_camera_matrix.npy')
roi = ()
with open('f', 'r') as f:
    roi = f.readline()
    roi = ast.literal_eval(roi)

img = cv2.imread("image_15.png")
cv2.imshow("distorted", img)
cv2.waitKey(0)
h,  w = img.shape[:2]
dst = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)
cv2.imshow("undistorted", dst)
cv2.waitKey(0)
