"""from meza import io
import pandas as pd

records = list(io.read_mdb('/home/matrix/Documents/Access.mdb', table='acc_monitor_log'))
userInfo = list(io.read_mdb('/home/matrix/Documents/Access.mdb', table='USERINFO'))
#print(records)
data = pd.DataFrame(records)
userinfo = pd.DataFrame(userInfo)
#print(data['card_no'], data['time'], data['pin'], data['event_point_name'], data['event_point_id'], data['device_id'])
time = data['time']
pin = data['pin']
idnum = userinfo['Badgenumber']
id = userinfo['ZIP']

for i in range(len(pin)):
    for j in range(len(idnum)):
        if pin[i] == idnum[j] and id[j] != "":
            print(pin[i], id[j])
            break
    if pin[i] == idnum[j] and id[j] != "":
            print(pin[i], id[j])
            break
"""

"""import sys
from zklib import zklib
import time
from zklib import zkconst

zk = zklib.ZKLib("10.10.5.83", 4370)
ret = zk.connect()
print("connection:", ret)"""

"""import sys
import os
sys.path.insert(1,os.path.abspath("./pyzk"))
from zk import ZK, const

conn = None
zk = ZK('10.10.5.83', port=4370, timeout=10)
try:
    print ('Connecting to device ...')
    conn = zk.connect()
    print(conn)
except Exception as e:
    print(e)
"""
