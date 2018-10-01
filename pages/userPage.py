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
from kivy.graphics import Color, Rectangle
from db import getInfo
from pages import Calendar, table

logoutButton = Button()
id = [0]*1
user = [None]*1
department = [None]*1

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

        userInfoLayout = BoxLayout(orientation='horizontal', size_hint=(1, 0.25), pos_hint={'left':1, 'top':1})
        calendarLayout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 0.55))
        #self.timingLayout = BoxLayout(orientation='horizontal', size_hint=(1, 0.35))
        userPageLayout.add_widget(userInfoLayout)
        userPageLayout.add_widget(calendarLayout)

        userInfoLabel = Label(text='%d : %s : %s' %(id[int(len(id)-1)], user[int(len(user)-1)], department[int(len(department)-1)]), size_hint=(0.5, 0.2))
        userInfoLayout.add_widget(userInfoLabel)

        calendarWidget = Calendar.CalendarWidget()
        calendarLayout.add_widget(calendarWidget)
