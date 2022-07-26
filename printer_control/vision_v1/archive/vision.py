import numpy as np
import cv2

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


def get_length(x0, y0, x1, y1):
    a = abs(x1 - x0)
    b = abs(y1 - y0)
    return np.sqrt(a * a + b * b)


def calculate_angle(box):
    # 0 refers to lowest coord.
    if get_length(*box[3], *box[2]) > get_length(*box[0], *box[3]):
        # Use 1 and 0
        dy = abs(box[0][1] - box[3][1])
        dx = abs(box[0][0] - box[3][0])
        if dy == 0:
            return np.pi / 2
        return np.arctan(dx / dy)
    dy = abs(box[2][1] - box[3][1])
    dx = abs(box[2][0] - box[3][0])

    return np.pi - np.arctan(dx / dy)


def resize(img):
    # arg1- input image, arg- output_width, output_height
    # return img
    return cv2.resize(img, (1024, 576))


def reduce_to_circle(image, circle):
    x_center, y_center, radius = circle
    image_crop = image[y_center - radius:y_center +
                       radius, x_center - radius:x_center + radius]
    mask = np.zeros_like(image_crop)
    mask = cv2.circle(mask, ((radius, radius)), radius, (1, 1, 1), -1)
    # result = cv2.cvtColor(image_crop, cv2.COLOR_BGR2BGRA)
    # result = np.dot(result[:, :, 3], mask[:, :, 0])
    result = image_crop * mask

    return result


fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=50, detectShadows=True)

# Callibration step
all_circles = []
while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    # sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(
        dist_transform, 0.7*dist_transform.max(), 255, 0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    circles = cv2.HoughCircles(unknown, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=50, param2=20, minRadius=500, maxRadius=550)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            all_circles.append(i)
    cv2.imshow('shit', resize(frame))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

circle = np.mean(all_circles, axis=0).astype(int)
# Background calibration
while(True):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    cv2.imshow('MOG2', resize(fgmask))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

# Put the screws
while(True):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame, learningRate=0)
    cv2.imshow('MOG2', resize(fgmask))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

rectangles = []
# Main detection stuff
count = 0
rects = 0
while(True):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame, learningRate=0)

    # frame = reduce_to_circle(frame, circle)

    fgmask = reduce_to_circle(fgmask, circle)

    _, fgmask = cv2.threshold(fgmask, 250, 255, cv2.THRESH_BINARY)

    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    fgmask = cv2.dilate(fgmask, kernel, iterations=2)

    contours, _ = cv2.findContours(
        fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rectangles = []

    for cnt in contours:
        if cv2.contourArea(cnt) > 200:
            # x, y, width, height = cv2.boundingRect(cnt)

            # cv2.rectangle(fgmask, (x, y), (x + width,
            #               y + height), 255, 2)

            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(fgmask, [box], 0, 255, 2)

            rectangles.append(box)

    cv2.imshow('fasdfsad', fgmask)

    # if len(rectangles) > 0 and count > 20 and len(rectangles) == rects:
    #     break
    # elif len(rectangles) > 0:
    #     count += 1
    #     rects = len(rectangles)
    # else:
    #     count = 0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
