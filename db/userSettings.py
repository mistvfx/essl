import pymysql
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.spinner import Spinner
from kivy.graphics import *
from kivy.properties import *

Builder.load_string("""
<TimingFix>:
    orientation: 'vertical'
    spacing: 5

    Spinner:
        text: 'DOOR'
        font_name: 'fonts/moon-bold.otf'
        values: ('IT', 'MM', 'PAINT', 'ROTO', 'HR', 'CONFERENCE ROOM', 'MAINDOOR', 'TRAINING-1', 'SERVER ROOM', 'ASLAM SIR', 'BACKDOOR')
        size_hint: (0.65, 0.25)
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_text: root.Dept(self.text)

    Spinner:
        text: 'IN/OUT'
        values: ('In', 'Out')
        font_name: 'fonts/moon-bold.otf'
        size_hint: (0.65, 0.25)
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_text: root.IO(self.text)

    TextInput:
        id: time
        hint_text: 'HH:MM:SS'
        font_size: self.size[1]/2.5
        padding: [self.size[1]*2.5, self.size[1]/5.0, 0, 0]
        font_name: 'fonts/moon-bold.otf'
        multiline: False
        size_hint: (0.65, 0.25)
        pos_hint: {'center_x': .5, 'center_y': .5}

    Button:
        text: 'ADD TIME'
        font_name: 'fonts/moon-bold.otf'
        size_hint: (0.65, 0.25)
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: root.Time(time.text)

<Permission>:
    size_hint: (0.5, 0.10)
    anchor_x: 'center'
    anchor_y: 'center'
    BoxLayout:
        TextInput:
            hint_text: 'HOURS (HH:MM:SS)'
            multiline: False
        Button:
            text: 'Submit Permission Time'

<SettingsTabs>:
    TabbedPanelItem:
        text: 'TIMING FIX'
        font_name: 'fonts/moon-bold.otf'
        TimingFix:

    TabbedPanelItem:
        text: 'PERMISSION'
        font_name: 'fonts/moon-bold.otf'
        Permission:

<userSettingPop>:
    size_hint: (0.75, 0.65)

    SettingsTabs:
        do_default_tab: False
""")

class SettingsTabs(TabbedPanel):
    pass

class TimingFix(BoxLayout):
    pass

class Permission(AnchorLayout):
    pass

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
        self.title = (artistID.split(":")[1] + " || " + date)
        self.font_name = 'fonts/moon-bold.otf'
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
