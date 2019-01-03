import pymysql
from db import getInfo, calcWrkHrs, monthlyWrkHours

def checkCredentials(username, password):
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT ID, Name, Department, Password FROM essl.user_master WHERE Status = 'OPEN' ")

    for data in cur.fetchall():
        if username == "" or password == "":
            return 0
        if username in str(data[0]) and password in str(data[3]):
            if str(data[2]) == 'ADMIN':
                cur.close()
                db.close()
                return 1
            elif str(data[2]) != 'ADMIN':
                from pages import userPage
                userPage.id = (data[0])
                userPage.user = (str(data[1]))
                userPage.department = (str(data[2]))
                getInfo.id.append(int(data[0]))
                calcWrkHrs.id.append(int(data[0]))
                calcWrkHrs.getUserTime()
                monthlyWrkHours.id.append(int(data[0]))
                cur.close()
                db.close()
                return ([2, data[0], data[1], data[2]])

    cur.close()
    db.close()
    return 0
