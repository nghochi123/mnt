import time
import tkinter as tk
import numpy as np
from constants.delta import *
from constants.screws import screwtypes, screwstrlst, screwtypes2, turntable_angles, head_sizes, totalplaces
from aruco_with_undistorted_modified import Aruco
from delta_movement import DeltaController
from vision_control import VisionController

aruco = Aruco()
vision = VisionController()
delta = DeltaController()

# *********************START OF GUI CODE*********************************

screw_selection = []


def selector():
    root = tk.Tk()
    root.title('Screw Selection')
    root.minsize(200, 200)

    window = tk.Tk()
    window.title('Selected screws')

    btn_list = []  # List to hold the button objects
    c_no, i, c = 0, 0, 0

    def update_screw(condition=0):
        global screw_selection
        s = ''

        def resetscreen():
            global screw_selection
            root.destroy()
            screw_selection = []
            selector()

        if condition == 0:
            for i in screw_selection:
                s += i[0]+' '
            try:
                label['text'] = s
                label2['text'] = ''
            except:
                resetscreen()
        elif condition == 1:
            try:
                label2['text'] = 'Screw has already been selected!'
            except:
                resetscreen()
        else:
            try:
                label2['text'] = '5 screws have already been selected!'
            except:
                resetscreen()

    def onClick(idx):
        global screw_selection
        if len(screw_selection) < 5:
            if [btn_list[idx].cget("text"), idx] not in screw_selection:
                screw_selection.append([btn_list[idx].cget("text"), idx])
                update_screw()
            else:
                update_screw(1)
        else:
            update_screw(2)

    def delscrew():
        global screw_selection
        if len(screw_selection) > 0:
            screw_selection.pop()
            update_screw()

    def close():
        try:
            root.destroy()
        except:
            pass
        window.destroy()

    for h in screwtypes:
        for s in h:
            b = tk.Button(
                root, text=screwstrlst[c], command=lambda idx=c: onClick(idx))
            b.grid(row=i, column=c_no)
            btn_list.append(b)
            i += 1
            c += 1
        c_no += 2
        i = 0

    label = tk.Label(master=window, text="")
    label.grid(row=0, column=0)
    label2 = tk.Label(master=window, text="")
    label2.grid(row=1, column=0)

    del_b = tk.Button(window, text=' '*25+'Delete previous selection' +
                      ' '*25, command=lambda: delscrew())
    del_b.grid(row=2, column=0)
    confirm_b = tk.Button(
        window, text=' '*25+' Confirm entire selection '+' '*25, command=lambda: close())
    confirm_b.grid(row=3, column=0)

    window.mainloop()
    root.mainloop()
    if len(screw_selection) == 0:
        selector()
    numlst = [s[1] for s in screw_selection]
    numlst.sort()
    screwstr = ''
    for num in numlst:
        screwstr += screwstrlst[num]+' '

    window2 = tk.Tk()
    window2.title('Boxes')
    label = tk.Label(
        master=window2, text="Screws will be placed in clockwise order with")
    label.grid(row=0, column=0)
    label = tk.Label(
        master=window2, text="the first screw type being placed in the box")
    label.grid(row=1, column=0)
    label = tk.Label(
        master=window2, text="directly below the ramp. Order of screws:")
    label.grid(row=2, column=0)
    label = tk.Label(master=window2, text=screwstr)
    label.grid(row=3, column=0)
    label = tk.Label(master=window2, text='Close window when done viewing.')
    label.grid(row=4, column=0)

    window2.mainloop()

    return [screwtypes2[i] for i in numlst]


# end of sorting, let user decide what to do next
num = -1
labeltext = 'Enter 0 to continue sorting with same screw types\nEnter 1 to continue sorting with different screw types\nEnter 2 '
labeltext += 'to stop sorting'


def finish():
    global num, labeltext
    num = -1

    frame = tk.Tk()
    frame.title(" ")
    frame.geometry('400x200')

    def getInput():
        global num, labeltext
        inp = inputtxt.get(1.0, "end-1c")
        if inp.isdigit():
            inp = int(inp)
            if 0 <= inp <= 2:
                num = inp
                frame.destroy()

    # TextBox Creation
    inputtxt = tk.Text(frame, height=1, width=5)
    inputtxt.pack()

    # Button Creation
    printButton = tk.Button(frame, text="Enter", command=getInput)
    printButton.pack()

    # Label Creation
    lbl = tk.Label(frame, text=labeltext)
    lbl.pack()
    frame.mainloop()
    if num == -1:
        finish()
    return num

# ********************END OF GUI CODE****************************

# original rect coords irl


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


def screw_sort(lw):
    global selected_screws
    l, w = lw
    headsize = 0
    for head in head_sizes:
        if round(w, 3) <= head:
            headindex = head_sizes.index(head)
            headsize = headindex+2
            break
    lengthsize = 0
    for s in selected_screws:
        if s[2] <= l <= s[3] and s[0] == headsize:
            lengthsize = s[1]
            break

    return headsize, lengthsize, w, l


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


def turntable_angle(stype):
    global selected_screws
    refangles = turntable_angles[:len(selected_screws)]
    for s in selected_screws:
        if stype[0] == s[0] and stype[1] == s[1]:
            return refangles[selected_screws.index(s)]


def correctplace(stype, x, y):
    for s in screwtypes[stype[0]-2]:
        if stype[1] == s[1]:
            places = [(s[i+4][0], s[i+4][1], s[i+4][2])
                      for i in range(totalplaces)]
            break
    min_diff = [get_length(place[0], place[1], x, y) for place in places]
    return min_diff.index(min(min_diff))+1


def main():
    global selected_screws, tocontinue
    try:
        if tocontinue == 0:
            pass
        else:
            selected_screws = selector()
    except:
        selected_screws = selector()
    delta.home()
    delta.allow_vision()
    time.sleep(2)
    pixel_per_mm = aruco.aruco_callibrate()
    vision.callibrate()
    rectangles = vision.get_rects()
    screwlst = [screw_sort(get_irl_dimensions(rectangle, pixel_per_mm))
                for rectangle in rectangles]
    print(screwlst)

    for rectangle in rectangles:
        screwtype = screw_sort(get_irl_dimensions(rectangle, pixel_per_mm))
        print(screwtype)
        if screwtype[1] == 0:  # if screw is not part of selected types
            continue
        old_x, old_y = np.average(rectangle, axis=0)
        x, y = rect_coords_irl(vision.circle, RADIUS, [old_x, old_y])

        # determine place position from rough x y values
        placeno = correctplace(screwtype, x, y)

        delta.allow_turntable_movement()
        delta.home_turntable()
        time.sleep(1)
        delta.move_turntable(turntable_angle(screwtype))

        delta.move_to_place(screwtype, placeno)
        time.sleep(1)
        delta.ramp()
    delta.home_turntable()
    time.sleep(1)
    tocontinue = finish()
    if tocontinue < 2:
        main()
    else:
        delta.end_connection()


if __name__ == '__main__':
    main()
