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
    inTime = datetime.timedelta(); outTime = datetime.timedelta(); sumTime = datetime.timedelta();
    accDoor = ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM']
    for i in range(len(io)):
        if door[i] in accDoor:
            if io[i] == 'In':
                inTime = time[i]
            elif io[i] == 'Out':
                outTime = time[i]
                sumTime = (sumTime)+(outTime-inTime)
    #infoPopup.AWH.append(sumTime)
    print(sumTime)
    return sumTime
    #print(sumTime)

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

    totalWorkingHours = (max(timings)-min(timings))
    #infoPopup.TWH.append(totalWorkingHours)
    #print(totalWorkingHours)

    sumTime = calActualWorkingHours(ios, timings, doors)

    NonWrkHours = StdWrkHrs - sumTime
    AdditionalHours = sumTime - StdWrkHrs

    infoPopup.TWH.append(totalWorkingHours)
    infoPopup.AWH.append(sumTime)
    if sumTime < StdWrkHrs:
        infoPopup.NCH.append(NonWrkHours)
        infoPopup.ACH.append(datetime.time())
    else:
        infoPopup.NCH.append(datetime.time())
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
