import numpy as np
import cv2

from constants.vars import VIDEO_LINK, HOUGH_MAX, HOUGH_MIN, HOUGH_PARAM_1, HOUGH_PARAM_2


def resize(img):
    return cv2.resize(img, (1024, 576))


def reduce_to_circle(image, circle):
    x_center, y_center, radius = circle
    image_crop = image[y_center - radius:y_center +
                       radius, x_center - radius:x_center + radius]
    mask = np.zeros_like(image_crop)
    mask = cv2.circle(mask, ((radius, radius)), radius, (1, 1, 1), -1)
    result = image_crop * mask

    return result


class VisionController():
    def __init__(self):
        self.cap = cv2.VideoCapture(VIDEO_LINK, cv2.CAP_DSHOW)
        self.fgbg = cv2.createBackgroundSubtractorMOG2(
            varThreshold=50, detectShadows=True)
        self.all_circles = []
        self.rectangles = []

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

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

    def background_callibration(self):
        while(True):
            _, frame = self.cap.read()
            fgmask = self.fgbg.apply(frame)
            cv2.imshow('Background Callibration', resize(fgmask))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def screw_placement(self):
        while(True):
            _, frame = self.cap.read()
            fgmask = self.fgbg.apply(frame, learningRate=0)
            cv2.imshow('Screw Placement', resize(fgmask))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def detect_screws(self):
        count = 0
        rects = 0
        while(True):
            ret, frame = self.cap.read()

            fgmask = self.fgbg.apply(frame, learningRate=0)

            fgmask = reduce_to_circle(fgmask, self.circle)

            _, fgmask = cv2.threshold(fgmask, 250, 255, cv2.THRESH_BINARY)
            kernel = np.ones((3, 3), np.uint8)
            fgmask = cv2.erode(fgmask, kernel, iterations=1)
            fgmask = cv2.dilate(fgmask, kernel, iterations=2)

            contours, _ = cv2.findContours(
                fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            rectangles = []

            for cnt in contours:
                if cv2.contourArea(cnt) > 200:

                    x, y, width, height = cv2.boundingRect(cnt)

                    cv2.rectangle(fgmask, (x, y), (x + width,
                                                   y + height), 255, 2)

                    rectangles.append([x, y, width, height])

            cv2.imshow('Detecting Screws', fgmask)

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

    def callibrate(self):
        self.circle_callibration()
        self.background_callibration()

    def get_rects(self):
        self.screw_placement()
        self.detect_screws()
        return self.rectangles
