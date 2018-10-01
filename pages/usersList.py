from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup

id = []
names = []

class userInfoPopup(BoxLayout):
    

class User(ButtonBehavior, Label):
    def __init__(self, ArtistId, ArtistName):
        super(User, self).__init__()
        self.ArtistId = ArtistId
        self.ArtistName = ArtistName
        texts = (str(ArtistId) + " : " + ArtistName)
        self.text = texts

    def on_press(self):
        pass

    def on_release(self):
        pass

class userList(ScrollView):
    def __init__(self, **args):
        super(userList, self).__init__(**args)
        self.listUI()

    def listUI(self):
        global id, names

        layout = GridLayout(cols=1, spacing=5, size_hint=(1, None))
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(len(id)):
            #listLbl = (str(id[i]) + " : " + names[i])
            lbl = User(id[i], names[i])
            lbl.size_hint_y=None
            layout.add_widget(lbl)

        self.add_widget(layout)
