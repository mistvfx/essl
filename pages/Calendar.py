from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.lang import Builder
from kivy.graphics import Triangle
from kivy.graphics import Color

from datetime import datetime

from . import calendar_data as cal_data
from db import getInfo, monthlyWrkHours
from pages import monthlyPopup, Dialog

aboveSWH = []
belowSWH = []
reg = []
holidays = []
leaves = []
artistHolidays = 0

id = 0

Builder.load_string("""

<arrowBtn>:
    color: (0, 0, 0, 1)
    background_color: (0, 0, 0, 0)
    font_size: 50
    bold: True

<monthBtn>:
    color: (0, 0, 0, 1)
    background_color: (0, 0, 0, 0)
    font_name: 'fonts/moon-bold.otf'
    bold: True

<WrkDayLabel>:
    color: (0.1, 0.1, 0.1, 1)
    text_size: [self.size[0], None]
    background_color: (0.5, 0.5, 0.5, 1)
    font_name: 'fonts/moon.otf'
    halign: "center"

<WeekEndLabel>:
    color: (1, 0.26, 0.21, 1)
    font_name: 'fonts/moon.otf'

<CalendarWidgetM>:
    canvas.before:
        Color:
            rgba: (0.1, 0.1, 0.1, 0.2)
        Rectangle:
            pos: [self.pos[0] - self.pos[0]/1.03, self.pos[1] - self.pos[1]*1.06]
            size: self.size
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: [self.pos[0] - self.pos[0], self.pos[1] - self.pos[1]]
            size: self.size

<CalNormalButton>:
    background_color: (1, 1, 1, 1)
    FloatLayout:
        pos: self.parent.pos
        size: self.parent.size
        Label:
            id: calLbl
            bold: True
            font_size: 20
            size_hint: (0.10, 0.30)
            pos_hint: {'y':0, 'right':1}
            text: ''
            color: (0, 0, 0, 1)
            canvas.before:
                Color:
                    rgba: (1, 1, 1, 0)
                Rectangle:
                    pos: self.pos
                    size: self.size
""")

class arrowBtn(Button):
    pass

class monthBtn(Button):
    pass

class WrkDayLabel(Label):
    pass

class WeekEndLabel(Label):
    pass

class CalNormalButton(Button):
    pass

class CalendarWidgetM(RelativeLayout):
    """ Basic calendar widget """

    def __init__(self, as_popup=False, touch_switch=False, *args, **kwargs):
        super(CalendarWidgetM, self).__init__(*args, **kwargs)

        self.as_popup = as_popup
        self.touch_switch = touch_switch
        self.prepare_data()
        monthlyWrkHours.getHolidays()
        self.init_ui()

    def init_ui(self):

        self.left_arrow = arrowBtn(text="<", on_press=self.go_prev,
                                      pos_hint={"top": 1, "left": 0}, size_hint=(.1, .1))

        self.right_arrow = arrowBtn(text=">", on_press=self.go_next,
                                       pos_hint={"top": 1, "right": 1}, size_hint=(.1, .1))

        self.add_widget(self.left_arrow)
        self.add_widget(self.right_arrow)

        # Title
        self.title_label = monthBtn(text=self.title, pos_hint={"top": 1, "center_x": .5}, size_hint=(None, 0.15), halign=("center"))
        monthlyPopup.month.append(self.title)
        self.add_widget(self.title_label)

        # ScreenManager
        self.sm = ScreenManager(pos_hint={"top": .9}, size_hint=(1, .9))
        self.add_widget(self.sm)

        self.create_month_scr(self.quarter[1], toogle_today=True)

    def create_month_scr(self, month, toogle_today=False):
        """ Screen with calendar for one month """
        monthlyWrkHours.calArtistLeave(self.active_date[2], str(self.active_date[1]).zfill(2), str(self.active_date[0]).zfill(2))
        #self.active_date[0] = day, self.active_date[1] = month, self.active_date[2] = year

        scr = Screen()
        m = self.month_names_eng[self.active_date[1] - 1]
        scr.name = "%s-%s" % (m, self.active_date[2])  # like march-2015

        # Grid for days
        grid_layout = GridLayout(cols=7, rows=7, size_hint=(1, 1), pos_hint={"top": 1}, spacing = 2)
        scr.add_widget(grid_layout)

        # Days abbrs
        for i in range(7):
            if i >= 5:  # weekends
                l = WeekEndLabel(text=self.days_abrs[i])
            else:  # work days
                l = WrkDayLabel(text=self.days_abrs[i])

            grid_layout.add_widget(l)

        global aboveSWH, belowSWH, holidays, artistHolidays

        # Buttons with days numbers
        for week in month:
            for day in week:
                if day[1] >= 6:  # weekends
                    self.tbtn = CalNormalButton(text=str(day[0]), background_color=(0.5, 0.5, 0.5, 1), color=(1, 1, 1, 1))
                else:
                    self.tbtn = CalNormalButton(text=str(day[0]), background_color=(255, 255, 255, 1), color=(0, 0, 0, 1))
                    for i in range(len(aboveSWH)):
                        if self.active_date[2] == aboveSWH[i][2]:
                            if self.active_date[1] == aboveSWH[i][1]:
                                if self.tbtn.text == str(aboveSWH[i][0]):
                                    self.tbtn.background_color=(0, 255, 0, 0.7)
                    for i in range(len(belowSWH)):
                        if self.active_date[2] == belowSWH[i][2]:
                            if self.active_date[1] == belowSWH[i][1]:
                                if self.tbtn.text == str(belowSWH[i][0]):
                                    self.tbtn.background_color=(255, 0, 0, 0.7)
                    for i in range(len(reg)):
                        if self.active_date[2] == reg[i][2]:
                            if self.active_date[1] == reg[i][1]:
                                if self.tbtn.text == str(reg[i][0]):
                                    self.tbtn.ids.calLbl.text = 'R'
                    for i in range(len(leaves)):
                        if self.active_date[2] == leaves[i][2]:
                            if self.active_date[1] == leaves[i][1]:
                                if day[0] == (leaves[i][0]):
                                    self.tbtn.background_color=(255, 195, 0, 0.7)
                    for i in range(len(holidays)):
                        if self.active_date[2] == holidays[i][2]:
                            if self.active_date[1] == holidays[i][1]:
                                if day[0] == holidays[i][0]:
                                    self.tbtn.background_color=(0, 0, 255, 0.7)

                self.tbtn.bind(on_press=self.get_btn_value)

                """if toogle_today:
                    # Down today button
                    if day[0] == self.active_date[0] and day[2] == 1:
                        self.tbtn.state = "down"""
                # Disable buttons with days from other months
                if day[2] == 0:
                    self.tbtn.text = " "
                    self.tbtn.disabled = True
                    self.tbtn.background_color = (255, 255, 255, 1)

                grid_layout.add_widget(self.tbtn)

        self.sm.add_widget(scr)

    def prepare_data(self):
        """ Prepare data for showing on widget loading """

        # Get days abbrs and month names lists
        self.month_names = cal_data.get_month_names()
        self.month_names_eng = cal_data.get_month_names_eng()
        self.days_abrs = cal_data.get_days_abbrs()

        # Today date
        self.active_date = cal_data.today_date_list()
        # Set title
        self.title = "%s - %s" % (self.month_names[self.active_date[1] - 1],
                                  self.active_date[2])

        # Quarter where current month in the self.quarter[1]
        self.get_quarter()

    def get_quarter(self):
        """ Get caledar and months/years nums for quarter """

        self.quarter_nums = cal_data.calc_quarter(self.active_date[2],
                                                  self.active_date[1])
        self.quarter = cal_data.get_quarter(self.active_date[2],
                                            self.active_date[1])

    def get_btn_value(self, inst):
        """ Get day value from pressed button """
        from pages import userPage, infoPopup, table, monthlyPopup

        global id

        self.active_date[0] = int(inst.text)
        formatted_date = "{}:{}:{}".format(str(self.active_date[0]).zfill(2), str(self.active_date[1]).zfill(2), self.active_date[2])

        getInfo.date = formatted_date
        userPage.date = formatted_date
        infoPopup.date = formatted_date
        table.date = formatted_date
        monthlyPopup.date = formatted_date

        if self.as_popup:
            self.parent_popup.dismiss()

        #getInfo.getUserInfo(id, formatted_date)

    def go_prev(self, inst):
        """ Go to screen with previous month """
        monthlyWrkHours.calArtistLeave(self.quarter_nums[0][0], self.quarter_nums[0][1], self.active_date[0])

        # Change active date
        self.active_date = [self.active_date[0], self.quarter_nums[0][1],
                            self.quarter_nums[0][0]]

        # Name of prev screen
        n = self.quarter_nums[0][1] - 1
        prev_scr_name = "%s-%s" % (self.month_names_eng[n],
                                   self.quarter_nums[0][0])

        # If it's doen't exitst, create it
        if not self.sm.has_screen(prev_scr_name):
            self.create_month_scr(self.quarter[0])

        self.sm.current = prev_scr_name
        self.sm.transition.direction = "left"

        self.get_quarter()
        self.title = "%s - %s" % (self.month_names[self.active_date[1] - 1],
                                  self.active_date[2])

        self.title_label.text = self.title

        # assign title to monthlyPopup
        monthlyPopup.month.append(self.title)

    def go_next(self, inst):
        """ Go to screen with next month """
        monthlyWrkHours.calArtistLeave(self.quarter_nums[2][0], self.quarter_nums[2][1], self.active_date[0])

         # Change active date
        self.active_date = [self.active_date[0], self.quarter_nums[2][1],
                            self.quarter_nums[2][0]]

        # Name of prev screen
        n = self.quarter_nums[2][1] - 1
        next_scr_name = "%s-%s" % (self.month_names_eng[n],
                                   self.quarter_nums[2][0])

        # If it's doen't exitst, create it
        if not self.sm.has_screen(next_scr_name):
            self.create_month_scr(self.quarter[2])

        self.sm.current = next_scr_name
        self.sm.transition.direction = "right"

        self.get_quarter()
        self.title = "%s - %s" % (self.month_names[self.active_date[1] - 1],
                                  self.active_date[2])

        self.title_label.text = self.title

        # assign title to monthlyPopup
        monthlyPopup.month.append(self.title)

    def on_touch_move(self, touch):
        """ Switch months pages by touch move """

        if self.touch_switch:
            # Left - prev
            if touch.dpos[0] < -30:
                self.go_prev(None)
            # Right - next
            elif touch.dpos[0] > 30:
                self.go_next(None)
