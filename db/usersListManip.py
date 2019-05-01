import pymysql
from pages import usersList
from db.essl_credentials import credentials

def getUserInfo():
    db = pymysql.connect(credentials['address'], credentials['username'], credentials['password'], credentials['db'], autocommit=True, connect_timeout=1)
    cur = db.cursor()
    cur.execute("SELECT ID, Name, Department, Password FROM essl.user_master WHERE Status = 'OPEN' AND Name != 'ADMIN'")

    userData = { 'artistId': [],
                'artistName': [],
                'artistDept': []}

    for data in cur.fetchall():
        usersList.id.append(data[0])
        usersList.names.append(data[1])
        userData['artistId'].append(data[0])
        userData['artistName'].append(data[1])
        userData['artistDept'].append(data[2])

    cur.close()
    db.close()
    return userData

def checkMail(id):
    db = pymysql.connect(credentials['address'], credentials['username'], credentials['password'], credentials['db'], autocommit=True, connect_timeout=1)
    cur = db.cursor()
    cur.execute("SELECT email FROM essl.`user_master` WHERE ID = '%d'"%(int(id)))
    if cur.fetchone()[0] == None:
        cur.close()
        db.close()
        return 0
    else:
        cur.close()
        db.close()
        return 1

def submit_email(id, email):
    db = pymysql.connect(credentials['address'], credentials['username'], credentials['password'], credentials['db'], autocommit=True, connect_timeout=1)
    cur = db.cursor()
    try:
        cur.execute("UPDATE essl.`user_master` SET email = '%s' WHERE ID = '%d'"%(email, int(id)))
    except Exception as e:
        print(e)

    cur.close()
    db.close()


#192.168.1.234
