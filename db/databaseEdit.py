import pymysql
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from KivyCalendar import DatePicker
from kivy.lang import Builder

from pages import Dialog

Builder.load_string("""
<DBtabs>:
    do_default_tab: False
    
    TabbedPanelItem:
        text: 'DELETE'
        font_name: 'fonts/moon-bold.otf'
        DeleteData:
""")

def formatDate(date):
    Dt = date.split(".")
    return str("-".join(list(reversed(Dt))))

class DBtabs(TabbedPanel):
    pass

class DeleteData(BoxLayout):
    def __init__(self, **args):
        super(DeleteData, self).__init__(**args)
        self.orientation = "vertical"

        def callback(instance):
            if instance.text == 'DELETE ALL DATA':
                self.deleteAllData(formatDate(date.text))

        date = DatePicker(size_hint_y=0.20, pHint=(0.35, 0.35))
        self.add_widget(date)

        delBtn = Button(text='DELETE ALL DATA', size_hint_y=0.20)
        delBtn.bind(on_release = callback)
        self.add_widget(delBtn)

    def deleteAllData(self, delDate):
        db = pymysql.connect("127.0.0.1", "mcheck", "py@123", "essl", autocommit=True)
        cur = db.cursor()
        cur1 = db.cursor()

        cur.execute("SELECT ID FROM essl.user_master WHERE Status = 'OPEN'")
        for id in cur.fetchall():
            if id[0] == 1000:
                continue
            cur1.execute("DELETE FROM essl.%d WHERE MDATE = '%s'"%(id[0], delDate))

        def callback(instance):
            if instance.text == 'OK':
                pop.dismiss()
                return 0
        closePopBtn = Button(text="OK", size_hint=(1, 0.25))
        closePopBtn.bind(on_release=callback)
        pop = Dialog.dialog("DELETED SUCCESSFULLY!!!", "All data for the selected date has been deleted successfully !!", closePopBtn)
        pop.open()

def setup():
    popup = Popup(title='Database Edits', content=DBtabs(), size_hint=(0.75, 0.75))
    popup.open()
