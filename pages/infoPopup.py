from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.properties import *
from kivy.lang import Builder
from kivy.clock import Clock
import datetime
import threading

from pages import table

closeBtn = Button()
TWH = 0
AWH = 0
NCH = 0
ACH = 0

id = ''
date = ''

Builder.load_string("""
#:import DataTable pages.table
<HdrLayout>:
    orientation: 'horizontal'
    size_hint: (1, 0.05)
    canvas.before:
        Color:
            rgba: (0, 0, 0, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<TblLayout>:
    orientation: 'horizontal'
    canvas.before:
        Color:
            rgba: (0, 0, 0, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<InfoLbl>:
    color: (1, 1, 1, 1)
    font_name: 'fonts/GoogleSans-Bold.ttf'
    #text_size: self.size
    markup: True
    canvas.before:
        Color:
            rgba: (124/255, 77/255, 255/255, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<InfoTabAdmin>:
    BoxLayout:
        id: overallLayout
        orientation: 'vertical'
        HdrLayout:
            id: header_layout_admin
            Label:
                text: 'Details'
                bold: True
            GridLayout:
                cols: 4
                size_hint: (0.55, 1)
                Label:
                    text: 'I/O'
                    bold: True
                Label:
                    text: 'TIME'
                    bold: True
                Label:
                    text: 'DOOR'
                    bold: True
                Label:
                    text: 'Access Type'
                    bold: True
        TblLayout:
            id: table_layout_admin
            GridLayout:
                id: info_admin
                cols: 2
                size_hint: (0.45, 1)

<InfoTab>:
    orientation: 'vertical'
    spacing: 5
    Label:
        text: root.date_text
        size_hint_y: 0.05
        color: (1, 1, 1, 1)
        font_name: 'fonts/GoogleSans-Bold.ttf'
        canvas.before:
            Color:
                rgba: (230/255, 81/255, 0/255, 1)
            Rectangle:
                size: self.size
                pos: self.pos
    StackLayout:
        pos: self.parent.pos
        size: self.parent.size
        size_hint_y: 0.25
        orientation: 'lr-tb'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_x: 0.25
            canvas.before:
                Color:
                    rgba: (98/255, 0/255, 234/255, 1)
                Rectangle:
                    size: self.size
                    pos: self.pos
            Image:
                source: 'icons/time.png'
        GridLayout:
            size_hint_x: 0.75
            spacing: 1
            cols: 2
            rows: 2
            canvas.before:
                Color:
                    rgba: (98/255, 0/255, 234/255, 1)
                Rectangle:
                    size: self.size
                    pos: self.pos
            InfoLbl:
                text: root.tw
            InfoLbl:
                text: root.aw
            InfoLbl:
                text: root.nc
            InfoLbl:
                text: root.ac

<UserTable>:
    orientation: 'vertical'
    HdrLayout:
        GridLayout:
            cols:4
            size_hint: (1, 1)
            spacing: 1
            Label:
                text: 'I/O'
                bold: True
                background_color: (1, 1, 1, 1)
                canvas.before:
                    Color:
                        rgba: (76/255, 175/255, 80/255, 1)
                    Rectangle:
                        size: self.size
                        pos: self.pos
            Label:
                text: 'TIME'
                bold: True
                background_color: (1, 1, 1, 1)
                canvas.before:
                    Color:
                        rgba: (76/255, 175/255, 80/255, 1)
                    Rectangle:
                        size: self.size
                        pos: self.pos
            Label:
                text: 'DOOR'
                bold: True
                background_color: (1, 1, 1, 1)
                canvas.before:
                    Color:
                        rgba: (76/255, 175/255, 80/255, 1)
                    Rectangle:
                        size: self.size
                        pos: self.pos
            Label:
                text: 'ACCESS TYPE'
                bold: True
                background_color: (1, 1, 1, 1)
                canvas.before:
                    Color:
                        rgba: (76/255, 175/255, 80/255, 1)
                    Rectangle:
                        size: self.size
                        pos: self.pos
    TblLayout:
        DataTable:
            size_hint: (0.65, 1)

""")

class HdrLayout(BoxLayout):
    pass

class TblLayout(BoxLayout):
    pass

class InfoLbl(Label):
    pass

def formatTime(time):
    try:
        seconds = time.total_seconds()
    except:
        seconds = 0
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)

    return ('{}:{}'.format(hours, minutes))

class UserTable(BoxLayout):
    def __init__(self, **kwargs):
        super(UserTable, self).__init__(**kwargs)
        view = ModalView(size_hint=(0.75, 0.75), background_color=(0, 0, 0, 0.6))
        view.add_widget(self)
        view.open()

class InfoTab(BoxLayout):
    tw = StringProperty('')
    aw = StringProperty('')
    nc = StringProperty('')
    ac = StringProperty('')

    date_text = StringProperty('')

    def __init__(self, **kwargs):
        super(InfoTab, self).__init__(**kwargs)
        self.t1 = threading.Thread(target=self.startClock())
        self.t1.start()
        #self.popInfo()

    def startClock(self):
        self.clock = Clock.schedule_interval(lambda dt: self.popInfo(), 0.5)

    def popInfo(self):
        #global TWH, AWH, NCH, ACH,
        global id, date
        from db import getInfo
        if date == '':
            return
        self.date_text = str(date)
        try:
            info = getInfo.getUserInfo(id, date)
        except Exception as e:
            return

        self.tw = "Total Hours \n\n \t    {}".format(formatTime(info['TWH']))
        self.aw = "Working Hours \n\n \t      {}".format(formatTime(info['AWH']))
        self.nc = "Non-Completed Actual Hours \n\n \t                     {}".format(formatTime(info['NCH']))
        self.ac = "Additional Hours \n\n \t         {}".format(formatTime(info['ACH']))

class InfoTabAdmin(BoxLayout):
    def __init__(self, id, date):
        super(InfoTabAdmin, self).__init__()
        self.popUI(id, date)
        self.openPopup()

    def openPopup(self):
        popup = ModalView(size_hint=(0.85, 0.85))
        popup.add_widget(self)
        #popup.bind(on_dismiss=self.stopClock)
        popup.open()

    def popUI(self, id, date):
        from db import getInfo
        getInfo.getUserInfo(id, date)

        tab = table.DataTableAdmin()
        tab.size_hint=(0.55, 1)
        self.ids.table_layout_admin.add_widget(tab)

        global TWH, AWH, NCH, ACH
        tw = formatTime(TWH)
        aw = formatTime(AWH)
        nc = formatTime(NCH)
        ac = formatTime(ACH)

        infoQ = ['Total Hours :', tw, 'Working Hours :', aw, 'Non-Completed Actual Hours:', nc, 'Additional Hours:', ac]

        for i in range(len(infoQ)):
            infoLabels = InfoLbl(text=infoQ[i])
            if i % 2 == 1:
                infoLabels.size_hint_x= 0.30
            self.ids.info_admin.add_widget(infoLabels)
