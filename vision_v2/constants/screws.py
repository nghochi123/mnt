from csv import reader

templst=[]
screwtypes=[[],[],[],[],[]]
screwtypes2=[]

try:
    with open('screw_calibration_final.csv',mode='r') as f:
        lst=reader(f)
        count=0
        for l in lst:
            if count==0:
                headers=l
                count+=1
            else:
                templst.append(l)
except:
    print('screw_calibration_final.csv not found in folder, try again!')
    exit()

totalplaces=len(headers)-4
turntable_angles=[int(a) for a in templst[-3] if a!='']   #turntable angles to turn to for diff screw types
turntable_angles.append(int(templst[-1][0]))   #angle for a full 360 degree turn
head_sizes=[float(v) for v in templst[-6] if v!='']   #screw head size ranges

for type in templst:
    if type[0]==type[1]==type[2]==type[3]=='':
        break
    h,l,l_short,l_long=type[0],type[1],type[2],type[3]
    h,l,l_short,l_long=int(h),int(l),float(l_short),float(l_long)
    toappend=[h,l,l_short,l_long]

    for i in range(totalplaces):
        lst=type[i+4].split(',')
        try:
            lst[0],lst[1],lst[2]=int(lst[0]),int(lst[1]),int(lst[2])
        except:
            pass
        toappend.append(lst)

    screwtypes[h-2].append(toappend)

screwstrlst=[]
for h in screwtypes:
    for s in h:
        screwtypes2.append(s)
        screwstr='M'+str(s[0])+','+str(s[1])+'mm'
        while len(screwstr)<7:
            screwstr+=' '
        screwstrlst.append(screwstr)