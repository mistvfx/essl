import pymysql
import datetime
from pages import Calendar
from db.essl_credentials import credentials
from db import monthlyWrkHours

id = [0]*1
def getDayMonthYear(date):
    return (date.day, date.month, date.year)

def calActualWorkingHours(io, time, door, lvl):
    global id
    sumTime = datetime.timedelta()
    level = { '1': ['MM', 'ROTO', 'PAINT', 'CONFERENCEROOM', 'TRAINING', 'IT', 'HR', 'SERVER', 'STORE'],
            '2': ['MM', 'ROTO', 'PAINT', 'CONFERENCEROOM', 'TRAINING', 'HR'],
            '3': ['MM', 'ROTO', 'PAINT', 'CONFERENCEROOM', 'TRAINING'],
            '4': ['MM', 'ROTO', 'CONFERENCEROOM'],
            '5': ['ROTO', 'CONFERENCEROOM'],
            '6': ['MM', 'CONFERENCEROOM', 'TRAINING'],
            '7': ['ROTO', 'CONFERENCEROOM', 'TRAINING']}
    i = 0

    while i < len(io):
        try:
            if door[i] in level[lvl] and io[i].lower() == 'in' and door[i+1] == door[i] and io[i+1].lower() == 'out':
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
    db = pymysql.connect(credentials['address'], credentials['username'], credentials['password'], credentials['db'], autocommit=True, connect_timeout=1)
    cur = db.cursor()

    cur.execute("SELECT IO, MTIME, DOOR FROM essl.`%d` WHERE MDATE = '%s' ORDER BY MTIME ASC" %(id, date))

    ios = []
    timings = []
    doors = []

    for data in cur.fetchall():
        ios.append(data[0])
        timings.append(data[1])
        doors.append(data[2])

    cur1 = db.cursor()
    cur1.execute("SELECT Level FROM essl.user_master WHERE ID = '%d'"%(id))

    for data in cur1.fetchall():
        lvl = data[0]

    ActWorHrs = calActualWorkingHours(ios, timings, doors, lvl)
    cur.close()
    db.close()
    return ActWorHrs


def getUserTime():
    StdWrkHrs = datetime.timedelta(hours=8, minutes=29, seconds=59)
    db = pymysql.connect(credentials['address'], credentials['username'], credentials['password'], credentials['db'], autocommit=True, connect_timeout=1)
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

        cur1 = db.cursor()
        cur1.execute("SELECT Level FROM essl.user_master WHERE ID = '%d'"%(id[int(len(id)-1)]))

        for data in cur1.fetchall():
            lvl = data[0]

        DMY = getDayMonthYear(mdate[0])
        ActWorHrs = calActualWorkingHours(ios, timings, doors, lvl)
        if(ActWorHrs > StdWrkHrs):
            Calendar.aboveSWH.append(DMY)
        elif ActWorHrs < StdWrkHrs and ActWorHrs > datetime.timedelta(hours=3, minutes=0, seconds=0):
            Calendar.belowSWH.append(DMY)
        else:
            Calendar.leaves.append(DMY)

        level = { '1': ['MM', 'ROTO', 'PAINT', 'CONFERENCEROOM', 'TRAINING', 'IT', 'HR', 'SERVER', 'STORE'],
                '2': ['MM', 'ROTO', 'PAINT', 'CONFERENCEROOM', 'TRAINING', 'HR'],
                '3': ['MM', 'ROTO', 'PAINT', 'CONFERENCEROOM', 'TRAINING'],
                '4': ['MM', 'ROTO', 'CONFERENCEROOM'],
                '5': ['ROTO', 'CONFERENCEROOM'],
                '6': ['MM', 'CONFERENCEROOM', 'TRAINING'],
                '7': ['ROTO', 'CONFERENCEROOM', 'TRAINING']}

        i = 0
        while i < len(ios):
            try:
                if doors[i] in level[lvl] and ios[i].lower() == 'in' and doors[i+1] == doors[i] and ios[i+1].lower() == 'out':
                    pass
                elif doors[i-1] in level[lvl] and ios[i-1].lower() == 'in' and doors[i-1] == doors[i] and ios[i].lower() == 'out':
                    pass
                elif doors[i] in level[lvl]:
                    Calendar.reg.append(DMY)
                    break
            except:
                pass
            i += 1

    monthlyWrkHours.getHolidays()

    cur.close()
    cur1.close()
    db.close()
