from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from datetime import datetime
from kivy.lang import Builder


from pages import calendar_data as cal_data, Dialog, kivytoast

selectedDates = []
holiday = []
halfday = []

Builder.load_string("""
<ToggleBtn>:
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<HolidayBtn>:
    font_name: 'fonts/moon-bold.otf'
    canvas.before:
        Color:
            rgba: (128, 0, 128, 0.5)
        Rectangle:
            pos: self.pos
            size: self.size

<HalfdayBtn>:
    font_name: 'fonts/moon-bold.otf'
    canvas.before:
        Color:
            rgba: (0, 255, 255, 0.25)
        Rectangle:
            pos: self.pos
            size: self.size
""")

class ToggleBtn(ToggleButton):
    pass

class HolidayBtn(ToggleButton):
    pass

class HalfdayBtn(ToggleButton):
    pass

class CalendarWidgetS(RelativeLayout):
    """ Basic calendar widget """

    def __init__(self, as_popup=False, touch_switch=False, *args, **kwargs):
        super(CalendarWidgetS, self).__init__(*args, **kwargs)

        self.as_popup = as_popup
        self.touch_switch = touch_switch
        #self.selectedDates = []
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
        self.title_label = Label(text=self.title, pos_hint={"top": 1, "center_x": .5}, size_hint=(None, 0.15), halign=("center"))
        self.add_widget(self.title_label)

        # ScreenManager
        self.sm = ScreenManager(pos_hint={"top": .9}, size_hint=(1, .9))
        self.add_widget(self.sm)

        self.create_month_scr(self.quarter[1], toogle_today=True)

    def create_month_scr(self, month, toogle_today=False):
        """ Screen with calendar for one month """

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

        global holiday, halfday

        # Buttons with days numbers
        for week in month:
            for day in week:
                if day[1] >= 6:  # weekends
                    self.tbtn = ToggleBtn(text=str(day[0]), color=(0, 0, 0, 1))
                else:
                    self.tbtn = ToggleBtn(text=str(day[0]), color=(0, 0, 0, 1))
                    print(self.active_date, holiday)
                    for i in range(len(holiday)):
                        if self.active_date[2] == holiday[i][2]:
                            if self.active_date[1] == holiday[i][1]:
                                if day[0] == holiday[i][0]:
                                    self.tbtn.background_color=(128, 0, 128, 1)
                    for i in range(len(halfday)):
                        if self.active_date[2] == halfday[i][2]:
                            if self.active_date[1] == halfday[i][1]:
                                if day[0] == halfday[i][0]:
                                    self.tbtn.background_color=(0, 255, 255, 0.5)

                self.tbtn.bind(on_press=self.get_btn_value)

                if toogle_today:
                    # Down today button
                    if day[0] == self.active_date[0] and day[2] == 1:
                        self.tbtn.state = "down"
                # Disable buttons with days from other months
                if day[2] == 0:
                    self.tbtn.text = " "
                    self.tbtn.disabled = True
                    self.tbtn.background_color = (0, 0, 0, 0.1)

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

        selected = [self.active_date[0], self.active_date[1], self.active_date[2]]

        global selectedDates

        if selected in selectedDates:
            selectedDates.remove(selected)
            #print(selectedDates)
        else:
            selectedDates.append(selected)
            #print(selectedDates)

        if self.as_popup:
            self.parent_popup.dismiss()

        #getInfo.openPopup()

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

import pymysql

def paintDates():
    global holiday, halfday
    db = pymysql.connect("10.10.5.60", "mcheck", "mcheck@123", "essl", autocommit=True, connect_timeout=1)
    cur = db.cursor()
    cur.execute("SELECT DAY, MONTH, YEAR, DETAIL FROM essl.month_details")

    for data in cur.fetchall():
        if data[3] == 'HOLIDAY':
            holiday.append([data[0], data[1], data[2]])
        else:
            halfday.append([data[0], data[1], data[2]])


def setup():

    paintDates()

    calSettingsLayout = BoxLayout(orientation='vertical')

    daySetLayout = BoxLayout(orientation='horizontal', size_hint_y=0.2)
    holidayBtn = HolidayBtn(text='HOLIDAY', size_hint_x=0.5, color=(128, 0, 128, 1), bold=True)
    daySetLayout.add_widget(holidayBtn)
    halfdayBtn = HalfdayBtn(text='HALF DAY', size_hint_x=0.5, color=(0, 255, 255, 0.5), bold=True)
    daySetLayout.add_widget(halfdayBtn)
    calSettingsLayout.add_widget(daySetLayout)

    cal = CalendarWidgetS()
    calSettingsLayout.add_widget(cal)

    def callback(instance):
        def call(instance):
            if instance.text == 'OK':
                pop.dismiss()
        global selectedDates
        if instance.text == 'SAVE':
            db = pymysql.connect("10.10.5.60", "mcheck", "mcheck@123", "essl", autocommit=True, connect_timeout=1)
            cur = db.cursor()
            closePopBtn = Button(text="OK", size_hint=(1, 0.25))
            closePopBtn.bind(on_release=call)
            if holidayBtn.state == 'down':
                for date in selectedDates:
                    cur.execute("INSERT INTO essl.month_details (DAY, MONTH, YEAR, DETAIL) VALUES(%d, %d, %d, 'HOLIDAY')" %(date[0], date[1], date[2]))
                kivytoast.toast('Holidays Applied', (0, 1, 0, 0.5), length_long=True)
            elif halfdayBtn.state == 'down':
                for date in selectedDates:
                    cur.execute("INSERT INTO essl.month_details (DAY, MONTH, YEAR, DETAIL) VALUES(%d, %d, %d, 'HALFDAY')" %(date[0], date[1], date[2]))
                kivytoast.toast('Halfdays Applied', (0, 1, 0, 0.5), length_long=True)

            cur.close()
            db.close()

    saveBtn = Button(text='SAVE', size_hint_y=0.2)
    saveBtn.bind(on_press=callback)
    calSettingsLayout.add_widget(saveBtn)

    popup = Popup(title='date settings', content=calSettingsLayout, size_hint=(0.65, 0.65))
    popup.open()
