import pymysql
from pages import userPage
from db import getInfo, calcWrkHrs, monthlyWrkHours

def checkCredentials(username, password):
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT ID, Name, Department, Password FROM essl.user_master WHERE Status = 'OPEN' ")

    for data in cur.fetchall():
        if username == "" and password == "":
            return 0
        if username in str(data[0]) and password in str(data[3]):
            if str(data[2]) == 'ADMIN':
                cur.close()
                db.close()
                return 1
            else:
                userPage.id.append(int(data[0]))
                getInfo.id.append(int(data[0]))
                calcWrkHrs.id.append(int(data[0]))
                monthlyWrkHours.id.append(int(data[0]))
                userPage.user.append(str(data[1]))
                userPage.department.append(str(data[2]))
                calcWrkHrs.getUserTime()
                cur.close()
                db.close()
                return 2

    cur.close()
    db.close()
    return 0
