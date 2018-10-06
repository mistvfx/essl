import pymysql
import datetime
from db import calcWrkHrs
from pages import Calendar

id = []

def calMonWrkHrs(year, month):
    global id
    sumWrkHrs = datetime.timedelta()
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT DISTINCT(MDate) from essl.`%d` WHERE YEAR(MDate) = '%d' AND MONTH(MDate) = '%d'" %(id[len(id)-1], int(year), month))
    for date in cur.fetchall():
        actWrkHrs = calcWrkHrs.calMon(id[len(id)-1], date[0])
        sumWrkHrs += actWrkHrs

    cur.close()
    db.close()
    return sumWrkHrs

def getHolidays():
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT * FROM essl.month_details")

    holidays = []

    for data in cur.fetchall():
        if data[2] == 'HOLIDAY':
            holidays.append([data[0], data[1]])
            Calendar.holidays.append([data[0], data[1]])

    cur.close()
    db.close()
    return holidays
