import json
import os
import numpy as np
import cv2


def add_three_arrays(a, b, c):
    return np.array(a) + np.array(b) + np.array(c)


f = open('mvtec_screws.json', 'r')
res = json.load(f)
f.close()

os.chdir('annotations')

annotations = res['annotations']

'''
Format required by YOLOv5 is: centerX, centerY, width, height. IN PERCENTAGE FORM RELATIVE TO ENTIRE IMAGE.
BASED ON IMAGES,
CATEGORIES WE WANT (THAT ARE SCREWS) ARE:
1,2,3,4,5,6,8,12,13.
ALL IMAGES HAVE HEIGHT: 1440, WIDTH 1920.
Markus Ulrich, Patrick Follmann, Jan-Hendrik Neudeck: A comparison of shape-based matching with deep-learning-based object detection; in: Technisches Messen, 2019, DOI 10.1515/teme-2019-0076.
WE WANT TO WRITE IN AS CATEGORY 0 (SCREWS)
THE BBOX VARIABLE HAS: row, col, width, height, phi
https://github.com/hukaixuan19970627/yolov5_obb
REQUIRES (x1,y1,x2,y2,x3,y3,x4,y4,CATEGORY,DIFFICULTY)
'''
image = cv2.imread('screws_002.png')


for annotation in annotations:
    if annotation['category_id'] in [1, 2, 3, 4, 5, 6, 8, 12, 13]:
        # f = open(f'screws_{annotation["image_id"]}.txt', 'a')
        bbox = annotation['bbox']
        y, x, w, h, phi = bbox
        phi = np.pi - phi
        R = [[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]]
        top_disp = np.dot(R, [0, h / 2])
        left_disp = np.dot(R, [w / 2, 0])
        right_disp = np.dot(R, [-w / 2, 0])
        bottom_disp = np.dot(R, [0, -h / 2])
        x1, y1 = add_three_arrays([x, y], top_disp, left_disp)
        x2, y2 = add_three_arrays([x, y], top_disp, right_disp)
        x3, y3 = add_three_arrays([x, y], bottom_disp, right_disp)
        x4, y4 = add_three_arrays([x, y], bottom_disp, left_disp)

        if annotation['image_id'] == 2:
            image = cv2.line(image, (int(x1), int(y1)),
                             (int(x2), int(y2)), (0, 255, 0), 3)
            image = cv2.line(image, (int(x2), int(y2)),
                             (int(x3), int(y3)), (0, 255, 0), 3)
            image = cv2.line(image, (int(x3), int(y3)),
                             (int(x4), int(y4)), (0, 255, 0), 3)
            image = cv2.line(image, (int(x4), int(y4)),
                             (int(x1), int(y1)), (0, 255, 0), 3)
            # f = open(
            #     f'screws_{str(annotation["image_id"]).rjust(3, "0")}.txt', 'a')
            # f.write(f"{x1} {y1} {x2} {y2} {x3} {y3} {x4} {y4} Screw 0\n")
            # f.close()
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
