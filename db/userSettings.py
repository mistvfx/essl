import pymysql
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.properties import *

from pages import Dialog

Date = ""
id = 0

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
            id: hours
            hint_text: 'HOURS (HH:MM:SS)'
            multiline: False
        Button:
            text: 'Submit Permission Time'
            on_release: root.addPermTime(hours.text)

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
    def Dept(self, dept):
        self.door = dept

    def IO(self, io):
        self.io = io

    def Time(self, time):
        global Date, id
        db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
        cur = db.cursor()
        try:
            cur.execute("INSERT INTO essl.%d (IO, MTIME, MDATE, DOOR) VALUES('%s', '%s', '%s', '%s')" %(int(id), self.io, time, Date, self.door))
        except:
            def callback(instance):
                if instance.text == 'OK':
                    pop.dismiss()
                    return 0
            closePopBtn = Button(text="OK", size_hint=(1, 0.25))
            closePopBtn.bind(on_release=callback)
            pop = Dialog.dialog("Error !!!", "Please Provide valid information !!", closePopBtn)
            pop.open()
        cur.close()
        db.close()

class Permission(AnchorLayout):
    def addPermTime(self, time):
        if time == '':
            def callback(instance):
                if instance.text == 'OK':
                    pop.dismiss()
                    return 0
            closePopBtn = Button(text="OK", size_hint=(1, 0.25))
            closePopBtn.bind(on_release=callback)
            pop = Dialog.dialog("No TIME !!!", "Please Enter valid HOURS !!", closePopBtn)
            pop.open()
        global Date, id
        db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
        cur = db.cursor()
        cur.execute("INSERT INTO essl.%d (IO, MTIME, MDATE, DOOR) VALUES('P', '%s', '%s', 'PERMISSION')" %(int(id), time, Date))
        cur.close()
        db.close()

class Doors(BoxLayout):
    pass

def getTimings(artistID):
    print(artistID)

def formatDate(date):
    Dt = date.split(".")
    return str("-".join(list(reversed(Dt))))

class userSettingPop(Popup):
    def __init__(self, artistID, date):
        super().__init__()
        global Date, id
        self.date = formatDate(date)
        Date = formatDate(date)
        self.id = artistID.split(":")[0]
        id = artistID.split(":")[0]
        self.title = (artistID.split(":")[1] + " || " + date)
        self.font_name = 'fonts/moon-bold.otf'
