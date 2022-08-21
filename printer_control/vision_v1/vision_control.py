import numpy as np
import cv2

from constants.vars import VIDEO_LINK, HOUGH_MAX, HOUGH_MIN, HOUGH_PARAM_1, HOUGH_PARAM_2

# Resize image for visibility purposes

def reduce_size(img):
    return cv2.resize(img, (512, 288))

# Change the image from a rectangle to a circle, to reduce the focus to just a smaller range

def reduce_to_circle(image, circle):
    x_center, y_center, radius = circle
    image_crop = image[y_center - radius:y_center +
                       radius, x_center - radius:x_center + radius]
    mask = np.zeros_like(image_crop)
    mask = cv2.circle(mask, ((radius, radius)), radius, (1, 1, 1), -1)
    result = image_crop * mask

    return result

# Vision controller class


class VisionController():
    # Initialise the video capturing device, as well as the background subtraction model for use later on
    def __init__(self):
        self.cap = cv2.VideoCapture(VIDEO_LINK, cv2.CAP_V4L)
        self.fgbg = cv2.createBackgroundSubtractorMOG2(
            varThreshold=70, detectShadows=True)
        self.all_circles = []
        self.rectangles = []

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # Detect where the circle is.

    def circle_callibration(self):
        while True:
            _, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            _, thresh = cv2.threshold(
                gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            # noise removal
            kernel = np.ones((3, 3), np.uint8)
            opening = cv2.morphologyEx(
                thresh, cv2.MORPH_OPEN, kernel, iterations=2)
            # sure background area
            sure_bg = cv2.dilate(opening, kernel, iterations=3)
            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
            _, sure_fg = cv2.threshold(
                dist_transform, 0.7*dist_transform.max(), 255, 0)
            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            unknown = cv2.subtract(sure_bg, sure_fg)
            circles = cv2.HoughCircles(unknown, cv2.HOUGH_GRADIENT, 1, 20,
                                       param1=HOUGH_PARAM_1, param2=HOUGH_PARAM_2,
                                       minRadius=HOUGH_MIN, maxRadius=HOUGH_MAX)
            # Since the circles detected may not be accurate, I opted to take the average of all the circles detected.
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    self.all_circles.append(i)
            cv2.imshow('Callibration', resize(frame))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.circle = np.mean(self.all_circles, axis=0).astype(int)
        cv2.destroyAllWindows()

    # Callibrate background using background subtraction
    def background_callibration(self):
        while(True):
            _, frame = self.cap.read()
            fgmask = self.fgbg.apply(frame)
            cv2.imshow('Background Callibration', resize(fgmask))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    # This is a pause for placement of screws, if there is a lot of white, means that calibration did not go well = restart
    def screw_placement(self):
        while(True):
            _, frame = self.cap.read()
            fgmask = self.fgbg.apply(frame, learningRate=0)
            cv2.imshow('Screw Placement', resize(fgmask))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    # Detect Screws
    def detect_screws(self):
        while(True):
            ret, frame = self.cap.read()

            # Using the predefined background subtraction model, we create a mask, then reduce it to a circle.
            fgmask = self.fgbg.apply(frame, learningRate=0)
            fgmask = reduce_to_circle(fgmask, self.circle)
            # We reduce the noise with a threshold, erode and dilate function. (Just need to know that it reduces the noise)
            _, fgmask = cv2.threshold(fgmask, 250, 255, cv2.THRESH_BINARY)
            kernel = np.ones((3, 3), np.uint8)
            fgmask = cv2.erode(fgmask, kernel, iterations=1)
            fgmask = cv2.dilate(fgmask, kernel, iterations=2)

            # Using contour detection, we try to find contours in the mask (So basically from the front,
            # we make it completely black and white so we can easily determine the boundaries and find the edges or contours)
            contours, _ = cv2.findContours(
                fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            rectangles = []

            # We create a oriented bounding box based on the contours detected AND only if the area is greater than 200 pixels^2, and collect all these boxes.
            for cnt in contours:
                if cv2.contourArea(cnt) > 200:

                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(fgmask, [box], 0, 255, 2)

                    rectangles.append(box)

            cv2.imshow('Detecting Screws', reduce_size(fgmask))

            # if len(rectangles) > 0 and count > 20 and len(rectangles) == rects:
            #     break
            # elif len(rectangles) > 0:
            #     count += 1
            #     rects = len(rectangles)
            # else:
            #     count = 0

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.rectangles = rectangles
        cv2.destroyAllWindows()

    # Convenience function
    def callibrate(self):
        self.circle_callibration()
        self.background_callibration()

    # Convenience function
    def get_rects(self):
        self.screw_placement()
        self.detect_screws()
        return self.rectangles
