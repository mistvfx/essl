from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
#from KivyCalendar import CalendarWidget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.graphics import *
from kivy.lang import Builder

from db import getInfo
from pages import Calendar, table

logoutButton = Button()
id = [0]*1
user = [None]*1
department = [None]*1

Builder.load_string("""
<UserPage>:
    canvas.before:
        Color:
            hsv: 0, 0, 0.80
        Rectangle:
            pos: self.pos
            size: self.size

<userLabel>:
    size_hint_y: 0.10
    pos_hint: {'top':1}
    bold: True
    color: (0, 0, 0, 1)
    font_name: 'fonts/moon-bold.otf'
    font_size: 25
""")

class userLabel(Label):
    pass

class UserPage(Screen):
    def __init__(self, **args):
        super(UserPage, self).__init__(**args)
        self.user()

    def user(self):
        global id, user, department

        #userPageLayout = BoxLayout(orientation='vertical')
        userPageLayout = FloatLayout(size=(Window.width, Window.height))
        self.add_widget(userPageLayout)

        global logoutBtn
        try:
            userPageLayout.add_widget(logoutButton)
        except:
            pass

        userInfoLabel = userLabel(text='%d | %s | %s' %(id[int(len(id)-1)], user[int(len(user)-1)], department[int(len(department)-1)]))
        userPageLayout.add_widget(userInfoLabel)

        calendarWidget = Calendar.CalendarWidget()
        calendarWidget.size_hint=(0.75, 0.75); calendarWidget.pos_hint={'center_y':0.5, 'center_x':0.5}
        userPageLayout.add_widget(calendarWidget)

        otherInfoLayout = BoxLayout(orientation='horizontal', size_hint=(0.1, 0.1), pos_hint={'center_y':0.1, 'center_x':0.5})
        userPageLayout.add_widget(otherInfoLayout)

        info1 = Label(text= 'LEAVES :', color=(0, 0, 0, 1))
        otherInfoLayout.add_widget(info1)
