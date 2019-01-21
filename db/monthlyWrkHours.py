import pymysql
import datetime
import calendar
from db import calcWrkHrs
from pages import Calendar

id = []

def calMonWrkHrs(year, month):
    global id
    sumWrkHrs = datetime.timedelta()
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT DISTINCT(MDate) from essl.`%d` WHERE YEAR(MDate) = '%d' AND MONTH(MDate) = '%d'" %(id[len(id)-1], int(year), int(month)))
    for date in cur.fetchall():
        actWrkHrs = calcWrkHrs.calMon(id[len(id)-1], date[0])
        sumWrkHrs += actWrkHrs

    cur.close()
    db.close()
    return sumWrkHrs

def calMonTotWrkHrs(year, month):
    global id
    totWrkHrs = datetime.timedelta()
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur1 = db.cursor()
    cur2 = db.cursor()
    cur.execute("SELECT DISTINCT(MDate) from essl.`%d` WHERE YEAR(MDate) = '%d' AND MONTH(MDate) = '%d'" %(id[len(id)-1], int(year), int(month)))
    for date in cur.fetchall():
        #print(date[0].day)
        cur1.execute("SELECT MIN(MTIME), MAX(MTIME) FROM essl.`%d` WHERE MDate = '%s'" %(id[len(id)-1], date[0]))
        cur2.execute("SELECT DOOR, MTIME FROM essl.`%d` WHERE MDate = '%s'" %(id[len(id)-1], date[0]))

        for data in cur1.fetchall():
            for data1 in cur2.fetchall():
                if data1[0] == 'PERMISSION':
                    totWrkHrs -= data1[1]
            totWrkHrs += (data[1]-data[0])

    cur.close()
    cur1.close()
    db.close()

    return totWrkHrs

def calArtistLeave(year, month, d):
    global id
    month = int(month)
    d = int(d)

    totalDays = calendar.monthrange(year, month)[1]
    Month = calendar.monthcalendar(year, month)
    leave = 0
    hDays = 0
    holidays = getHolidays()
    actualWorkingDays = []

    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur1 = db.cursor()
    cur.execute("SELECT DISTINCT(MDate) from essl.`%d` WHERE YEAR(MDate) = '%d' AND MONTH(MDate) = '%d'" %(id[len(id)-1], int(year), int(month)))
    for date in cur.fetchall():
        actualWorkingDays.append(date[0].day)
        actWrkHrs = calcWrkHrs.calMon(id[len(id)-1], date[0])
        if actWrkHrs < datetime.timedelta(hours=3, minutes=0, seconds=0):
            leave += 1
            Calendar.leaves.append([date[0].day, date[0].month, date[0].year])

    for week in Month:
        for day in week:
            for i in range(len(holidays)):
                if day == holidays[i][0] and month == holidays[i][1] and year == holidays[i][2]:
                    hDays += 1
            if day == week[6] or day in actualWorkingDays or day == 0:
                continue
            elif day == d:
                return leave - hDays
            else :
                leave += 1
                #print('leave day', day)
                Calendar.leaves.append([day, month, year])

    #print('leave', leave, hDays)
    cur.close()
    db.close()
    return leave - hDays

def calArtistLeaveMon(year, month):
    global id

    totalDays = calendar.monthrange(year, month)[1]
    Month = calendar.monthcalendar(year, month)
    leave = 0
    hDays = 0
    holidays = getHolidays()
    actualWorkingDays = []

    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT DISTINCT(MDate) from essl.`%d` WHERE YEAR(MDate) = '%d' AND MONTH(MDate) = '%d'" %(id[len(id)-1], int(year), int(month)))
    for date in cur.fetchall():
        actualWorkingDays.append(date[0].day)

    for week in Month:
        for day in week:
            for i in range(len(holidays)):
                if day == holidays[i][0] and month == holidays[i][1] and year == holidays[i][2]:
                    hDays += 1
            if day == week[6] or day in actualWorkingDays or day == 0:
                continue
            else :
                leave += 1

    cur.close()
    db.close()
    return leave - hDays

def ArtistLeaveDates(year, month, id):
    from datetime import datetime
    today = datetime.today()
    if year > today.year:
        return None
    elif year == today.year and month > today.month:
        return None
    leave_dates = []
    sundays = []
    holidays = []

    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()

    Month = calendar.monthcalendar(year, month)

    for week in Month:
        for day in week:
            for i in range(len(holidays)):
                if day == holidays[i][0] and month == holidays[i][1] and year == holidays[i][2]:
                    holidays.append("{}-{}-{}".format(year, month, day))
            if day == week[6] and day != 0:
                sundays.append("{}-{}-{}".format(year, month, day))
    #print(sundays)

    def formatDate(day):
        return ("{}-{}-{}".format(year, str(month).zfill(2), str(day).zfill(2)))

    allDays = calendar.monthrange(int(year), int(month))[1]
    for d in range(1, allDays+1):
        date = formatDate(d)
        if d == today.day and month == today.month and year == today.year:
            break
        try:
            cur.execute("SELECT SNum from essl.`%d` WHERE MDate = '%s'"%(id, date))
            if cur.fetchall() == () and date not in sundays and date not in holidays:
                leave_dates.append(date)
        except Exception as e:
            print(e)

    return leave_dates

def getHolidays():
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT * FROM essl.month_details")

    holidays = []

    for data in cur.fetchall():
        if data[3] == 'HOLIDAY':
            holidays.append([data[0], data[1], data[2]])
            Calendar.holidays.append([data[0], data[1], data[2]])

    cur.close()
    db.close()
    return holidays
