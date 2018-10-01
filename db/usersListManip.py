import pymysql
from pages import usersList

def getUserInfo():
    db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
    cur = db.cursor()
    cur.execute("SELECT ID, Name, Department, Password FROM essl.user_master WHERE Status = 'OPEN' ")

    for data in cur.fetchall():
        usersList.id.append(data[0])
        usersList.names.append(data[1])
