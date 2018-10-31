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
    after20 = datetime.timedelta(hours=20, minutes=0, seconds=0)
    before24 = datetime.timedelta(hours=23, minutes=59, seconds=59)
    after24 = datetime.timedelta(hours=0, minutes=0, seconds=59)
    before5 = datetime.timedelta(hours=6, minutes=0, seconds=0)
    accDoor = ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'TRAINING-1', 'IT', 'HR']
    for i in range(len(io)):
        if door[i] in accDoor:
            if time[i] > after24 and time[i] < before5 and io[i] == 'Out' and door[i] in accDoor:
                sumTime = sumTime + time[i]
                outT = 1
            if io[i-1] == io[i] and door[i-1] in accDoor and door[i] in accDoor:
                continue
            if io[i] == 'In':
                inTime = time[i]
            elif io[i] == 'Out':
                outTime = time[i]
                sumTime = (sumTime)+(outTime-inTime)
            if time[i] > after20 and time[i] < before24:
                try:
                    if io[i] == 'In' and io[i+1] != 'Out':
                        pass
                except:
                    sumTime = (sumTime)+(before24 - time[i])
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
        else:
            Calendar.belowSWH.append(DMY)

    monthlyWrkHours.getHolidays()

    cur.close()
    cur1.close()
    db.close()
