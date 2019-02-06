import pymysql
from pages import table, infoPopup
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
import datetime

id = [0]*1
date = ""

def formatDate(date):
    allDateData = list(reversed(date.split(":")))
    dt = (str(allDateData[0]) +"-"+ str(allDateData[1]).zfill(2) +"-"+ str(allDateData[2]))
    return dt

"""class getUserInfo(Screen):
    def __init__(self, **args):
        super(loginWindow, self).__init__(**args)
        self.login()"""

def calActualWorkingHours(io, time, door, lvl):
    sumTime = datetime.timedelta()
    level = { '1': ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'TRAINING-1', 'IT', 'HR', 'SERVER ROOM', 'STORE'],
            '2': ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'TRAINING-1', 'HR'],
            '3': ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'TRAINING-1'],
            '4': ['MM', 'ROTO', 'CONFERENCE ROOM'],
            '5': ['ROTO', 'CONFERENCE ROOM'],
            '6': ['MM', 'CONFERENCE ROOM', 'TRAINING-1'],
            '7': ['ROTO', 'CONFERENCE ROOM', 'TRAINING-1']}
    i = 0

    while i < len(io):
        try:
            if door[i] in level[lvl] and io[i] == 'In' and door[i+1] == door[i] and io[i+1] == 'Out':
                sumTime += (time[i+1] - time[i])
                i += 2
                continue

            elif door[i] == 'PERMISSION':
                sumTime -= time[i]

        except:
            continue

        i += 1

    return sumTime

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

def getUserInfo(id, date):
    StdWrkHrs = datetime.timedelta(hours=8, minutes=29, seconds=59)
    formattedDate = formatDate(date)
    #print(formattedDate, date)
    db = pymysql.connect("10.10.5.60", "mcheck", "mcheck@123", "essl", autocommit=True, connect_timeout=1)
    cur = db.cursor()
    cur.execute("SELECT IO, MTIME, MDATE, DOOR, AccType FROM essl.`%d` WHERE MDATE = '%s' ORDER BY MTIME ASC" %(id, formattedDate))

    ios = []
    timings = []
    doors = []

    for data in cur.fetchall():
        #table.io.append(data[0])
        #table.time.append(data[1])
        #table.door.append(data[3])
        #table.accType.append(data[4])
        ios.append(data[0])
        timings.append(data[1])
        doors.append(data[3])

    cur1 = db.cursor()
    cur1.execute("SELECT Level FROM essl.user_master WHERE ID = '%d'"%(id))

    for data in cur1.fetchall():
        lvl = data[0]

    table.lvl = lvl
    table.id = id
    table.date = formattedDate

    totalWorkingHours = calTotalWorkingHours(ios, timings, doors)

    sumTime = calActualWorkingHours(ios, timings, doors, lvl)

    NonWrkHours = StdWrkHrs - sumTime
    AdditionalHours = sumTime - StdWrkHrs

    info = {'TWH': totalWorkingHours,
            'AWH': sumTime}
    infoPopup.TWH = (totalWorkingHours)
    infoPopup.AWH = (sumTime)
    if sumTime < StdWrkHrs:
        infoPopup.NCH = (NonWrkHours)
        info['NCH'] = NonWrkHours
        info['ACH'] = datetime.timedelta()
        infoPopup.ACH = (datetime.timedelta())
    else:
        infoPopup.NCH = (datetime.timedelta())
        info['NCH'] = datetime.timedelta()
        info['ACH'] = AdditionalHours
        infoPopup.ACH = (AdditionalHours)

    cur.close()
    db.close()
    return info

def get_IO_info(id, date):
    #formattedDate = formatDate(date)
    db = pymysql.connect("10.10.5.60", "mcheck", "mcheck@123", "essl", autocommit=True, connect_timeout=1)
    cur = db.cursor()
    cur.execute("SELECT IO, MTIME, MDATE, DOOR, AccType FROM essl.`%d` WHERE MDATE = '%s' ORDER BY MTIME ASC" %(id, date))

    #ios = []
    #timings = []
    #doors = []

    del table.io[:]; del table.time[:]; del table.door[:]; del table.accType[:]

    for data in cur.fetchall():
        table.io.append(data[0])
        table.time.append(data[1])
        table.door.append(data[3])
        table.accType.append(data[4])

def openPopup(ua):
    global id, date

    db = pymysql.connect("10.10.5.60", "mcheck", "mcheck@123", "essl", autocommit=True, connect_timeout=1)
    cur = db.cursor()
    cur.execute("SELECT Name FROM essl.user_master WHERE ID = '%d'"%(id[len(id)-1]))
    name = cur.fetchone()

    getUserInfo(id[len(id)-1], date)

    if ua == 'user':
        pass
        #tab = infoPopup.InfoTab(name, date)
    elif ua == 'admin':
        tab = infoPopup.InfoTabAdmin(name, date)

    #popup = ModalView(size_hint=(0.85, 0.85))
    #popup.add_widget(tab)
    #title="{}||{}".format(name[0], formatDate(date[len(date)-1])), content=tab,
    #popup.open()
