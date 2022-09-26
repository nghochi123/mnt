import tkinter as tk
from constants.screws import screwtypes, screwstrlst, screwtypes2

screw_selection = []


def selector():
    root = tk.Tk()
    root.title('Screw Selection')
    root.minsize(200, 200)

    window = tk.Tk()
    window.title('Display selected screws')

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


print(selector())
