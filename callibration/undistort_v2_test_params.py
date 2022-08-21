import cv2
import numpy as np
import sys

# You should replace these 3 lines with the output in calibration step
DIM = (1920, 1080)
K = np.array([[1416.075821043672, 0.0, 966.0639173760993], [
             0.0, 1413.0795084730821, 483.96859228345846], [0.0, 0.0, 1.0]])
D = np.array([[-0.12161218796037346], [0.3342925061383832],
             [-1.5724350814060781], [1.8229490266346593]])


def undistort(img_path):
    img = cv2.imread(img_path)
    cv2.imshow("distorted", img)
    cv2.waitKey(0)
    h, w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(
        K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(
        img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imwrite("undistorted_callibrated_test_params.png", undistorted_img)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)
