import pymysql
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.image import Image
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
""")


class Settings(Popup):
    def __init__(self, **args):
        super(Settings, self).__init__(**args)
        self.size_hint=(0.75, 0.75)
        self.UI()
        Popup.open(self)

    def UI(self):
        def callback(instance):
            if instance.text == 'CALENDAR DETAILS':
                calSettings.setup()

        #calDetBtn = Button(text='CALENDAR DETAILS', size_hint=(0.25, 0.25))
        calDetBtn = calButton()
        calDetBtn.bind(on_press=callback)
        self.add_widget(calDetBtn)

class calButton(Button):
    pass
