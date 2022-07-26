import time
from constants.delta import *
from delta_movement import DeltaController
from vision_control import VisionController

vision = VisionController()
delta = DeltaController()


def image_to_physical(circle, delta_radius, image_coords):
    image_circle_radius = circle[2]
    ratio = delta_radius / image_circle_radius
    x = (image_coords[0] - image_circle_radius) * ratio
    y = (image_circle_radius - image_coords[1]) * ratio
    return x, y


def main():
    delta.home()
    # delta.move(*START)
    delta.allow_vision()
    time.sleep(2)
    vision.callibrate()
    rectangles = vision.get_rects()
    print(rectangles)
    for rectangle in rectangles:
        x, y = image_to_physical(vision.circle, RADIUS, [
            rectangle[0], rectangle[1]])
        print(x, y)
        delta.move_to_rect((x, y))
    delta.end_connection()


if __name__ == '__main__':
    main()
