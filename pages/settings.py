import pymysql
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from db import calSettings, databaseEdit, bulkedits

Builder.load_string("""
<calButton@Button>:
    text: 'CALENDAR DETAILS'
    size_hint_y: 0.25
    font_name: 'fonts/moon-bold.otf'
    background_color: (0, 0, 0, 1)
    Image:
        source: 'icons/cal.png'
        y: self.parent.y
        x: self.parent.x

<DBBtn>:
    text: 'Database Editing'
    size_hint_y: 0.25
    font_name: 'fonts/moon-bold.otf'
    background_color: (0, 0, 0, 1)

<BulkEdits>:
    text: 'BULK EDITS'
    size_hint_y: 0.25
    font_name: 'fonts/moon-bold.otf'
    background_color: (0, 0, 0, 1)

""")

class DBBtn(Button):
    pass

class BulkEdits(Button):
    pass

class Settings(Popup):
    def __init__(self, **args):
        super(Settings, self).__init__(**args)
        self.size_hint=(0.75, 0.75)
        self.UI()
        Popup.open(self)

    def UI(self):
        popLayout = BoxLayout(orientation='vertical', spacing = 10)
        self.add_widget(popLayout)

        def callback(instance):
            if instance.text == 'CALENDAR DETAILS':
                calSettings.setup()
            elif instance.text == 'Database Editing':
                databaseEdit.setup()
            elif instance.text == 'BULK EDITS':
                bulkedits.setup()

        #calDetBtn = Button(text='CALENDAR DETAILS', size_hint=(0.25, 0.25))
        calDetBtn = calButton()
        calDetBtn.bind(on_release=callback)
        popLayout.add_widget(calDetBtn)

        """db management"""

        dbBtn = DBBtn()
        dbBtn.bind(on_release=callback)
        popLayout.add_widget(dbBtn)

        blkEdit = BulkEdits()
        blkEdit.bind(on_release=callback)
        popLayout.add_widget(blkEdit)

class calButton(Button):
    pass
