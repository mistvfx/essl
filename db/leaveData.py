import pymysql
from db import monthlyWrkHours
from datetime import date, timedelta
import datetime

def getRequests(id, month, year):
    dates = []
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT from_date, to_date FROM essl.`leave_details` WHERE ID = '%s' AND Status = 'LR' AND MONTH(from_date) = '%s' AND YEAR(from_date)='%s'"%(id, month, year))
    for data in cur.fetchall():
        from_date = data[0]
        to_date = data[1]

        if from_date == to_date:
            dates.append((from_date).strftime('%Y-%m-%d'))
        else:
            delta = to_date - from_date
            for i in range(delta.days + 1):
                dates.append((from_date + timedelta(i)).strftime('%Y-%m-%d'))

    return dates

def getPlanned(id, month, year):
    dates = []
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT from_date, to_date FROM essl.`leave_details` WHERE ID = '%s' AND Status = 'P' AND MONTH(from_date) = '%s' AND YEAR(from_date)='%s'"%(id, month, year))
    for data in cur.fetchall():
        from_date = data[0]
        to_date = data[1]

        if from_date == to_date:
            dates.append((from_date).strftime('%Y-%m-%d'))
        else:
            delta = to_date - from_date
            for i in range(delta.days + 1):
                dates.append((from_date + timedelta(i)).strftime('%Y-%m-%d'))

    return dates

def getSick(id, month, year):
    dates = []
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT from_date, to_date FROM essl.`leave_details` WHERE ID = '%s' AND Status = 'S' AND MONTH(from_date) = '%s' AND YEAR(from_date)='%s'"%(id, month, year))
    for data in cur.fetchall():
        from_date = data[0]
        to_date = data[1]

        if from_date == to_date:
            dates.append((from_date).strftime('%Y-%m-%d'))
        else:
            delta = to_date - from_date
            for i in range(delta.days + 1):
                dates.append((from_date + timedelta(i)).strftime('%Y-%m-%d'))

    return dates

def getPermission(id, month, year):
    dates = []
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT from_date, to_date FROM essl.`leave_details` WHERE ID = '%s' AND Status = 'PE' AND MONTH(from_date) = '%s' AND YEAR(from_date)='%s'"%(id, month, year))
    for data in cur.fetchall():
        from_date = data[0]
        to_date = data[1]

        if from_date == to_date:
            dates.append((from_date).strftime('%Y-%m-%d'))
        else:
            delta = to_date - from_date
            for i in range(delta.days + 1):
                dates.append((from_date + timedelta(i)).strftime('%Y-%m-%d'))

    return dates

def getDetails(month, year, id):
    details = []
    for i in id:
        detail = {'id': 0,
                  'leaveDates': [],
                  'planned': [],
                  'sick': [],
                  'leave_requests': [],
                  'permission': []}

        detail['id'] = i
        detail['leaveDates'] = monthlyWrkHours.ArtistLeaveDates(year, month, i)
        detail['planned'] = getPlanned(i, month, year)
        detail['leave_requests'] = getRequests(i, month, year)

        details.append(detail)

    return details

def grant_perm(details):
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("UPDATE essl.`leave_details` SET Status = 'P' WHERE ID = '%s' AND from_date = '%s'"%(details[0], details[1]))
    cur.close()
    db.close()
    return 1

def upload_to_db(id, from_date, to_date, reason):
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOt EXISTS essl.`leave_details` (`S_no` INT NOT NULL AUTO_INCREMENT, `ID` INT NOT NULL, `from_date` DATE NOT NULL, `to_date` DATE NOT NULL, `Reason` LONGTEXT NOT NULL, `Status` VARCHAR(45) NOT NULL, PRIMARY KEY (`S_no`));")
    cur.close()

    cur1 = db.cursor()
    try:
        cur1.execute("INSERT INTO essl.`leave_details` (ID, from_date, to_date, Reason, Status) VALUES('%s', '%s', '%s', '%s', 'LR')"%(id, from_date, to_date, reason))
        cur1.close()
        db.close()
        return 1
    except Exception as e:
        print(e)
        cur1.close()
        db.close()
        return 0
