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
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from pages import table, monthlyPopup
from db import getInfo, monthlyWrkHours
import datetime

id = []
names = []
date = []
months = ['January ', 'Feburary ', 'March ', 'April ', 'May ', 'June ', 'July ', 'August ', 'September ', 'October ', 'November ', 'December ']

def formatDate(date):
    #datetime.datetime.strptime(date[len(date)-1], '%d.%m.%Y').date()
    dt = date.split(".")
    return [dt[0], dt[1], dt[2]]

def formatDateTitle(date):
    global months
    dt = date.split(".")
    yr = months[int(dt[1])-1] + "-" + str(dt[2])
    #return (months[dt[1]] + "-" + str(dt[2]))
    return yr

class userInformation(TabbedPanel):
    def __init__(self):
        super(userInformation, self).__init__()
        self.tabsUI()

    def tabsUI(self):
        atdTab = TabbedPanelHeader(text='ATTENDANCE')
        self.add_widget(atdTab)

        def callback(instance):
            if instance.text == 'DAY':
                getInfo.openPopup()
            elif instance.text == 'MONTH':
                monthlyPopup.workTime()
                monthlyPopup.pop()

        btnsLayout = BoxLayout(orientation='vertical', size_hint=(1, 1))

        dayBtn = Button(text='DAY')
        dayBtn.bind(on_press=callback)
        btnsLayout.add_widget(dayBtn)

        weekBtn = Button(text='WEEK')
        weekBtn.bind(on_press=callback)
        btnsLayout.add_widget(weekBtn)

        monthBtn = Button(text='MONTH')
        monthBtn.bind(on_press=callback)
        btnsLayout.add_widget(monthBtn)
        atdTab.content = btnsLayout

class userInfoPopup(BoxLayout):
    pass

class User(ButtonBehavior, Label):
    def __init__(self, ArtistId, ArtistName):
        super(User, self).__init__()
        self.ArtistId = ArtistId
        self.ArtistName = ArtistName
        texts = (str(ArtistId) + " : " + ArtistName)
        self.text = texts

    def on_press(self):
        global date

        getInfo.id.append(int(self.ArtistId))
        getInfo.date.append(formatDate(date[len(date)-1]))

        monthlyWrkHours.id.append(int(self.ArtistId))
        monthlyPopup.month.append(formatDateTitle(date[len(date)-1]))

        popup = Popup(title=self.ArtistName, content=userInformation(), size_hint=(0.75, 0.75))
        popup.open()

    def on_release(self):
        pass

class userList(ScrollView):
    def __init__(self):
        super(userList, self).__init__()
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
