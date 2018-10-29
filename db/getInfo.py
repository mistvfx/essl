import pymysql
from pages import table, infoPopup
from kivy.uix.popup import Popup
from kivy.uix.button import Button
import datetime

id = [0]*1
date = [None]*1

def formatDate(date):
    allDateData = list(reversed(date))
    dt = (str(allDateData[0])+"-"+str(allDateData[1])+"-"+str(allDateData[2]))
    return dt

"""class getUserInfo(Screen):
    def __init__(self, **args):
        super(loginWindow, self).__init__(**args)
        self.login()"""

def calActualWorkingHours(io, time, door):
    inTime = datetime.timedelta(); outTime = datetime.timedelta(); sumTime = datetime.timedelta(); inCorrectTime = datetime.timedelta();
    after12 = datetime.timedelta(hours=0, minutes=1, seconds=0)
    after20 = datetime.timedelta(hours=20, minutes=0, seconds=0)
    before24 = datetime.timedelta(hours=23, minutes=59, seconds=59)
    after24 = datetime.timedelta(hours=0, minutes=0, seconds=59)
    ins = []
    outT = 0
    accDoor = ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'IT', 'TRAINING-1']
    for i in range(len(io)):
        if door[i] in accDoor:
            if time[i] > after24 and io[i] == 'Out' and door[i] in accDoor and outT == 0:
                #print(time[i], io[i], door[i])
                sumTime = sumTime + time[i]
                outT = 1
            #if time[i] > after12:
            #    if io[i] == 'Out':
            #        print(time[i], time[i]-after12)
            if io[i-1] == io[i] and door[i-1] in accDoor and door[i] in accDoor:
                #print(io[i], door[i], ":", io[i+1], door[i+1])
                """inCorrectTime = time[i+1] - time[i]
                sumTime = sumTime - inCorrectTime"""
                continue
            if io[i] == 'In':
                inTime = time[i]
            elif io[i] == 'Out':
                outTime = time[i]
                sumTime = (sumTime)+(outTime-inTime)
            if time[i] > after20 and time[i] < before24:
                try:
                    if io[i] == 'In' and io[i+1] != 'Out':
                        print(time[i])
                except:
                    print(before24 - time[i])
                    sumTime = (sumTime)+(before24 - time[i])
            print(sumTime)
                    #ins.append(time[i])
    #infoPopup.AWH.append(sumTime)
    #print(max(ins))
    return sumTime
    #print(sumTime)

def calTotalWorkingHours(ios, timings, doors):
    #times = datetime.timedelta()
    intimes = []
    outtimes = []
    for i, d, j in zip(ios, doors, range(len(ios))):
        if d == 'MAINDOOR' and i == 'In':
            intimes.append(timings[j])
        elif d == 'MAINDOOR' and i == 'Out':
            outtimes.append(timings[j])

    return max(outtimes)-min(intimes)

def getUserInfo():
    StdWrkHrs = datetime.timedelta(hours=8, minutes=29, seconds=59)
    global id, date
    formattedDate = formatDate(date[int(len(date)-1)])
    #print(formattedDate)
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT IO, MTIME, MDATE, DOOR FROM essl.`%d` WHERE MDATE = '%s' ORDER BY MTIME ASC" %(id[int(len(id)-1)], formattedDate))

    ios = []
    timings = []
    doors = []

    for data in cur.fetchall():
        table.io.append(data[0])
        table.time.append(data[1])
        table.door.append(data[3])
        ios.append(data[0])
        timings.append(data[1])
        doors.append(data[3])

    totalWorkingHours = calTotalWorkingHours(ios, timings, doors)
    #infoPopup.TWH.append(totalWorkingHours)
    #print(totalWorkingHours)

    sumTime = calActualWorkingHours(ios, timings, doors)

    NonWrkHours = StdWrkHrs - sumTime
    AdditionalHours = sumTime - StdWrkHrs

    infoPopup.TWH.append(totalWorkingHours)
    infoPopup.AWH.append(sumTime)
    if sumTime < StdWrkHrs:
        infoPopup.NCH.append(NonWrkHours)
        infoPopup.ACH.append(datetime.timedelta())
    else:
        infoPopup.NCH.append(datetime.timedelta())
        infoPopup.ACH.append(AdditionalHours)

    cur.close()
    db.close()

def openPopup():
    popUpCLoseBtn = Button(text='close', size_hint=(0.35, 1))
    infoPopup.closeBtn = popUpCLoseBtn

    getUserInfo()

    tab = infoPopup.infoTab()
    popup = Popup(title="INFORMATION", content=tab, size_hint=(0.85, 0.85))
    popup.open()
    popUpCLoseBtn.bind(on_press=popup.dismiss)
