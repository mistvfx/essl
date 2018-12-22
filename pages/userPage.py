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

<InfoLabel>:
    color: (0, 0, 0, 1)
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size

<OtherButton>:
    text: 'Extras'
    size_hint: (0.1, 0.1)
""")

class userLabel(Label):
    pass

class OtherLayout(BoxLayout):
    pass

class InfoLabel(Label):
    pass

class OtherButton(Button):
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

        def callback(instance):
            from pages import leaveReq
            leaveReq.Data.append([user[len(user)-1], id[len(id)-1], department[len(department)-1]])
            pop = Popup(title= 'Leave Reuqest Form', content= leaveReq.LeaveLayout(), size_hint=(0.5, 0.5))
            pop.open()

        others = OtherButton(pos_hint= {'right':1})
        others.bind(on_release=callback)
        userPageLayout.add_widget(others)

        userInfoLabel = userLabel(text='%d | %s | %s' %(id[int(len(id)-1)], user[int(len(user)-1)], department[int(len(department)-1)]))
        userPageLayout.add_widget(userInfoLabel)

        calendarWidget = Calendar.CalendarWidgetM()
        calendarWidget.size_hint=(0.75, 0.75); calendarWidget.pos_hint={'center_y':0.5, 'center_x':0.5}
        userPageLayout.add_widget(calendarWidget)

        otherInfoLayout = OtherLayout(orientation='horizontal', size_hint=(0.75, 0.05), pos_hint={'center_y':0.08, 'center_x':0.5}, spacing=10, padding=(10, 0, 0, 10))
        userPageLayout.add_widget(otherInfoLayout)

        redLayout = BoxLayout(orientation = 'horizontal', size_hint_x=0.15)
        red = Button(text="", background_color=(255, 0, 0, 0.7), size_hint_x=0.2)
        redInfo = InfoLabel(text="Non Completed")
        redLayout.add_widget(red)
        redLayout.add_widget(redInfo)

        greenLayout = BoxLayout(orientation = 'horizontal', size_hint_x=0.15)
        green = Button(text="", background_color=(0, 255, 0, 0.7), size_hint_x=0.2)
        greenInfo = InfoLabel(text="Completed")
        greenLayout.add_widget(green)
        greenLayout.add_widget(greenInfo)

        yellowLayout = BoxLayout(orientation = 'horizontal', size_hint_x=0.15)
        yellow = Button(text="", background_color=(255, 255, 0, 0.7), size_hint_x=0.2)
        yellowInfo = InfoLabel(text="Absent")
        yellowLayout.add_widget(yellow)
        yellowLayout.add_widget(yellowInfo)

        blueLayout = BoxLayout(orientation = 'horizontal', size_hint_x=0.15)
        blue = Button(text="", background_color=(0, 0, 255, 0.7), size_hint_x=0.2)
        blueInfo = InfoLabel(text="Holiday")
        blueLayout.add_widget(blue)
        blueLayout.add_widget(blueInfo)

        greyLayout = BoxLayout(orientation = 'horizontal', size_hint_x=0.15)
        grey = Button(text="", background_color=(0.5, 0.5, 0.5, 1), size_hint_x=0.2)
        greyInfo = InfoLabel(text="Sat/Sun")
        greyLayout.add_widget(grey)
        greyLayout.add_widget(greyInfo)

        otherInfoLayout.add_widget(redLayout)
        otherInfoLayout.add_widget(greenLayout)
        otherInfoLayout.add_widget(yellowLayout)
        otherInfoLayout.add_widget(blueLayout)
        otherInfoLayout.add_widget(greyLayout)
