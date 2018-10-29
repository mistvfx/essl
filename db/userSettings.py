import pymysql
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.graphics import *
from kivy.properties import *

Builder.load_string("""
<userSettingPop>:
    size_hint: (0.75, 0.65)
    BoxLayout:
        orientation: 'vertical'

        Spinner:
            text: 'DOOR'
            values: ('IT', 'MM', 'PAINT', 'ROTO', 'HR', 'CONFERENCE ROOM', 'MAINDOOR', 'TRAINING-1', 'SERVER ROOM', 'ASLAM SIR', 'BACKDOOR')
            size_hint_y: None
            on_text: root.Dept(self.text)

        Spinner:
            text: 'IN/OUT'
            values: ('In', 'Out')
            size_hint_y: None
            on_text: root.IO(self.text)

        TextInput:
            id: time
            text_hint: 'HH:MM:SS'
            size_hint_y: 0.20

        Button:
            text: 'ADD TIME'
            size_hint_y: None
            on_release: root.Time(time.text)

""")

def getTimings(artistID):
    print(artistID)

def formatDate(date):
    Dt = date.split(".")
    return str("-".join(list(reversed(Dt))))

class userSettingPop(Popup):
    def __init__(self, artistID, date):
        super().__init__()
        self.date = formatDate(date)
        self.id = artistID.split(":")[0]
        self.title = (artistID.split(":")[1] + " :: " + date)
    #def __init__(self, **args):
    #    super(userSettingPop, self).__init__(**args)

    def Dept(self, dept):
        self.door = dept

    def IO(self, io):
        self.io = io

    def Time(self, time):
        print(self.id, self.door, self.io, time, self.date)
        db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
        cur = db.cursor()
        cur.execute("INSERT INTO essl.%d (IO, MTIME, MDATE, DOOR) VALUES('%s', '%s', '%s', '%s')" %(int(self.id), self.io, time, self.date, self.door))
        cur.close()
        db.close()
