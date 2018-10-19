import pymysql
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from db import calSettings

Builder.load_string("""
<calButton@Button>:
    text: 'CALENDAR DETAILS'
    size_hint: 1, 0.25
    background_color: (255, 255, 255, 1)
    Image:
        source: 'icons/cal.png'
        y: self.parent.y
        x: self.parent.x

<deleteAllDBBtn>:
    TextInput:
        text_hint: 'PASSWORD'

""")

class deleteAllDBBtn(DropDown):
    pass

class Settings(Popup):
    def __init__(self, **args):
        super(Settings, self).__init__(**args)
        self.size_hint=(0.75, 0.75)
        self.UI()
        Popup.open(self)

    def UI(self):
        popLayout = BoxLayout(orientation='horizontal')
        self.add_widget(popLayout)

        def callback(instance):
            if instance.text == 'CALENDAR DETAILS':
                calSettings.setup()

        #calDetBtn = Button(text='CALENDAR DETAILS', size_hint=(0.25, 0.25))
        calDetBtn = calButton()
        calDetBtn.bind(on_press=callback)
        popLayout.add_widget(calDetBtn)

        """db management"""

        delAllBtn = deleteAllDBBtn()
        popLayout.add_widget(delAllBtn)

class calButton(Button):
    pass
