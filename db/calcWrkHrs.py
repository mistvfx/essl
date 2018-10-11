import pymysql
import datetime
from pages import Calendar
from db import monthlyWrkHours

id = [0]*1
def getDayMonthYear(date):
    return (date.day, date.month, date.year)

def calActualWorkingHours(io, time, door):
    #getDayMonthYear(date)
    inTime = datetime.timedelta(); outTime = datetime.timedelta(); sumTime = datetime.timedelta();
    accDoor = ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'TRAINING-1']
    for i in range(len(io)):
        if door[i] in accDoor:
            if io[i-1] == io[i] and door[i-1] in accDoor and door[i] in accDoor:
                print(io[i], door[i], ":", io[i+1], door[i+1])
                """inCorrectTime = time[i+1] - time[i]
                sumTime = sumTime - inCorrectTime"""
                continue
            if io[i] == 'In':
                inTime = time[i]
            elif io[i] == 'Out':
                outTime = time[i]
                sumTime = (sumTime)+(outTime-inTime)
    return sumTime
    #print(sumTime)

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
        else:
            Calendar.belowSWH.append(DMY)

    monthlyWrkHours.getHolidays()

    cur.close()
    cur1.close()
    db.close()
