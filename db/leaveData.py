import pymysql
from db import monthlyWrkHours
import datetime
from datetime import date, timedelta, datetime

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
        detail['permission'] = getPermission(i, month, year)

        details.append(detail)

    return details

def grant_perm(details):
    from db import ExchangeMail
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("UPDATE essl.`leave_details` SET Status = 'P' , acc_date = '%s' WHERE ID = '%s' AND from_date = '%s'"%(datetime.today().strftime('%Y-%m-%d'), details[0], details[1]))
    ExchangeMail.accepted_mail(details[0], details[1])
    cur.close()
    db.close()
    return 1

def decline_perm(details):
    from db import ExchangeMail
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("UPDATE essl.`leave_details` SET Status = 'R' WHERE ID = '%s' AND from_date = '%s'"%(details[0], details[1]))
    ExchangeMail.declined_mail(details[0], details[1])
    cur.close()
    db.close()
    return 1

def upload_to_db(id, from_date, to_date, type, reason):
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS essl.`leave_details` (`S_no` int(11) NOT NULL AUTO_INCREMENT, `ID` int(11) NOT NULL, `from_date` date NOT NULL, `to_date` date NOT NULL, `Reason` longtext NOT NULL, `Status` varchar(45) NOT NULL, `Type` varchar(45) DEFAULT NULL, `app_date` date DEFAULT NULL, `acc_date` date DEFAULT NULL, PRIMARY KEY (`S_no`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;")
    cur.close()

    cur1 = db.cursor()
    cur2 = db.cursor()
    try:
        types = type.split(":")
        cur2.execute("UPDATE essl.`leaves` SET EL = EL-%d, CL = CL-%d WHERE ID = '%s'"%(int(types[0].split("-")[1]), int(types[1].split("-")[1]), id))
    except Exception as e:
        print(e)
        types = type.split("-")
        if types[0] == 'EL':
            cur2.execute("UPDATE essl.`leaves` SET EL = EL-%d WHERE ID = '%s'"%(int(types[1]), id))
        elif types[0] == 'CL':
            cur2.execute("UPDATE essl.`leaves` SET CL = CL-%d WHERE ID = '%s'"%(int(types[1]), id))
    try:
        cur1.execute("INSERT INTO essl.`leave_details` (ID, from_date, to_date, Reason, Status, Type, app_date) VALUES('%s', '%s', '%s', '%s', 'LR', '%s', '%s')"%(id, from_date, to_date, reason, type, datetime.today().strftime('%Y-%m-%d')))
        cur1.close()
        db.close()
        return 1
    except Exception as e:
        print(e)
        cur1.close()
        db.close()
        return 0

def getFeedback(id):
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT from_date, to_date, Type, Status, app_date, Reason FROM essl.`leave_details` WHERE ID = '%s'"%(id))
    data = cur.fetchall()
    cur.close()
    db.close()
    return data

def get_leaves_data(id):
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT EL, CL FROM essl.`leaves` WHERE ID = '%s'"%(id))
    data = cur.fetchone()
    cur.close()
    db.close()
    return data
