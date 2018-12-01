import pymysql
import datetime
from pages import Calendar
from db import monthlyWrkHours

id = [0]*1
def getDayMonthYear(date):
    return (date.day, date.month, date.year)

def calActualWorkingHours(io, time, door):
    sumTime = datetime.timedelta()
    accDoor = ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'TRAINING-1', 'IT', 'HR']
    i = 0

    while i < len(io):
        try:
            if door[i] in accDoor and io[i] == 'In' and door[i+1] == door[i] and io[i+1] == 'Out':
                sumTime += (time[i+1] - time[i])
                i += 2
                continue

            elif door[i] == 'PERMISSION':
                sumTime -= time[i]

        except:
            break

        i += 1

    return sumTime

def calMon(id, date):
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()

    cur.execute("SELECT IO, MTIME, DOOR FROM essl.`%d` WHERE MDATE = '%s' ORDER BY MTIME ASC" %(id, date))

    ios = []
    timings = []
    doors = []

    for data in cur.fetchall():
        ios.append(data[0])
        timings.append(data[1])
        doors.append(data[2])

    ActWorHrs = calActualWorkingHours(ios, timings, doors)
    cur.close()
    db.close()
    return ActWorHrs


def getUserTime():
    StdWrkHrs = datetime.timedelta(hours=8, minutes=29, seconds=59)
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT DISTINCT(MDATE) FROM essl.`%d` ORDER BY MDATE ASC" %(id[int(len(id)-1)]))
    cur1 = db.cursor()
    for mdate in cur.fetchall():
        cur1.execute("SELECT IO, MTIME, DOOR FROM essl.`%d` WHERE MDATE = '%s' ORDER BY MTIME ASC" %(id[int(len(id)-1)], mdate[0]))

        ios = []
        timings = []
        doors = []

        for data in cur1.fetchall():
            ios.append(data[0])
            timings.append(data[1])
            doors.append(data[2])

        DMY = getDayMonthYear(mdate[0])
        ActWorHrs = calActualWorkingHours(ios, timings, doors)
        if(ActWorHrs > StdWrkHrs):
            Calendar.aboveSWH.append(DMY)
        elif ActWorHrs < StdWrkHrs and ActWorHrs > datetime.timedelta(hours=3, minutes=0, seconds=0):
            Calendar.belowSWH.append(DMY)
        else:
            Calendar.leaves.append(DMY)

    monthlyWrkHours.getHolidays()

    cur.close()
    cur1.close()
    db.close()
