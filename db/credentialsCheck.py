import pymysql
from db import getInfo, calcWrkHrs, monthlyWrkHours

def checkCredentials(username, password):
    from db.essl_credentials import credentials
    db = pymysql.connect(credentials['address'], credentials['username'], credentials['password'], credentials['db'], autocommit=True, connect_timeout=1)
    cur = db.cursor()
    try:
        cur.execute("SELECT ID, Name, Department, Password, Level FROM essl.user_master WHERE Status = 'OPEN'")
    except pymysql.err.ProgrammingError:
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_master(ID INT, Name VARCHAR(225) NOT NULL, Department VARCHAR(50), Password VARCHAR(225) NOT NULL, Level CHAR NOT NULL DEFAULT '5', email VARCHAR(225), Status VARCHAR(10) NOT NULL DEFAULT 'OPEN', PRIMARY KEY (ID));")
        cursor.execute("INSERT INTO essl.user_master VALUES(9989, 'ADMIN', 'ADMIN', 9899, '1', 'mett@mistvfx.local', 'OPEN')")
        cur.execute("SELECT ID, Name, Department, Password, Level FROM essl.user_master WHERE Status = 'OPEN'")

    for data in cur.fetchall():
        if username == "" or password == "":
            return 0
        if username in str(data[0]) and password in str(data[3]):
            if str(data[2]) == 'ADMIN':
                cur.close()
                db.close()
                return 1
            elif str(data[2]) != 'ADMIN':
                from pages import userPage, Calendar, infoPopup, table
                Calendar.id = data[0]
                infoPopup.id = data[0]
                table.id = data[0]
                table.lvl = data[4]
                userPage.id = (data[0])
                userPage.user = (str(data[1]))
                userPage.department = (str(data[2]))
                getInfo.id.append(int(data[0]))
                calcWrkHrs.id.append(int(data[0]))
                calcWrkHrs.getUserTime()
                monthlyWrkHours.id.append(int(data[0]))
                cur.close()
                db.close()
                return 2

    cur.close()
    db.close()
    return 0


#db = pymysql.connect(credentials['address'], credentials['username'], credentials['password'], credentials['db'], autocommit=True, connect_timeout=1)
