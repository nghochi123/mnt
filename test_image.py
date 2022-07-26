import json
import os
import numpy as np
import cv2


def add_three_arrays(a, b, c):
    return np.array(a) + np.array(b) + np.array(c)


f = open('P0032.txt', 'r')
res = f.readlines()
f.close()

image = cv2.imread('P0032.png')


for line in res:
    x1, y1, x2, y2, x3, y3, x4, y4, obj, difficulty = line.split(' ')

    # if annotation['image_id'] == 2:
    image = cv2.line(image, (int(float(x1)), int(float(y1))),
                     (int(float(x2)), int(float(y2))), (0, 255, 0), 3)
    image = cv2.line(image, (int(float(x2)), int(float(y2))),
                     (int(float(x3)), int(float(y3))), (0, 255, 0), 3)
    image = cv2.line(image, (int(float(x3)), int(float(y3))),
                     (int(float(x4)), int(float(y4))), (0, 255, 0), 3)
    image = cv2.line(image, (int(float(x4)), int(float(y4))),
                     (int(float(x1)), int(float(y1))), (0, 255, 0), 3)
    # f = open(
    #     f'screws_{str(annotation["image_id"]).rjust(3, "0")}.txt', 'a')
    # f.write(f"{x1} {y1} {x2} {y2} {x3} {y3} {x4} {y4} Screw 0\n")
    # f.close()

cv2.imwrite('P0032_write.png', image)
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
