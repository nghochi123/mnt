import cv2
import ast
import numpy as np


def resize(img):
    return cv2.resize(img, (960, 540))


parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
aruco_length = 5
displacement = 1.5

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
    corners, _, _ = cv2.aruco.detectMarkers(
        dst, aruco_dict, parameters=parameters)
    if corners:

        # Draw polygon around the marker
        int_corners = np.int0(corners)
        cv2.polylines(dst, int_corners, True, (0, 255, 0), 5)

        # Aruco Perimeter
        sum_perim = 0
        for corner in corners:
            sum_perim += cv2.arcLength(corner, True)
        aruco_perimeter = sum_perim / len(corners)

        # Pixel to cm ratio
        pixel_cm_ratio = aruco_perimeter / (4 * aruco_length + displacement)

        x = 150
        y = 300

        pts = np.array([[[x, y], [x + pixel_cm_ratio * 15, y],
                        [x + pixel_cm_ratio * 15, y + pixel_cm_ratio * 3], [x, y + pixel_cm_ratio * 3]]],
                       np.int32)

        cv2.polylines(dst, pts, True, (255, 0, 0), 10)

        print(pixel_cm_ratio)

    cv2.imshow("Test", resize(dst))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
