import pymysql
import datetime
from db import calcWrkHrs

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

    return sumWrkHrs
