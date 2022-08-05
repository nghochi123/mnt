import numpy as np
import cv2 as cv
import glob
import os

import ast

dist_old = np.load('dist.npy')
cameraMatrix_old = np.load('camera_matrix.npy')
newCameraMatrix_old = np.load('new_camera_matrix.npy')
roi_old = ()
with open('f', 'r') as f:
    roi_old = f.readline()
    roi_old = ast.literal_eval(roi_old)

os.chdir('./images')

################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################

chessboardSize = (17, 12)
frameSize = (1920, 1080)


# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)


# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboardSize[0],
                       0:chessboardSize[1]].T.reshape(-1, 2)

size_of_chessboard_squares_mm = 9
objp = objp * size_of_chessboard_squares_mm


# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.


images = glob.glob('*.png')

for image in images:

    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # cv.imshow('img', gray)
    cv.waitKey(1)

    # Find the chess board corners
    ret, corners = cv.findChessboardCornersSB(gray, chessboardSize, None)

    print(ret)

    # If found, add object points, image points (after refining them)
    if ret == True:

        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(1000)


cv.destroyAllWindows()


############## CALIBRATION #######################################################

ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(
    objpoints, imgpoints, frameSize, None, None)


############## UNDISTORTION #####################################################
os.chdir('../')

img = cv.imread('image_15.png')
h,  w = img.shape[:2]
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(
    cameraMatrix, dist, (w, h), 1, (w, h))

print(newCameraMatrix, newCameraMatrix_old, cameraMatrix, cameraMatrix_old)

print(dist == dist_old, 'hello', cameraMatrix == cameraMatrix_old, 'hello',
      newCameraMatrix == newCameraMatrix_old, 'hello', roi == roi_old)

np.save('dist', dist)
np.save('camera_matrix', cameraMatrix)
np.save('new_camera_matrix', newCameraMatrix)
print(roi)

# Undistort
dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('caliResult1.png', dst)


# # Undistort with Remapping
# mapx, mapy = cv.initUndistortRectifyMap(
#     cameraMatrix, dist, None, newCameraMatrix, (w, h), 5)
# dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

# # crop the image
# x, y, w, h = roi
# dst = dst[y:y+h, x:x+w]
# cv.imwrite('caliResult2.png', dst)


# Reprojection Error
mean_error = 0

for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(
        objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error

print("total error: {}".format(mean_error/len(objpoints)))


def resize(img):
    return cv.resize(img, (1024, 576))


cam = cv.VideoCapture(1, cv.CAP_DSHOW)

# set new dimensionns to cap object (not cap)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 2048)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

while(True):
    ret, frame = cam.read()
    h,  w = frame.shape[:2]
    dst = cv.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv.imshow("Test", resize(dst))
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
