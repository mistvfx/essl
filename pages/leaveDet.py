from kivy.lang import Builder
from KivyCalendar import DatePicker
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from datetime import datetime
from calendar import monthrange
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import *
from kivy.properties import ObjectProperty
from kivy.uix.bubble import Bubble
from kivy.uix.modalview import ModalView
from kivy.vector import Vector

from db import usersListManip, leaveData, userSettings
from pages import calendar_data
from pages.specialFeatures import MouseOver

Builder.load_string("""
<LeaveDetLayout>:
    orientation: 'vertical'
    size_hint: (1, 1)
    BoxLayout:
        id: infoLayout
        orientation: 'horizontal'
        size_hint: (1, 0.05)
        spacing: 25
        padding: (4, 4, 4, 4)
        canvas.before:
            Color:
                rgba: (0.8, 0.8, 0.8, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            orientation: 'horizontal'
            canvas.before:
                Color:
                    rgba: (1, 1, 1, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: 'UP'
                font_name: 'fonts/GoogleSans-Bold.ttf'
                color: (1, 0, 0, 1)
                background_color: (1, 1, 1, 0)
                size_hint_x: 0.2
                canvas:
                    Color:
                        rgba: (1, 0, 0, 0.3)
                    Rectangle:
                        pos: self.pos
                        size: self.size
            Label:
                text: 'Unplanned'
                font_name: 'fonts/GoogleSans-Regular.ttf'
                color: (0, 0, 0, 1)
        BoxLayout:
            orientation: 'horizontal'
            canvas.before:
                Color:
                    rgba: (1, 1, 1, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: 'P'
                font_name: 'fonts/GoogleSans-Bold.ttf'
                color: (0, 1, 0, 1)
                background_color: (1, 1, 1, 0)
                size_hint_x: 0.2
                canvas:
                    Color:
                        rgba: (0, 1, 0, 0.3)
                    Rectangle:
                        pos: self.pos
                        size: self.size
            Label:
                text: 'Planned'
                font_name: 'fonts/GoogleSans-Regular.ttf'
                color: (0, 0, 0, 1)
        BoxLayout:
            orientation: 'horizontal'
            canvas.before:
                Color:
                    rgba: (1, 1, 1, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: 'S'
                font_name: 'fonts/GoogleSans-Bold.ttf'
                color: (0.5, 0.5, 0.5, 1)
                background_color: (1, 1, 1, 0)
                size_hint_x: 0.2
                canvas:
                    Color:
                        rgba: (0.5, 0.5, 0.5, 0.3)
                    Rectangle:
                        pos: self.pos
                        size: self.size
            Label:
                text: 'Sick'
                font_name: 'fonts/GoogleSans-Regular.ttf'
                color: (0, 0, 0, 1)
        BoxLayout:
            orientation: 'horizontal'
            canvas.before:
                Color:
                    rgba: (1, 1, 1, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: 'LR'
                font_name: 'fonts/GoogleSans-Bold.ttf'
                #color: (1, 1, 0, 1)
                color: (0, 0, 0, 1)
                background_color: (1, 1, 1, 0)
                size_hint_x: 0.2
                canvas:
                    Color:
                        rgba: (1, 1, 0, 0.3)
                    Rectangle:
                        pos: self.pos
                        size: self.size
            Label:
                text: 'Leave Requested'
                font_name: 'fonts/GoogleSans-Regular.ttf'
                color: (0, 0, 0, 1)
        BoxLayout:
            orientation: 'horizontal'
            canvas.before:
                Color:
                    rgba: (1, 1, 1, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: 'PE'
                font_name: 'fonts/GoogleSans-Bold.ttf'
                color: (0, 0, 1, 1)
                background_color: (1, 1, 1, 0)
                size_hint_x: 0.2
                canvas:
                    Color:
                        rgba: (0, 0, 1, 0.3)
                    Rectangle:
                        pos: self.pos
                        size: self.size
            Label:
                text: 'Permission'
                font_name: 'fonts/GoogleSans-Regular.ttf'
                color: (0, 0, 0, 1)

    BoxLayout:
        orientation: 'horizontal'
        BoxLayout:
            orientation: 'vertical'
            size_hint: (0.25, 1)
            BoxLayout:
                id: deptChooser
                size_hint: (1, 0.14)
                orientation: 'vertical'
                canvas.before:
                    Color:
                        rgba: (1, 1, 1, 1)
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Spinner:
                    text: 'DEPT'
                    values: ('MM', 'ROTO', 'PAINT', 'PROD', 'HR')
                    size_hint_y: 0.5
                    background_color: (1, 1, 1, 0)
                    font_name: 'fonts/GoogleSans-Medium.ttf'
                    canvas.before:
                        Color:
                            rgba: (0.5, 0.5, 0.5, 1)
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                Label:
                    text: 'ARTISTS'
                    color: (0, 0, 0, 1)
                    font_name: 'fonts/GoogleSans-Regular.ttf'

            NamesScroll:
                id: scroll_a
                size: self.size
                size_hint: (1, 0.7)
                do_scroll_y: False
                GridLayout:
                    id: artistlist
                    cols: 1
                    size_hint_y: None
                    padding: (1, 1, 1, 0)
                    spacing: 1
                    canvas.before:
                        Color:
                            rgba: (0, 0, 0, 1)
                        Rectangle:
                            pos: self.pos
                            size: self.size

        BoxLayout:
            orientation: 'vertical'
            size_hint: (0.75, 1)
            BoxLayout:
                id: dateInfo
                size_hint: (1, 0.2)
                orientation: 'vertical'
                FloatLayout:
                    id: monthInfo
                    pos: self.pos
                    size_hint_y: 0.5
                    size: self.size
                    canvas:
                        Color:
                            rgba: (1, 1, 1, 1)
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    CircularButton:
                        text: '<'
                        bold: True
                        pos_hint: {"center_y": 0.50, "center_x": 0.08}
                        on_release: root.go_prev()
                    Label:
                        id: monthName
                        color: (0.4, 0.4, 0.4, 1)
                        pos_hint: {"center_x":0.5, "center_y":0.5}
                        font_name: 'fonts/GoogleSans-Bold.ttf'
                    CircularButton:
                        text: '>'
                        bold: True
                        pos_hint: {"center_y": 0.50, "right": 0.92}
                        on_release: root.go_next()
                DaysScreen:
                    size_hint: (1, 0.01)

            ChartScreen:
                size_hint: (1, 1)
                pos: self.pos
                FloatLayout:
                    id: details
                    size: self.size
                    pos: self.pos


<DaysGrid>:
    spacing: 1
    canvas.before:
        Color:
            rgba: (0.5, 0.5, 0.5, 1)
        Rectangle:
            pos: self.pos
            size: self.size

<ChartGrid>:
    spacing: 1
    canvas.before:
        Color:
            rgba: (0.5, 0.5, 0.5, 0)
        Rectangle:
            pos: self.pos
            size: self.size

<DaysNumLabel>:
    font_name: 'fonts/GoogleSans-Medium.ttf'
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size

<DaysLabel>:
    font_name: 'fonts/GoogleSans-Regular.ttf'
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size

<ArtistLabel>:
    font_name: 'fonts/GoogleSans-MediumItalic.ttf'
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size

<LeaveButton>:
    font_name: 'fonts/GoogleSans-MediumItalic.ttf'
    background_color: (1, 1, 1, 0)
    color: (0, 0, 0, 0)
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size

<PopMenuPerm>:
    background_color: (1, 1, 1, 0)
    BoxLayout:
        id: layout
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: (1, 1, 1, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        Button:
            text: 'A'
            size_hint: (1, 0.5)
            color: (0, 1, 0, 1)
            background_color: (1, 1, 1, 0)
            on_release: root.acceptLeave()
            canvas.before:
                Color:
                    rgba: (0, 1, 0, 0.3)
                Rectangle:
                    pos: self.pos
                    size: self.size
        Button:
            text: 'D'
            size_hint: (1, 0.5)
            color: (1, 0, 0, 1)
            background_color: (1, 1, 1, 0)
            on_release: root.declineLeave()
            canvas.before:
                Color:
                    rgba: (1, 0, 0, 0.3)
                Rectangle:
                    pos: self.pos
                    size: self.size

<PopMenuLeave>:
    background_color: (1, 1, 1, 0)
    BoxLayout:
        id: layout
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: (1, 1, 1, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        Button:
            text: 'P'
            size_hint: (1, 0.5)
            color: (0, 1, 0, 1)
            background_color: (1, 1, 1, 0)
            on_release: root.permTime()
            canvas.before:
                Color:
                    rgba: (0, 1, 0, 0.3)
                Rectangle:
                    pos: self.pos
                    size: self.size

<CircularButton>:
    size: (min(self.width,self.height),min(self.width,self.height))
    background_color: (1, 0.64, 0, 0)
    font_size: 25
    canvas.before:
        Color:
            rgba: ((1,0.64,0,1) if self.state == "normal" else (1,0.32,0,1))
        Ellipse:
            pos: self.pos
            size: self.size
""")
class CircularButton(Button):
    def collide_point(self, x, y):
          return Vector(x, y).distance(self.center) <= self.width / 2

class NamesScroll(ScrollView):
    pass

class ChartScroll(ScrollView):
    pass

class DaysScreen(Screen):
    pass

class DaysGrid(GridLayout):
    pass

class ChartScreen(Screen):
    pass

class ChartGrid(GridLayout):
    pass

class DaysNumLabel(Label):
    pass

class ArtistLabel(Label):
    pass

class DaysLabel(Label):
    def set_bgGray(self):
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 0.50)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

opDetail = 0

class PopMenuLeave(ModalView):
    def __init__(self, **args):
        super(PopMenuLeave, self).__init__(**args)
        self.size_hint = (None, None)
        self.height = 50
        self.width = 50

    def open_pop(self, touch):
        self.pos_hint={'x' : touch.spos[0], 'top' : touch.spos[1]}
        self.open()

    def permTime(self):
        global opDetail
        #p = leaveData.grant_perm(detail)
        view = ModalView(size_hint=(0.25, 0.25), background_color=(0, 0, 0, 0.6))
        view.add_widget(userSettings.Permission(opDetail))
        view.open()

class LeaveButton(Button, MouseOver):
    #def on_hover(self, *args):
    #    self.view = ModalView(size_hint=(0.1, 0.1), background_color=(0, 0, 0, 0.6))
    #    #self.view.pos = (self.pos[0], self.pos[1])
    #    self.view.add_widget(Label(text='test'))
    #    self.view.open()

    #def on_exit(self, *args):
    #    try:
    #        self.view.dismiss()
    #    except:
    #        pass

    def set_bgGray(self):
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 0.50)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def setUP(self):
        self.color = (1, 0, 0, 0)
        with self.canvas.before:
            #Color(1, 0, 0, 0.50)
            self.rect = Rectangle(source='icons/leave/UP.png', pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def setP(self):
        self.color = (0, 1, 0, 0)
        with self.canvas.before:
            #Color(1, 0, 0, 0.50)
            self.rect = Rectangle(source='icons/leave/P.png', pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def setPE(self):
        self.color = (0, 0, 1, 0)
        with self.canvas.before:
            #Color(1, 0, 0, 0.50)
            self.rect = Rectangle(source='icons/leave/PE.png', pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_touch_up(self, touch):
        if touch.button == 'right':
            try:
                self.view.dismiss()
            except:
                self.view = ModalView(size_hint=(0.1, 0.1), background_color=(0, 0, 0, 0.6))
                self.view.pos_hint={'x' : touch.spos[0], 'top' : touch.spos[1]}
                self.view.add_widget(Label(text='test'))
                self.view.open()
        if touch.button == 'left':
            if self.collide_point(touch.x, touch.y):
                self.popup = PopMenuLeave()
                self.popup.open_pop(touch)

detail = 0

class PopMenuPerm(ModalView):
    def __init__(self, **args):
        super(PopMenuPerm, self).__init__(**args)
        self.size_hint = (None, None)
        self.height = 50
        self.width = 50

    def open_pop(self, touch):
        self.pos_hint={'x' : touch.spos[0], 'top' : touch.spos[1]}
        self.open()

    def acceptLeave(self):
        self.dismiss()
        global detail
        p = leaveData.grant_perm(detail)

    def declineLeave(self):
        self.dismiss()
        global detail
        p = leaveData.decline_perm(detail)

class PermissionButton(LeaveButton):
    def __init__(self, **args):
        super(PermissionButton, self).__init__(**args)
        self.size_hint_y=None
        self.height=30
        self.on_touch_up = self.popM
        self.set_bgYellow()

    def popM(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.popup = PopMenuPerm()
            self.popup.open_pop(touch)

    def set_bgYellow(self):
        #self.text = 'LR'
        self.color = (1, 1, 0, 0)
        with self.canvas.before:
            #Color(1, 1, 0, 0.50)
            self.rect = Rectangle(source='icons/leave/LR.png', pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class LeaveDetLayout(BoxLayout):
    def __init__(self, **args):
        super(LeaveDetLayout, self).__init__(**args)
        self.artistDetList = usersListManip.getUserInfo()
        self.setup()
        self.init_ui()

    def init_ui(self):
        self.sm1 = ScreenManager(pos_hint={"top": .9}, size_hint=(1, .9))
        self.ids.dateInfo.add_widget(self.sm1)

        self.sm2 = ScreenManager(pos_hint={"top": 1}, size_hint=(1, 1))
        self.ids.details.add_widget(self.sm2)

        self.ids.artistlist.rows = len(self.artistDetList['artistId'])
        self.ids.artistlist.bind(minimum_height=self.ids.artistlist.setter('height'))
        for a in self.artistDetList['artistName']:
            artistLbl = ArtistLabel(text="{}".format(a), size_hint_y=None, color=(0, 0, 0, 1), height=30)
            self.ids.artistlist.add_widget(artistLbl)

        self.create_leave_scr()

    def create_leave_scr(self):
        Det = leaveData.getDetails(self.months.index(self.dispMonth)+1, self.dispYear, self.artistDetList['artistId'])
        #print(Det)

        days = DaysScreen()
        days.name = self.ids.monthName.text
        daysNum = DaysGrid(rows=2)
        daysNum.cols = self.numOfDays[1]
        for i in range(1, self.numOfDays[1]+1):
            dayNumLbl = DaysNumLabel(text='{}'.format(i), color=(0, 0, 0, 1), )
            daysNum.add_widget(dayNumLbl)
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        l = 0
        w = self.numOfDays[0]
        while l < (self.numOfDays[1]):
            wd = weekdays[w]
            weekDaysLbl = DaysLabel(text='{}'.format(wd), color=(0, 0, 0, 1))
            if wd == 'Sun':
                weekDaysLbl.set_bgGray()
            l += 1
            w += 1
            if w == 7:
                w = 0
            if l > (self.numOfDays[1]+1):
                break
            daysNum.add_widget(weekDaysLbl)
        days.add_widget(daysNum)
        self.sm1.add_widget(days)

        # starting to add chart
        charts = ChartScreen()
        charts.name = self.ids.monthName.text
        self.chartScroll = ChartScroll(size_hint= (1, 1))
        #self.chartScroll.bind(scroll_y=lambda x:self.scroll_sync) #.ids.scroll_a.scroll_y
        self.chartScroll.bind(scroll_y=self.scroll_sync)
        leaveGrid = ChartGrid()
        leaveGrid.bind(minimum_height=leaveGrid.setter('height'))
        leaveGrid.size_hint=(1, None)
        leaveGrid.rows = len(self.artistDetList['artistId'])
        leaveGrid.cols = self.numOfDays[1]
        leaveGrid.padding = (0, 1, 0, 0)

        def callback(wid, touch):
            global detail
            det = wid.text.split(".")
            detail = [det[0], det[1]]

        def opCall(wid, touch):
            global opDetail
            det = wid.text.split(".")
            opDetail = [det[0], det[1]]

        for r in range(leaveGrid.rows):
            #print(Det[r]['leaveDates'][0])
            leaveDates = Det[r]['leaveDates']
            planned = Det[r]['planned']
            requests = Det[r]['leave_requests']
            permissions = Det[r]['permission']
            l = 0
            w = self.numOfDays[0]
            for c in range(leaveGrid.cols):
                curDate = "{}-{}-{}".format(self.dispYear, str(self.months.index(self.dispMonth)+1).zfill(2), str(c+1).zfill(2))
                lvBtn = LeaveButton(text='{}.{}'.format(Det[r]['id'], curDate), size_hint_y=None, height=30)
                lvBtn.bind(on_touch_down =opCall)
                wd = weekdays[w]
                try:
                    if curDate in leaveDates:
                        lvBtn.setUP()
                except Exception as e:
                    print(e)
                    pass
                if curDate in planned:
                    lvBtn.setP()
                if curDate in permissions:
                    lvBtn.setPE()
                if curDate in requests:
                    lvBtn = PermissionButton(text='{}.{}'.format(Det[r]['id'], curDate))
                    lvBtn.bind(on_touch_down =callback)
                if wd == 'Sun':
                    lvBtn.set_bgGray()
                l += 1
                w += 1
                if w == 7:
                    w = 0
                if l > (self.numOfDays[1]+1):
                    break
                leaveGrid.add_widget(lvBtn)

        self.chartScroll.add_widget(leaveGrid)
        charts.add_widget(self.chartScroll)
        self.sm2.add_widget(charts)

    def setup(self):
        self.months = calendar_data.get_month_names()
        self.today = datetime.today()
        self.dispMonth = self.months[self.today.month - 1]
        self.dispYear = self.today.year
        self.numOfDays = monthrange(self.dispYear, self.today.month)
        self.ids.monthName.text = "{} - {}".format(self.dispMonth, self.dispYear)

    def go_prev(self):
        self.dispMonth = self.months[self.months.index(self.dispMonth) - 1]
        if self.dispMonth == self.months[-1]:
            self.dispYear -= 1
        self.numOfDays = monthrange(self.dispYear, self.months.index(self.dispMonth)+1)
        self.ids.monthName.text = "{} - {}".format(self.dispMonth, self.dispYear)

        if not self.sm1.has_screen(self.ids.monthName.text) and not self.sm2.has_screen(self.ids.monthName.text):
            print("creating screen1")
            self.create_leave_scr()

        self.sm1.current = self.ids.monthName.text
        self.sm2.current = self.ids.monthName.text
        self.sm1.transition.direction = "left"
        self.sm2.transition.direction = "left"

    def go_next(self):
        if self.months.index(self.dispMonth) == 11:
            self.dispMonth = self.months[0]
            self.dispYear += 1
            self.numOfDays = monthrange(self.dispYear, self.months.index(self.dispMonth)+1)
            self.ids.monthName.text = "{} - {}".format(self.dispMonth, self.dispYear)

            if not self.sm1.has_screen(self.ids.monthName.text):
                print("creating screen1")
                self.create_leave_scr()

            self.sm1.current = self.ids.monthName.text
            self.sm1.transition.direction = "right"

            if not self.sm2.has_screen(self.ids.monthName.text):
                print("creating screen2")
                self.create_leave_scr()

            self.sm2.current = self.ids.monthName.text
            self.sm2.transition.direction = "right"

            return 0

        self.dispMonth = self.months[self.months.index(self.dispMonth) + 1]
        self.numOfDays = monthrange(self.dispYear, self.months.index(self.dispMonth)+1)
        self.ids.monthName.text = "{} - {}".format(self.dispMonth, self.dispYear)

        if not self.sm1.has_screen(self.ids.monthName.text):
            print("creating screen")
            self.create_leave_scr()
        self.sm1.current = self.ids.monthName.text
        self.sm1.transition.direction = "right"

        if not self.sm2.has_screen(self.ids.monthName.text):
            print("creating screen")
            self.create_leave_scr()

        self.sm2.current = self.ids.monthName.text
        self.sm2.transition.direction = "right"

    def scroll_sync(self, instance, value):
        self.ids.scroll_a.scroll_y = self.chartScroll.scroll_y
