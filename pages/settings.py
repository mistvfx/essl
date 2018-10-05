import pymysql
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from db import calSettings

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

        calDetBtn = Button(text='CALENDAR DETAILS', size_hint=(0.25, 0.25))
        calDetBtn.bind(on_press=callback)
        self.add_widget(calDetBtn)
