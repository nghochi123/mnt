import time
import numpy as np
from constants.delta import *
from delta_movement import DeltaController
from vision_control import VisionController

vision = VisionController()
delta = DeltaController()


def rect_coords_irl(circle, delta_radius, image_coords):
    image_circle_radius = circle[2]
    ratio = delta_radius / image_circle_radius
    x = (image_coords[0] - image_circle_radius) * ratio
    y = (image_circle_radius - image_coords[1]) * ratio
    return x, y


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


def main():
    delta.home()
    # delta.move(*START)
    delta.allow_vision()
    time.sleep(2)
    vision.callibrate()
    rectangles = vision.get_rects()
    for rectangle in rectangles:
        old_x, old_y = np.average(rectangle, axis=0)
        x, y = rect_coords_irl(vision.circle, RADIUS, [old_x, old_y])
        angle = calculate_angle(rectangle)

        delta.spin_to_angle(angle)
        delta.move_to_rect((x, y))
        delta.move_to_output(np.pi)
    delta.end_connection()


if __name__ == '__main__':
    main()
