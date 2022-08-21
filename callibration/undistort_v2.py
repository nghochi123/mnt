import cv2
import numpy as np
import sys

# You should replace these 3 lines with the output in calibration step
DIM = (1920, 1080)
K = np.array([[15630.97751860718, 0.0, 963.9329353453995], [
             0.0, 15661.236884219428, 483.00118054736294], [0.0, 0.0, 1.0]])
D = np.array([[-38.34376052988407], [-2131.2243860753247],
             [1507460.5667898422], [-697687173.7193158]])


def undistort(img_path):
    img = cv2.imread(img_path)
    cv2.imshow("distorted", img)
    cv2.waitKey(0)
    h, w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(
        K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(
        img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imwrite("undistorted_callibrated.png", undistorted_img)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)
