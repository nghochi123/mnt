# import the necessary packages
from scipy.spatial import distance as dist
import numpy as np
import imutils
from imutils import contours
from imutils import perspective
import cv2

# detect aruco marker


def findArucoMarkers(img, markerSize=6, totalMarkers=100, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(cv2.aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    # print(key)

    # Load the dictionary that was used to generate the markers.
    arucoDict = cv2.aruco.Dictionary_get(key)

    # Initialize the detector parameters using default values
    arucoParam = cv2.aruco.DetectorParameters_create()

    # Detect the markers
    bboxs, ids, rejected = cv2.aruco.detectMarkers(
        gray, arucoDict, parameters=arucoParam)
    return bboxs, ids, rejected
# find object size


# Load image
image = cv2.imread("2.jpg")

# resize image
image = imutils.resize(image, width=500)

# convert BGR image to gray scale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# remove Gaussian noise from the image
gray = cv2.GaussianBlur(gray, (7, 7), 0)

# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# sort the contours from left-to-right and initialize the
(cnts, _) = contours.sort_contours(cnts)

# for pixel to inch calibration
pixelsPerMetric = None

# Detect Aruco marker and use
# it's dimension to calculate the pixel to inch ratio
arucofound = findArucoMarkers(image, totalMarkers=100)
if len(arucofound[0]) != 0:
    print(arucofound[0][0][0])
    aruco_perimeter = cv2.arcLength(arucofound[0][0][0], True)
    print(aruco_perimeter)
    # Pixel to Inch ratio
    # perimeter of the aruco marker is 8 inches
    pixelsPerMetric = aruco_perimeter / 8
    print(" pixel to inch", pixelsPerMetric)
else:
    pixelsPerMetric = 38.0

# loop over the contours individually
for c in cnts:

    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 2000:
        continue
    ''' bounding rectangle is drawn with minimum area, so it considers the rotation also. 
    The function used is cv.minAreaRect(). It returns a Box2D structure which contains following details - 
    ( center (x,y), (width, height), angle of rotation ). 
    But to draw this rectangle, we need 4 corners of the rectangle. 
    It is obtained by the function cv.boxPoints()
    '''
    # compute the rotated bounding box of the contour
    box = cv2.minAreaRect(c)
    box = cv2.boxPoints(box)
    box = np.int0(box)
    cv2.drawContours(image, [box], 0, (0, 0, 255), 2)

    # Draw the centroid
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.circle(image, (cX, cY), 5, (255, 255, 255), -1)

    # order the points in the contour such that they appear
    # in top-left, top-right, bottom-right, and bottom-left
    # order, then draw the outline of the rotated bounding
    # box
    (tl, tr, br, bl) = box
    width_1 = (dist.euclidean(tr, tl))
    height_1 = (dist.euclidean(bl, tl))
    d_wd = width_1/pixelsPerMetric
    d_ht = height_1/pixelsPerMetric

    # display the image with object width and height in inches
    cv2.putText(image, "{:.1f}in".format(d_wd), ((int((tl[0] + tr[0])*0.5)-15, int(
        (tl[1] + tr[1])*0.5)-15)), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    cv2.putText(image, "{:.1f}in".format(d_ht), ((int((tr[0] + br[0])*0.5)+10, int(
        (tr[1] + br[1])*0.5)+10)), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    # show the output image
    cv2.imshow("Image-dim", image)
    fname = "size{}.jpg".format(str('s'))
    cv2.imwrite(fname, image)
    key = cv2.waitKey(0)

cv2.destroyAllWindows()
