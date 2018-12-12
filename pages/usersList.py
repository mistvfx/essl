from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.behaviors import *
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.treeview import *
from kivy.properties import *
from kivy.graphics import *
from kivy.lang import Builder

from pages import table, monthlyPopup, Dialog
from pages.specialFeatures import *
from db import getInfo, monthlyWrkHours, userSettings
import datetime

id = []
names = []
date = []
months = ['January ', 'Feburary ', 'March ', 'April ', 'May ', 'June ', 'July ', 'August ', 'September ', 'October ', 'November ', 'December ']

Builder.load_string("""
<dayBtn>:
    text: 'Day'
    font_name: 'fonts/moon-bold.otf'
    size_hint_x: 0.1
    size_hint_y: 1
    color: (1, 1, 1, 0)
    background_color: (0, 0, 0, 0)
    Image:
        source: 'icons/day.png'
        size: self.parent.size
        y: self.parent.y
        x: self.parent.x

<monthInfoBtn>:
    text: 'Month'
    font_name: 'fonts/moon-bold.otf'
    size_hint_x: 0.1
    color: (1, 1, 1, 0)
    background_color: (0, 0, 0, 0)
    canvas.before:
        Color:
            rgba: (0, 0, 0, 1)
    Image:
        source: 'icons/month.png'
        size: self.parent.size
        y: self.parent.y
        x: self.parent.x

<settingsBtn>:
    text: 'Settings'
    font_name: 'fonts/moon-bold.otf'
    size_hint_x: 0.1
    color: (1, 1, 1, 0)
    background_color: (0, 0, 0, 0)
    Image:
        source: 'icons/userSettings.png'
        size: self.parent.size
        y: self.parent.y
        x: self.parent.x

<user>:
    size_hint_y: None
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 1
        pos: root.pos
        size: root.size

        canvas.before:
            Color:
                rgba: (0, 0, 0, 0.1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [25, 25, 25, 25]

        Image:
            source: 'icons/user.png'
            size_hint_x: 0.25
        UserInfo:
            id: artistLabel
            text: root.Artist
            font_name: 'fonts/moon-bold.otf'
            color: (0, 0, 0, 1)
            size_hint_x: 0.7
        dayBtn:
            on_release: self.getDayInfo(artistLabel.text)
        monthInfoBtn:
            on_release: self.getMonthInfo(artistLabel.text)
        settingsBtn:
            on_release: self.settingsPop(artistLabel.text)
""")

def formatDate(date):
    #datetime.datetime.strptime(date[len(date)-1], '%d.%m.%Y').date()
    dt = date.split(".")
    return [dt[0], dt[1], dt[2]]

def formatDateTitle(date):
    global months
    dt = date.split(".")
    yr = months[int(dt[1])-1] + "-" + str(dt[2])
    return yr

class user(Widget):
    Artist = StringProperty("")
    def __init__(self, ArtistId, ArtistName):
        super(user, self).__init__()
        self.ArtistId = ArtistId
        self.ArtistName = ArtistName
        texts = (str(ArtistId) + ":" + ArtistName)
        self.Artist = texts

class UserInfo(TouchRippleBehavior, Label):
    def __init__(self, **kwargs):
        super(UserInfo, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        collide_point = self.collide_point(touch.x, touch.y)
        if collide_point:
            touch.grab(self)
            self.ripple_show(touch)
            return True
        return False

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.ripple_fade()
            return True
        return False

class dayBtn(Button, MouseOver):
    def __init__(self, **args):
        super(dayBtn, self).__init__(**args)

    def on_hover(self):
        self.background_color = (1, 0, 0, 0.5)

    def on_exit(self):
        self.background_color = (0, 0, 0, 0)

    def getDayInfo(self, artistID):
        global date

        getInfo.id.append(int(artistID.split(":")[0]))
        getInfo.date.append(formatDate(date[len(date)-1]))

        try:
            getInfo.openPopup('admin')
        except Exception as e:
            print(e)
            def callback(instance):
                if instance.text == 'OK':
                    pop.dismiss()
            closePopBtn = Button(text="OK", size_hint=(1, 0.25))
            closePopBtn.bind(on_release=callback)
            pop = Dialog.dialog("No Data !!!", "No data Available for the selected date !!", closePopBtn)
            pop.open()

class settingsBtn(Button, MouseOver):
    def __init__(self, **args):
        super(settingsBtn, self).__init__(**args)

    def on_hover(self):
        self.background_color = (0, 1, 0, 0.5)

    def on_exit(self):
        self.background_color = (0, 0, 0, 0)

    def settingsPop(self, artistID):
        global date
        userSettings.userSettingPop(artistID, date[len(date)-1]).open()

class monthInfoBtn(Button, MouseOver):
    def __init__(self, **args):
        super(monthInfoBtn, self).__init__(**args)

    def on_hover(self):
        self.background_color = (0, 0, 1, 0.5)

    def on_exit(self):
        self.background_color = (0, 0, 0, 0)

    def getMonthInfo(self, artistID):
        global date

        monthlyWrkHours.id.append(int(artistID.split(":")[0]))
        monthlyPopup.month.append(formatDateTitle(date[len(date)-1]))

        monthlyPopup.workTime()
        monthlyPopup.pop()

class userList(ScrollView):
    def __init__(self):
        super(userList, self).__init__()
        self.listUI()

    def listUI(self):
        global id, names

        layout = GridLayout(cols=1, spacing=1, padding=(20, 0, 0, 0), size_hint=(1, None))
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(len(id)):
            lbl = user(id[i], names[i])
            layout.add_widget(lbl)

        self.add_widget(layout)
