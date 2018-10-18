from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty

from . import calendar_data as cal_data
from db import getInfo, monthlyWrkHours
from pages import monthlyPopup, Dialog

aboveSWH = []
belowSWH = []
holidays = []

class CalendarWidget(RelativeLayout):
    """ Basic calendar widget """

    def __init__(self, as_popup=False, touch_switch=False, *args, **kwargs):
        super(CalendarWidget, self).__init__(*args, **kwargs)

        self.as_popup = as_popup
        self.touch_switch = touch_switch
        self.prepare_data()
        self.init_ui()

    def init_ui(self):

        self.left_arrow = Button(text="<", on_press=self.go_prev,
                                      pos_hint={"top": 1, "left": 0}, size_hint=(.1, .1))

        self.right_arrow = Button(text=">", on_press=self.go_next,
                                       pos_hint={"top": 1, "right": 1}, size_hint=(.1, .1))

        self.add_widget(self.left_arrow)
        self.add_widget(self.right_arrow)

        def callback(instance):
            monthlyPopup.month.append(self.title)
            monthlyPopup.workTime()
            monthlyPopup.pop()

        # Title
        self.title_label = Button(text=self.title, pos_hint={"top": 1, "center_x": .5}, size_hint=(None, 0.15), halign=("center"))
        self.title_label.bind(on_press=callback)
        self.add_widget(self.title_label)

        # ScreenManager
        self.sm = ScreenManager(pos_hint={"top": .9}, size_hint=(1, .9))
        self.add_widget(self.sm)

        self.create_month_scr(self.quarter[1], toogle_today=True)

    def create_month_scr(self, month, toogle_today=False):
        """ Screen with calendar for one month """
        #print(self.active_date[0], self.active_date[1], self.active_date[2])

        scr = Screen()
        m = self.month_names_eng[self.active_date[1] - 1]
        scr.name = "%s-%s" % (m, self.active_date[2])  # like march-2015

        # Grid for days
        grid_layout = GridLayout(cols=7, rows=7, size_hint=(1, 1), pos_hint={"top": 1})
        scr.add_widget(grid_layout)

        # Days abbrs
        for i in range(7):
            if i >= 5:  # weekends
                l = Label(text=self.days_abrs[i], color=(1, 0, 0, 1))
            else:  # work days
                l = Label(text=self.days_abrs[i], text_size=(self.size[0], None), halign="center")

            grid_layout.add_widget(l)

        global aboveSWH, belowSWH, holidays

        # Buttons with days numbers
        for week in month:
            for day in week:
                if day[1] >= 6:  # weekends
                    self.tbtn = Button(text=str(day[0]), background_color=(1, 0, 0, 1), color=(0, 0, 0, 1))
                else:
                    self.tbtn = Button(text=str(day[0]), background_color=(255, 255, 255, 1), color=(0, 0, 0, 1))
                    for i in range(len(aboveSWH)):
                        if self.active_date[2] == aboveSWH[i][2]:
                            if self.active_date[1] == aboveSWH[i][1]:
                                if self.tbtn.text == str(aboveSWH[i][0]):
                                    self.tbtn.background_color=(0, 255, 0, 1)
                    for i in range(len(belowSWH)):
                        if self.active_date[2] == belowSWH[i][2]:
                            if self.active_date[1] == belowSWH[i][1]:
                                if self.tbtn.text == str(belowSWH[i][0]):
                                    self.tbtn.background_color=(255, 0, 0, 1)
                    for i in range(len(holidays)):
                        if self.active_date[1] == holidays[i][1]:
                            if day[0] == holidays[i][0]:
                                self.tbtn.background_color=(0, 0, 255, 1)

                self.tbtn.bind(on_press=self.get_btn_value)

                if toogle_today:
                    # Down today button
                    if day[0] == self.active_date[0] and day[2] == 1:
                        self.tbtn.state = "down"
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

        self.active_date[0] = int(inst.text)

        getInfo.date.append(self.active_date)

        if self.as_popup:
            self.parent_popup.dismiss()

        try:
            getInfo.openPopup()
        except Exception as e:
            print(e)
            def callback(instance):
                if instance.text == 'OK':
                    pop.dismiss()
            closePopBtn = Button(text="OK", size_hint=(1, 0.25))
            closePopBtn.bind(on_release=callback)
            pop = Dialog.dialog("No Data !!!", "No data Available for the selected date !!", closePopBtn)
            pop.open()

    def go_prev(self, inst):
        """ Go to screen with previous month """

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

    def go_next(self, inst):
        """ Go to screen with next month """

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

    def on_touch_move(self, touch):
        """ Switch months pages by touch move """

        if self.touch_switch:
            # Left - prev
            if touch.dpos[0] < -30:
                self.go_prev(None)
            # Right - next
            elif touch.dpos[0] > 30:
                self.go_next(None)
