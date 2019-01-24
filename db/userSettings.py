import pymysql
from kivy.uix.popup import Popup
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

from pages import Dialog, infoPopup

Date = ""
id = ""

Builder.load_string("""
<userSettingPop>:
    size_hint: (0.75, 0.65)

    SettingsTabs:
        do_default_tab: False

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
    orientation: 'vertical'
    spacing: 5
    Label:
        id: curLvl
        text: 'CURRENT LEVEL : 0'
    BoxLayout:
        orientation: 'horizontal'
        Spinner:
            id: lvl
            text: 'LEVEL'
            values: ('1', '2', '3', '4', '5', '6', '7')
            font_name: 'fonts/moon-bold.otf'
            size_hint: (0.5, 0.25)
            pos_hint: {'center_x': .5, 'center_y': .5}
        Button:
            id: subLvl
            text: 'Assign Level'
            size_hint_x: 0.5
            on_release: root.submitLvl(lvl.text)
    BoxLayout:
        orientation: 'horizontal'
        Label:
            text: "User Status :"
        Switch:
            id: user_status
            active_norm_pos: 1
            on_touch_move: root.change_user_status()



<SettingsTabs>:
    TabbedPanelItem:
        text: 'LEVEL'
        font_name: 'fonts/moon-bold.otf'
        Level:
""")
def formatDate(date):
    Dt = date.split(".")
    return str("-".join(list(reversed(Dt))))

def getTimings():
    print(id)

class userSettingPop(Popup):
    def __init__(self, artistID, date):
        super(userSettingPop, self).__init__()
        global Date, id
        print('ok')
        self.date = formatDate(date)
        Date = formatDate(date)
        self.id = artistID.split(":")[0]
        id = artistID.split(":")[0]
        self.title = (artistID.split(":")[1] + " || " + date)
        self.font_name = 'fonts/moon-bold.otf'
        pass

class SettingsTabs(TabbedPanel):
    pass

class RemTime(FloatLayout):
    def __init__(self, ID, Date, IO, Time, Door, AccType):
        super(RemTime, self).__init__()
        self.id = str(ID)
        self.date = Date
        self.data = [IO, Time, Door, AccType]

    def remTime(self):
        try:
            db = pymysql.connect("10.10.5.60", "mcheck", "mcheck@123", "essl", autocommit=True)
        except:
            db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
        cur = db.cursor()
        def callback(instance):
            if instance.text == 'OK':
                pop.dismiss()
                return 0
        closePopBtn = Button(text="OK", size_hint=(1, 0.25))
        closePopBtn.bind(on_release=callback)
        try:
            cur.execute("DELETE FROM essl.%d WHERE IO = '%s' AND MTIME = '%s' AND MDATE = '%s' AND DOOR = '%s' AND AccType = '%s'"%(int(self.id), self.data[0], self.data[1], self.date, self.data[2], self.data[3]))
            pop = Dialog.dialog("Deleted", "Data Delete Successfull !! \n Details: TIME: {} | DATE: {} | DOOR:{}".format(self.data[1], self.date, self.data[2]), closePopBtn)
            pop.open()
        except Exception as e:
            print(e)
            pop = Dialog.dialog("Error !!!", "Some Error Occured Please restart and try again !!", closePopBtn)
            pop.open()
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
        try:
            db = pymysql.connect("10.10.5.60", "mcheck", "mcheck@123", "essl", autocommit=True)
        except:
            db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
        cur = db.cursor()
        def callback(instance):
            if instance.text == 'OK':
                pop.dismiss()
                return 0
        closePopBtn = Button(text="OK", size_hint=(1, 0.25))
        closePopBtn.bind(on_release=callback)
        try:
            cur.execute("INSERT INTO essl.%d (IO, MTIME, MDATE, DOOR, AccType) VALUES('%s', '%s', '%s', '%s', 'REGULARIZATION')" %(int(self.id), self.io, time, self.date, self.door))
            pop = Dialog.dialog("Success", "Data added successfully !!", closePopBtn)
            #infoPopup.refreshTable()
            pop.open()
        except Exception as e:
            print(e)
            pop = Dialog.dialog("Error !!!", "Please Provide valid information !!", closePopBtn)
            pop.open()
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
        def callback(instance):
            if instance.text == 'OK':
                pop.dismiss()
                return 0
        closePopBtn = Button(text="OK", size_hint=(1, 0.25))
        closePopBtn.bind(on_release=callback)
        if time == '':
            pop = Dialog.dialog("No TIME !!!", "Please Enter valid HOURS !!", closePopBtn)
            pop.open()
        else:
            try:
                db = pymysql.connect("10.10.5.60", "mcheck", "mcheck@123", "essl", autocommit=True)
            except:
                db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
            cur = db.cursor()
            cur.execute("INSERT INTO essl.`leave_details` (ID, from_date, to_date, Reason, Status, app_date) VALUES('%d', '%s', '%s', '%s', 'PE', '%s')" %(int(self.data[0]), self.data[1], self.data[1], time, self.data[1]))
            cur.close()
            db.close()
            pop = Dialog.dialog("SUCCESS", "Success", closePopBtn)
            pop.open()

    def checkText(self, text):
        time = re.compile(r'[0-2][0-9]:[0-6][0-9]:[0-6][0-9]')
        if time.match(text):
            self.ids.hours.background_color = (0, 1, 0, 1)
        elif text != '':
            self.ids.hours.background_color = (1, 0, 0, 1)
        elif text == '':
            self.ids.hours.background_color = (1, 1, 1, 1)

class Level(BoxLayout):
    def submitLvl(self, lvl):
        global id
        try:
            db = pymysql.connect("10.10.5.60", "mcheck", "mcheck@123", "essl", autocommit=True)
        except:
            db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
        cur = db.cursor()
        cur.execute("UPDATE essl.user_master SET Level = '%d' WHERE ID = '%d'"%(int(lvl), int(id)))
        cur.close()
        db.close()

    def change_user_status(self):
        global id
        print(id)
        try:
            db = pymysql.connect("10.10.5.60", "mcheck", "mcheck@123", "essl", autocommit=True)
        except:
            db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
        cur = db.cursor()
        cur.execute("UPDATE essl.user_master SET Status = 'CLOSED' WHERE ID = '%d'"%(int(id)))
        cur.close()
        db.close()
