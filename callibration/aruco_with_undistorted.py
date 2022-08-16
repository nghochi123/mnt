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

# Set the vision capture device
cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# set new dimensions to cap object (not cap)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while(True):
    # Continuously read from the vision capture device
    ret, frame = cam.read()
    # First undistort the image using calibrated setup
    h,  w = frame.shape[:2]
    dst = cv2.undistort(frame, cameraMatrix, dist, None, newCameraMatrix)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    # Detect Aruco Markers
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

        # Draw a blue rectangle with a length of 15cm and a width of 3cm
        x = 150
        y = 300

        pts = np.array([[[x, y], [x + pixel_cm_ratio * 15, y],
                        [x + pixel_cm_ratio * 15, y + pixel_cm_ratio * 3], [x, y + pixel_cm_ratio * 3]]],
                       np.int32)

        cv2.polylines(dst, pts, True, (255, 0, 0), 10)

    # Show the image
    cv2.imshow("Test", resize(dst))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
