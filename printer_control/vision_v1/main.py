# Main code, integrate everything into this code.
# Put anything related to the camera in vision_control.py, and anything related to the control of the printer into delta_movement.py.
# This is making use of object oriented programming. A good guide might be this: https://realpython.com/python3-object-oriented-programming/
# Basically, what you will be doing is to edit the functions in the class, and calling self.<function_name> to run it.
import time
import numpy as np
from constants.delta import *
from delta_movement import DeltaController
from vision_control import VisionController

# Initialize the vision controller and delta printer classes.
vision = VisionController()
delta = DeltaController()

# A function to convert the bounding boxes detected in the circle mask into delta printer coordinates.


def rect_coords_irl(circle, delta_radius, image_coords):
    image_circle_radius = circle[2]
    ratio = delta_radius / image_circle_radius
    x = (image_coords[0] - image_circle_radius) * ratio
    y = (image_circle_radius - image_coords[1]) * ratio
    return x, y

# Get the length between two points (Pythagoras)


def get_length(x0, y0, x1, y1):
    a = abs(x1 - x0)
    b = abs(y1 - y0)
    return np.sqrt(a * a + b * b)

# Calculate the angle of the bounding box (using tangent inverse between the change in x direction vs change in y direction)


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

# Functions in classes work this way: <className>.<function_name>(). The functions only work in the class that it is defined in.


def main():
    # First home the machine (Using the delta printer class that was initiated)
    delta.home()
    delta.home_turntable()
    # Move the camera + claw somewhere that doesn't block the camera
    delta.allow_vision()
    time.sleep(2)
    # Allow the calibration of the vision to occur - recognise circle, background subtraction, and noise cancelling.
    vision.callibrate()
    # Get the bounding boxes that correspond to the screws identified.
    rectangles = vision.get_rects()
    for rectangle in rectangles:
        # Get the irl coordinates of the center of the screw, as well as its angle. The angle is relative to the normal angle used in math, and is in radians.
        old_x, old_y = np.average(rectangle, axis=0)
        x, y = rect_coords_irl(vision.circle, RADIUS, [old_x, old_y])
        angle = calculate_angle(rectangle)

        # Spin the servo in the angle detected by the screws, then move to it, grip it and move to the output in an arc
        delta.spin_to_angle(angle)
        delta.move_to_rect((x, y))
        delta.move_to_output(np.pi)
    # End connection to safely exit the program.
    delta.end_connection()


if __name__ == '__main__':
    main()
