import time
import numpy as np
from constants.delta import *
from constants.screws import *
from aruco_with_undistorted_modified import Aruco
from delta_movement import DeltaController
from vision_control import VisionController

#aruco = Aruco()
#vision = VisionController()
delta = DeltaController()

#text = "length,width\n"

# original rect coords irl
def rect_coords_irl(circle, delta_radius, image_coords):
    image_circle_radius = circle[2]
    ratio = delta_radius / image_circle_radius
    x = (image_coords[0] - image_circle_radius) * ratio
    y = (image_circle_radius - image_coords[1]) * ratio
    return x, y

# def rect_coords_irl(circle, ratio, image_coords):
#    image_circle_radius = circle[2]
#    # ratio = delta_radius / image_circle_radius
#    x = (image_coords[0] - image_circle_radius) /(ratio/10)
#    y = (image_circle_radius - image_coords[1]) /(ratio/10)
#    return x, y

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

'''
def screw_sort(lw):
    l,w=lw
    for head in head_sizes:
        if round(w,3) <= head:
            headindex=head_sizes.index(head)
            headsize=headindex+2
            break
    return headsize, l, w
    for length in length_sizes[headindex]:
        if l<=length:
            lengthsize=length_irl_sizes[headindex][length_sizes[headindex].index(length)]
            break
    
    return headsize, lengthsize
'''
def get_irl_dimensions(box, pixel_mm_ratio):
    #global text
    side1 = get_length(*box[1], *box[0]) / pixel_mm_ratio
    side2 = get_length(*box[2], *box[1]) / pixel_mm_ratio

    if side1 >= side2:
        full_length = side1
        full_width = side2
    else:
        full_length = side2
        full_width = side1
    
    return full_length, full_width

    text = text + f"{full_length},{full_width}\n"


def main():
    while True:
        c=input('What to test? ')
        if c=='t':
            while True:
                delta.allow_turntable_movement()
                turn=int(input('Input angle:'))
                #delta.home_turntable()
                if turn=='c':
                    break
                time.sleep(1)
                delta.move_turntable(turn)
        elif c=='e':
            delta.end_connection()
            exit()
        elif c=='pos':   #to check for marking on tape
            delta.home()
            time.sleep(1)
            while True:     #find corresponding index number and then screw type, make gripper go to screw type and test ramp
                delta.open_grip()
                stype=input('Input screw type to check (follow this format, M2,6mm or M5,25mm etc)): ')
                if stype in screwstrlst: 
                    placeno=int(input('Key in place number (1/2/3): '))
                    if placeno in [1,2,3]:
                        stypelst=screwtypes2[screwstrlst.index(stype)][placeno+3]
                        print(stypelst)
                        delta.move(stypelst[0],stypelst[1],stypelst[2])
                        time.sleep(1)
                        delta.ramp()
                    else:
                        print('Invalid place no, try again!')
                elif stype=='c':
                    break
                else:
                    print('Screw type invalid, try again!')
        else:
            delta.home()
            # delta.move(*START)
            #delta.allow_vision()
            time.sleep(1)
            delta.open_grip()
            while True:      
                c=input('Input coordinates to go to: ')
                if c=='' or c=='c':
                    break
                elif c=='home':
                    delta.home()
                elif c=='close':
                    delta.close_grip()
                elif c=='open':
                    delta.open_grip()
                elif c=='ramp':
                    delta.close_grip()
                    time.sleep(1)
                    delta.move(-20,0,170)
                    delta.move(0,-115,210)
                    #delta.move(0,-115,200)
                    time.sleep(1)
                    delta.open_grip()
                elif c=='resetgrip':
                    delta.spin_to_angle(np.pi/2)
                    delta.close_grip()
                elif c=='testgrip':
                    delta.close_grip()
                    try:
                        delta.move(oldx,oldy,150)
                    except:
                        delta.open_grip()
                elif c=='adjustgrip':
                    delta.open_grip(True)
                else:
                    try:
                        x,y,z=c.split(',')
                        if x=='s':
                            x=oldx
                        if y=='s':
                            y=oldy
                        if z=='s':
                            z=oldz
                        x,y,z=int(x),int(y),int(z)
                        oldx,oldy,oldz=x,y,z
                        delta.move(x,y,z)
                    except:
                        print('Incorrect input, try again!')

    # for rectangle in rectangles:
    #     #get_irl_dimensions(rectangle, pixel_per_mm)
    #     screwtype=screw_sort(get_irl_dimensions(rectangle, pixel_per_mm))
    #     print(screwtype)
    #     #delta.allow_turntable_movement()
    #     #delta.home_turntable()
    #     #delta.move_turntable(screwtype)
    #     old_x, old_y = np.average(rectangle, axis=0)
    #     x, y = rect_coords_irl(vision.circle, RADIUS, [old_x, old_y])
    #     angle = calculate_angle(rectangle)

    #     delta.spin_to_angle(angle)
    #     delta.move_to_rect((x, y))
    #     delta.move_to_output(np.pi/4)
    #delta.open_grip()


if __name__ == '__main__':
    main()
    '''
    with open('text.txt', 'w') as f:
        f.write(text)
    '''