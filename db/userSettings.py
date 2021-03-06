import pymysql
from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.properties import *
import re
from db.essl_credentials import credentials

from pages import Dialog, infoPopup, kivytoast

Date = ""
id = ""

Builder.load_string("""
<TimingFix>:
    orientation: 'vertical'
    spacing: 5

    Spinner:
        text: 'DOOR'
        font_name: 'fonts/moon-bold.otf'
        values: ('IT', 'MM', 'PAINT', 'ROTO', 'HR', 'CONFERENCEROOM', 'TRAINING', 'SERVER', 'ASLAM SIR', 'BACKDOOR')
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
        background_color: (1, 1, 1, 1)
        font_size: self.size[1]/2.5
        padding: [self.size[1], self.size[1]/5.0, 0, 0]
        font_name: 'fonts/moon-bold.otf'
        multiline: False
        size_hint: (0.65, 0.25)
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_text: root.checkText(time.text)

    Button:
        text: 'ADD TIME'
        font_name: 'fonts/moon-bold.otf'
        size_hint: (0.65, 0.25)
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: root.Time(time.text)

<RemTime>:
    pos: self.pos
    size: self.size
    Button:
        text: 'Remove Time'
        size_hint: (0.75, 0.25)
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        on_press: root.remTime()

<Permission>:
    size_hint: (0.5, 0.10)
    anchor_x: 'center'
    anchor_y: 'center'
    BoxLayout:
        orientation: 'vertical'
        TextInput:
            id: hours
            hint_text: 'HOURS (HH:MM:SS)'
            multiline: False
            on_text: root.checkText(hours.text)
        Button:
            text: 'Submit'
            on_release: root.addPermTime(hours.text)

<Level>:
    BoxLayout:
        orientation: 'horizontal'
        GridLayout:
            rows: 8
            Label:
                text: 'Level Information'
            Label:
                text: '1: [MM, ROTO, PAINT, CONFERENCEROOM, TRAINING, IT, HR, SERVER, STORE]'
                halign: 'left'
                text_size: self.width, self.height
            Label:
                text: '2: [MM, ROTO, PAINT, CONFERENCEROOM, TRAINING, HR]'
                halign: 'left'
                text_size: self.width, self.height
            Label:
                text: '3: [MM, ROTO, PAINT, CONFERENCEROOM, TRAINING]'
                halign: 'left'
                text_size: self.width, self.height
            Label:
                text: '4: [MM, ROTO, CONFERENCEROOM]'
                halign: 'left'
                text_size: self.width, self.height
            Label:
                text: '5: [ROTO, CONFERENCEROOM]'
                halign: 'left'
                text_size: self.width, self.height
            Label:
                text: '6: [MM, CONFERENCEROOM, TRAINING]'
                halign: 'left'
                text_size: self.width, self.height
            Label:
                text: '7: [ROTO, CONFERENCEROOM, TRAINING]'
                halign: 'left'
                text_size: self.width, self.height
        BoxLayout:
            orientation: 'vertical'
            spacing: 5
            canvas.before:
                Color:
                    rgba: (0, 0, 0, 1)
                Rectangle:
                    size: self.size
                    pos: self.pos
            BoxLayout:
                orientation: 'horizontal'
                spacing: 5
                canvas.before:
                    Color:
                        rgba: (1, 1, 1, 1)
                    Rectangle:
                        size: self.size
                        pos: self.pos
                Label:
                    id: curLvl
                    text: root.user_level
                    color: (0, 0, 0, 1)
                BoxLayout:
                    orientation: 'vertical'
                    Spinner:
                        id: lvl
                        text: 'LEVEL'
                        values: ('1', '2', '3', '4', '5', '6', '7')
                        font_name: 'fonts/moon-bold.otf'
                        size_hint: (0.75, 0.5)
                        pos_hint: {'center_x': .5, 'center_y': .5}
                    Button:
                        id: subLvl
                        text: 'Assign Level'
                        size_hint: (1, 0.5)
                        on_release: root.submitLvl(lvl.text)
            BoxLayout:
                orientation: 'horizontal'
                canvas.before:
                    Color:
                        rgba: (1, 1, 1, 1)
                    Rectangle:
                        size: self.size
                        pos: self.pos
                Label:
                    text: "User Status :"
                    color: (0, 0, 0, 1)
                Switch:
                    id: user_status
                    active_norm_pos: 1
                    on_touch_move: root.change_user_status()
""")
def formatDate(date):
    Dt = date.split(".")
    return str("-".join(list(reversed(Dt))))

class SettingsTabs(TabbedPanel):
    pass

class Level(ModalView):
    user_level = StringProperty('')

    def __init__(self, artist_id, date):
        super(Level, self).__init__()
        self.size_hint = (0.75, 0.35)
        global id
        id = artist_id.split(":")[0]
        self.get_level(artist_id.split(":")[0])

    def get_level(self, id):
        db = pymysql.connect(credentials['address'], credentials['username'], credentials['password'], credentials['db'], autocommit=True, connect_timeout=1)
        cur = db.cursor()
        cur.execute("SELECT Level FROM essl.user_master WHERE ID = '%d'"%(int(id)))
        self.user_level = 'Current Level : {}'.format(cur.fetchone()[0])
        cur.close()
        db.close()

    def submitLvl(self, lvl):
        global id
        db = pymysql.connect(credentials['address'], credentials['username'], credentials['password'], credentials['db'], autocommit=True, connect_timeout=1)
        cur = db.cursor()
        cur.execute("UPDATE essl.user_master SET Level = '%d' WHERE ID = '%d'"%(int(lvl), int(id)))
        cur.close()
        db.close()

    def change_user_status(self):
        global id
        db = pymysql.connect(credentials['address'], credentials['username'], credentials['password'], credentials['db'], autocommit=True, connect_timeout=1)
        cur = db.cursor()
        cur.execute("UPDATE essl.user_master SET Status = 'CLOSED' WHERE ID = '%d'"%(int(id)))
        cur.close()
        db.close()

class RemTime(FloatLayout):
    def __init__(self, ID, Date, IO, Time, Door, AccType):
        super(RemTime, self).__init__()
        self.id = str(ID)
        self.date = Date
        self.data = [IO, Time, Door, AccType]

    def remTime(self):
        db = pymysql.connect(credentials['address'], credentials['username'], credentials['password'], credentials['db'], autocommit=True, connect_timeout=1)
        cur = db.cursor()
        try:
            cur.execute("DELETE FROM essl.%d WHERE IO = '%s' AND MTIME = '%s' AND MDATE = '%s' AND DOOR = '%s' AND AccType = '%s'"%(int(self.id), self.data[0], self.data[1], self.date, self.data[2], self.data[3]))
            kivytoast.toast('Deleted Successfully !', (1, 0, 1, 0.5), length_long=True)
        except Exception as e:
            print(e)
            kivytoast.toast('Error, Please Restart', (1, 0, 0, 0.5), length_long=True)
        cur.close()
        db.close()

class TimingFix(BoxLayout):
    def __init__(self, ID, Date):
        super(TimingFix, self).__init__()
        self.id = str(ID)
        self.date = Date

    def Dept(self, dept):
        self.door = dept

    def IO(self, io):
        self.io = io

    def Time(self, time):
        db = pymysql.connect(credentials['address'], credentials['username'], credentials['password'], credentials['db'], autocommit=True, connect_timeout=1)
        cur = db.cursor()
        try:
            cur.execute("INSERT INTO essl.%d (IO, MTIME, MDATE, DOOR, AccType) VALUES('%s', '%s', '%s', '%s', 'REGULARIZATION')" %(int(self.id), self.io, time, self.date, self.door))
            kivytoast.toast('Data Added Successfully', (1, 0, 1, 0.5), length_long=True)
        except Exception as e:
            print(e)
            kivytoast.toast('Invalid Information !!', (1, 0, 0, 0.5), length_long=True)
        cur.close()
        db.close()

    def checkText(self, text):
        time = re.compile(r'[0-2][0-9]:[0-5][0-9]:[0-5][0-9]')
        if time.match(text):
            self.ids.time.background_color = (0, 1, 0, 1)
        elif text != '':
            self.ids.time.background_color = (1, 0, 0, 1)
        elif text == '':
            self.ids.time.background_color = (1, 1, 1, 1)

class Permission(AnchorLayout):
    def __init__(self, Data):
        super(Permission, self).__init__()
        self.data = Data

    def addPermTime(self, time):
        if time == '':
            kivytoast.toast('Invalid Hours !!', (1, 0, 0, 0.5), length_long=True)
        else:
            db = pymysql.connect(credentials['address'], credentials['username'], credentials['password'], credentials['db'], autocommit=True, connect_timeout=1)
            cur = db.cursor()
            cur.execute("INSERT INTO essl.`leave_details` (ID, from_date, to_date, Reason, Status, app_date) VALUES('%d', '%s', '%s', '%s', 'PE', '%s')" %(int(self.data[0]), self.data[1], self.data[1], time, self.data[1]))
            cur.close()
            db.close()
            kivytoast.toast('Success', (1, 0, 1, 0.5), length_long=True)

    def checkText(self, text):
        time = re.compile(r'[0-2][0-9]:[0-6][0-9]:[0-6][0-9]')
        if time.match(text):
            self.ids.hours.background_color = (0, 1, 0, 1)
        elif text != '':
            self.ids.hours.background_color = (1, 0, 0, 1)
        elif text == '':
            self.ids.hours.background_color = (1, 1, 1, 1)
