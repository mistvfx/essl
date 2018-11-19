import pymysql
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from KivyCalendar import DatePicker
from kivy.lang import Builder
import re

from pages import Dialog

Builder.load_string("""
<AddPermission>:
    Spinner:
        text: 'DEPARTMENT'
        font_name: 'fonts/moon-bold.otf'
        values: ('ALL', 'IT', 'MM', 'PAINT', 'ROTO', 'HR', 'PROD')
        size_hint: (0.55, 0.25)
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_text: root.Dept(self.text)

    TextInput:
        id: hours
        hint_text: 'HOURS (HH:MM:SS)'
        font_name: 'fonts/moon-bold.otf'
        font_size: 30
        size_hint: (0.55, 0.20)
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_text: root.checkText(hours.text)

    Button:
        text: 'ADD PERMISSION TIME'
        size_hint: (0.55, 0.25)
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: root.addPermTimeBulk(hours.text)

<BEtabs>:
    do_default_tab: False
    
    TabbedPanelItem:
        text: 'PERMISSION'
        font_name: 'fonts/moon-bold.otf'
        AddPermission:
""")

def formatDate(date):
    Dt = date.split(".")
    return str("-".join(list(reversed(Dt))))

class BEtabs(TabbedPanel):
    pass

class AddPermission(BoxLayout):
    def __init__(self, **args):
        super(AddPermission, self).__init__(**args)
        self.orientation = "vertical"
        self.spacing = 5
        self.department = ''

        self.date = DatePicker(size_hint=(0.55, 0.20), pHint=(0.35, 0.35), pos_hint={'center_x': .5, 'center_y': .5}, font_size=30)
        self.add_widget(self.date)

    def Dept(self, dept):
        self.department = dept

    def addPermTimeBulk(self, hours):
        def callback(instance):
            if instance.text == 'OK':
                pop.dismiss()
                return 0
        closePopBtn = Button(text="OK", size_hint=(1, 0.25))
        closePopBtn.bind(on_release=callback)
        if hours == '' or self.department == 'DEPARTMENT' or self.department == '':
            pop = Dialog.dialog("No TIME !!!", "Please Enter valid DATA !!", closePopBtn)
            pop.open()
        elif self.department == 'ALL':
            db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
            cur = db.cursor()
            cur1 = db.cursor()
            cur.execute("SELECT ID FROM essl.user_master WHERE Status = 'OPEN'")
            for id in cur.fetchall():
                if id[0] == 1000:
                    continue
                cur1.execute("INSERT INTO essl.%d (IO, MTIME, MDATE, DOOR) VALUES('P', '%s', '%s', 'PERMISSION')" %(int(id[0]), hours, formatDate(self.date.text)))
            cur.close()
            cur1.close()
            db.close()
            pop = Dialog.dialog("SUCCESS", "Successfully added the permission time", closePopBtn)
            pop.open()
        else:
            db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
            cur = db.cursor()
            cur1 = db.cursor()
            cur.execute("SELECT ID FROM essl.user_master WHERE Status = 'OPEN' AND Department = '%s'"%(self.department))
            for id in cur.fetchall():
                if id[0] == 1000:
                    continue
                cur1.execute("INSERT INTO essl.%d (IO, MTIME, MDATE, DOOR) VALUES('P', '%s', '%s', 'PERMISSION')" %(int(id[0]), hours, formatDate(self.date.text)))
            cur.close()
            cur1.close()
            db.close()
            pop = Dialog.dialog("SUCCESS", "Successfully added the permission time", closePopBtn)
            pop.open()

    def checkText(self, text):
        time = re.compile(r'[0-2][0-9]:[0-6][0-9]:[0-6][0-9]')
        if time.match(text):
            self.ids.hours.background_color = (0, 1, 0, 1)
        elif text != '':
            self.ids.hours.background_color = (1, 0, 0, 1)
        elif text == '':
            self.ids.hours.background_color = (1, 1, 1, 1)

def setup():
    popup = Popup(title='Bulk Edits', content=BEtabs(), size_hint=(0.75, 0.75))
    popup.open()
