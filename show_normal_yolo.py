import json
import os
import numpy as np
import cv2


def add_three_arrays(a, b, c):
    return np.array(a) + np.array(b) + np.array(c)


f = open('annotations_normal/screws_002.txt', 'r')
res = f.readlines()
f.close()

image_width = 1920
image_height = 1440

os.chdir('annotations')

image = cv2.imread('screws_002.png')


for line in res:
    category, x, y, width, height = [float(x) for x in line.split(' ')]
    x, width = x * image_width, width * image_width
    y, height = y * image_height, height * image_height
    x1, y1 = add_three_arrays([x, y], [0, height / 2], [-width / 2, 0])
    x2, y2 = add_three_arrays([x, y], [0, height / 2], [width / 2, 0])
    x3, y3 = add_three_arrays([x, y], [0, -height / 2], [width / 2, 0])
    x4, y4 = add_three_arrays([x, y], [0, -height / 2], [-width / 2, 0])
    # if annotation['category_id'] in [1, 2, 3, 4, 5, 6, 8, 12, 13]:
    #     # f = open(f'screws_{annotation["image_id"]}.txt', 'a')
    #     bbox = annotation['bbox']
    #     y, x, w, h, phi = bbox
    #     phi = np.pi - phi
    #     R = [[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]]
    #     top_disp = np.dot(R, [0, h / 2])
    #     left_disp = np.dot(R, [w / 2, 0])
    #     right_disp = np.dot(R, [-w / 2, 0])
    #     bottom_disp = np.dot(R, [0, -h / 2])
    #     x1, y1 = add_three_arrays([x, y], top_disp, left_disp)
    #     x2, y2 = add_three_arrays([x, y], top_disp, right_disp)
    #     x3, y3 = add_three_arrays([x, y], bottom_disp, right_disp)
    #     x4, y4 = add_three_arrays([x, y], bottom_disp, left_disp)

    #     if annotation['image_id'] == 2:
    image = cv2.line(image, (int(x1), int(y1)),
                     (int(x2), int(y2)), (0, 255, 0), 3)
    image = cv2.line(image, (int(x2), int(y2)),
                     (int(x3), int(y3)), (0, 255, 0), 3)
    image = cv2.line(image, (int(x3), int(y3)),
                     (int(x4), int(y4)), (0, 255, 0), 3)
    image = cv2.line(image, (int(x4), int(y4)),
                     (int(x1), int(y1)), (0, 255, 0), 3)
    #         # f = open(
    #         #     f'screws_{str(annotation["image_id"]).rjust(3, "0")}.txt', 'a')
    #         # f.write(f"{x1} {y1} {x2} {y2} {x3} {y3} {x4} {y4} Screw 0\n")
    #         # f.close()
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
