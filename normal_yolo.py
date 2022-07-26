import json
import os
import numpy as np
import cv2


def add_three_arrays(a, b, c):
    return np.array(a) + np.array(b) + np.array(c)


f = open('mvtec_screws.json', 'r')
res = json.load(f)
f.close()

os.chdir('annotations_normal')

annotations = res['annotations']
image_width = 1920
image_height = 1440

'''
For normal YOLO, class x_center y_center width height, which means we can simply use the original format.
'''

for annotation in annotations:
    if annotation['category_id'] in [1, 2, 3, 4, 5, 6, 8, 12, 13]:
        # f = open(f'screws_{annotation["image_id"]}.txt', 'a')
        bbox = annotation['bbox']
        y, x, w, h, phi = bbox
        f = open(
            f'screws_{str(annotation["image_id"]).rjust(3, "0")}.txt', 'a')
        f.write(
            f"0 {round(x/image_width, 5)} {round(y/image_height, 5)} {round(w/image_width, 5)} {round(h/image_height, 5)}\n")
        f.close()
