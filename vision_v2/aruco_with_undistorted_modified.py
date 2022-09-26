import cv2
import numpy as np


class Aruco():

    def __init__(self):
        pass

    # Set aruco parameters
    parameters = cv2.aruco.DetectorParameters_create()
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
    # Aruco Length on paper irl
    aruco_length = 5
    # Additional displacement because of some error
    displacement = 0

    # Set the vision capture device
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    # set new dimensions to cap object (not cap)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def undist(img):
        DIM = (1920, 1080)

        K = np.array([[15630.97751860718, 0.0, 963.9329353453995], [
            0.0, 15661.236884219428, 483.00118054736294], [0.0, 0.0, 1.0]])

        D = np.array([[-38.34376052988407], [-2131.2243860753247],
                      [1507460.5667898422], [-697687173.7193158]])

        h, w = img.shape[:2]
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(
            K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
        undistorted_img = cv2.remap(
            img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        return undistorted_img

    def aruco_callibrate(trigger):

        while(True):

            # Continuously read from the vision capture device
            ret, frame = Aruco.cam.read()
            dst = Aruco.undist(frame)
            # print(dst.shape)

            # Detect Aruco Markers
            corners, _, _ = cv2.aruco.detectMarkers(
                dst, Aruco.aruco_dict, parameters=Aruco.parameters)
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
                pixel_cm_ratio = aruco_perimeter / \
                    (4 * Aruco.aruco_length + Aruco.displacement)
                pixel_mm_ratio = pixel_cm_ratio / 10

                # Draw a blue rectangle with a length of 15cm and a width of 3cm
                x = 150
                y = 300

                pts = np.array([[[x, y], [x + pixel_cm_ratio * 15, y],
                                [x + pixel_cm_ratio * 15, y + pixel_cm_ratio * 3], [x, y + pixel_cm_ratio * 3]]],
                               np.int32)

                cv2.polylines(dst, pts, True, (255, 0, 0), 10)

            # Show the image
            cv2.imshow("Test", dst)  # , resize(dst))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        return pixel_mm_ratio
