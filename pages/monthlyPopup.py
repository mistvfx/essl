import calendar
import datetime
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.properties import *
from kivy.clock import Clock

from db import monthlyWrkHours
import time
import threading
import datetime

date = ''

Builder.load_string("""
<MonPop>:
    spacing: 1
    padding: (2, 2, 2, 2)
    canvas.before:
        Color:
            rgba: (158/255, 158/255, 158/255, 1)
        Rectangle:
            size: self.size
            pos: self.pos
    MonLabel_Header:
        text:'PARTICULARS'
        size_hint: (0.60, 0.25)
    MonLabel_Header:
        text:'DEFAULT'
        size_hint: (0.10, 0.25)
    MonLabel_Header:
        text:'TARGET'
        size_hint: (0.10, 0.25)
    MonLabel_Header:
        text:'CURRENT'
        size_hint: (0.10, 0.25)
    MonLabel_Header:
        text:'INCOMPLETE'
        size_hint: (0.10, 0.25)
    PopLabel:
        size_hint_x: 0.60
        text: root.total_wrkhrs_info
    PopLabel:
        text: root.default_total_working_hours
        size_hint_x: 0.10
    PopLabel:
        text: root.target_total_working_hours
        size_hint_x: 0.10
    PopLabel:
        text: root.current_total_working_hours
        size_hint_x: 0.10
    PopLabel:
        text: root.incomplete_total_working_hours
        size_hint_x: 0.10
    PopLabel1:
        size_hint_x: 0.60
        text: root.actual_wrkhrs_info
    PopLabel1:
        text: root.default_actual_working_hours
        size_hint_x: 0.10
    PopLabel1:
        text: root.target_actual_working_hours
        size_hint_x: 0.10
    PopLabel1:
        text: root.current_actual_working_hours
        size_hint_x: 0.10
    PopLabel1:
        text: root.incomplete_actual_working_hours
        size_hint_x: 0.10
    PopLabel:
        size_hint_x: 0.60
        text: root.wrkdays_info
    PopLabel:
        text: root.total_working_days
        size_hint_x: 0.10
    PopLabel:
        text: root.artist_working_days
        size_hint_x: 0.10
    PopLabel:
        text: '-'
        size_hint_x: 0.10
    PopLabel:
        text: root.nonworking_days
        size_hint_x: 0.10

<PopLabel>:
    color: (0, 0, 0, 1)
    font_name: 'fonts/GoogleSans-Bold.ttf'
    markup: True
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<PopLabel1@PopLabel>:
    color: (0, 0, 0, 1)
    font_name: 'fonts/GoogleSans-Bold.ttf'
    markup: True
    canvas.before:
        Color:
            rgba: (224/255, 224/255, 224/255, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<MonLabel_Header>:
    color: (0, 0, 0, 1)
    font_name: 'fonts/GoogleSans-Bold.ttf'
    markup: True
    canvas.before:
        Color:
            rgba: (79/255, 195/255, 247/255, 1)
        Rectangle:
            size: self.size
            pos: self.pos
""")

month = []
months = ['January ', 'February ', 'March ', 'April ', 'May ', 'June ', 'July ', 'August ', 'September ', 'October ', 'November ', 'December ']

def calTotWorkingDays(totDays, curMonth, givMonth, curDate, givYear):
    today = datetime.datetime.strftime(datetime.datetime.today(), '%d:%m:%Y')
    holidays = monthlyWrkHours.getHolidays()
    calTotWorkingDays.artistLeaves = monthlyWrkHours.calArtistLeave(givYear, givMonth, curDate)
    days = 0
    hDays = 0
    month = calendar.monthcalendar(givYear, givMonth)
    for week in month:
        for day in week:
            for i in range(len(holidays)):
                if day == holidays[i][0] and givMonth == holidays[i][1] and givYear == holidays[i][2]:
                    hDays += 1
            if day == 0 or day == week[6]:
                continue
            if str(day).zfill(2) == today.split(":")[0] and str(givMonth).zfill(2) == today.split(":")[1]:
                calTotWorkingDays.officeDefault = days-hDays
                return days-hDays-calTotWorkingDays.artistLeaves
            days += 1

    #print(days-hDays)

    calTotWorkingDays.officeDefault = days-hDays
    return days-hDays-calTotWorkingDays.artistLeaves

def workTime(month):
    StdWrkHrs = datetime.timedelta(hours=8, minutes=29, seconds=59)
    global months

    mon = month.split("-")
    workTime.year = int(mon[1])
    try:
        workTime.mont = int(months.index(mon[0])+1)
    except:
        workTime.mont = int(mon[0])

    date = str(datetime.date.today()).split("-")

    try:
        Sundays = len([1 for i in calendar.monthcalendar(int(mon[1]), months.index(mon[0])+1) if i[6] != 0])
        No_of_days = calendar.monthrange(int(mon[1]), months.index(mon[0])+1)
    except:
        Sundays = len([1 for i in calendar.monthcalendar(int(mon[1]), int(mon[0])) if i[6] != 0])
        No_of_days = calendar.monthrange(int(mon[1]), int(mon[0]))

    workTime.totWorkingdays = calTotWorkingDays(No_of_days[1], int(date[1]), workTime.mont, int(date[2]), workTime.year)

    workTime.tarWorkingTime = StdWrkHrs * workTime.totWorkingdays

def ActualWorkingTime():
    return(monthlyWrkHours.calMonWrkHrs(workTime.year, workTime.mont))

def TotalWorkingTime():
    return(monthlyWrkHours.calMonTotWrkHrs(workTime.year, workTime.mont))

def formatTime(time):
    seconds = time.total_seconds()
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)

    if hours < 0:
        return ('0:0')

    return ('{}:{}'.format(hours, str(minutes).zfill(2)))

class PopLabel(Label):
    pass

class MonLabel_Header(Label):
    pass

class MonPop(GridLayout):
    # total
    total_wrkhrs_info = StringProperty('Total Working Hours : [font=fonts/GoogleSans-Regular.ttf]\n \n DEFAULT << 10:00:00 X No. of DEFAULT Working Days \n TARGET << 10:00:00 X No. of TARGET Working Days \n CURRENT << Sum of Daily Total Working Hours[/font]')
    default_total_working_hours = StringProperty('')
    target_total_working_hours = StringProperty('')
    current_total_working_hours = StringProperty('')
    incomplete_total_working_hours = StringProperty('')

    # actual
    actual_wrkhrs_info = StringProperty('Actual Working Hours : [font=fonts/GoogleSans-Regular.ttf]\n \n DEFAULT << 08:30:00 X No. of DEFAULT Working Days \n TARGET << 08:30:00 X No. of TARGET Working Days \n CURRENT << Sum of Daily Actual Working Hours[/font]')
    default_actual_working_hours = StringProperty('')
    target_actual_working_hours = StringProperty('')
    current_actual_working_hours = StringProperty('')
    incomplete_actual_working_hours = StringProperty('')

    # working days
    wrkdays_info = StringProperty('Working Days : [font=fonts/GoogleSans-Regular.ttf]\n \n DEFAULT << Office Working Days \n TARGET << Artist Working Days \n INCOMPLETE << Leaves[/font]')
    total_working_days = StringProperty('')
    artist_working_days = StringProperty('')
    nonworking_days = StringProperty('')

    def __init__(self, **args):
        super(MonPop, self).__init__(**args)

        self.prev_month = '-'

        self.cols = 5
        self.DefTotWrkHrs = datetime.timedelta(hours=10, minutes=0, seconds=0)
        self.StdWrkHrs = datetime.timedelta(hours=8, minutes=29, seconds=59)
        self.t1 = threading.Thread(target=self.startClock(id, date))
        self.t1.start()

    def startClock(self, id, date):
        self.dets = Clock.schedule_interval(lambda dt: self.popUI(), 0.5)

    def popUI(self):
        global month
        if month == self.prev_month:
            return
        else:
            self.prev_month = month

        workTime(month)

        actWorkingTime = ActualWorkingTime()
        totWorkingTime = TotalWorkingTime()
        if workTime.tarWorkingTime-actWorkingTime < datetime.timedelta():
            reqWorkTime = datetime.timedelta()
        else:
            reqWorkTime = (workTime.tarWorkingTime-actWorkingTime)

        if workTime.totWorkingdays*self.DefTotWrkHrs > totWorkingTime:
            reqTotTime = formatTime(workTime.totWorkingdays*self.DefTotWrkHrs-totWorkingTime)
        else:
            reqTotTime = formatTime(datetime.timedelta())

        twt = formatTime(totWorkingTime)

        tawt = formatTime(workTime.tarWorkingTime)

        awt = formatTime(actWorkingTime)

        rwt = formatTime(reqWorkTime)

        #total
        self.default_total_working_hours = formatTime(calTotWorkingDays.officeDefault*self.DefTotWrkHrs)
        self.target_total_working_hours = formatTime(workTime.totWorkingdays*self.DefTotWrkHrs)
        self.current_total_working_hours = twt
        self.incomplete_total_working_hours = reqTotTime

        #actual
        self.default_actual_working_hours = formatTime(calTotWorkingDays.officeDefault*self.StdWrkHrs)
        self.target_actual_working_hours = formatTime(workTime.totWorkingdays*self.StdWrkHrs)
        self.current_actual_working_hours = awt
        self.incomplete_actual_working_hours = rwt

        # wrkdays
        self.total_working_days = "{}".format(calTotWorkingDays.officeDefault)
        self.artist_working_days = "{}".format(workTime.totWorkingdays)
        self.nonworking_days = "{}".format(calTotWorkingDays.artistLeaves)

        """'Total Target Actual Working Hours : \n ( %d * 8:30 )'%(workTime.totWorkingdays), '-', '-', tawt,"""

        """details = ['PARTICULARS', 'DEFAULT', 'TARGET', 'CURRENT', 'INCOMPLETE',
                'Total Working Hours : [font=fonts/GoogleSans-Regular.ttf]\n \n DEFAULT << 10:00:00 X No. of DEFAULT Working Days \n TARGET << 10:00:00 X No. of TARGET Working Days \n CURRENT << Sum of Daily Total Working Hours[/font]', formatTime(calTotWorkingDays.officeDefault*DefTotWrkHrs), formatTime(workTime.totWorkingdays*DefTotWrkHrs), twt, reqTotTime,
                'Actual Working Hours : [font=fonts/GoogleSans-Regular.ttf]\n \n DEFAULT << 08:30:00 X No. of DEFAULT Working Days \n TARGET << 08:30:00 X No. of TARGET Working Days \n CURRENT << Sum of Daily Actual Working Hours[/font]', formatTime(calTotWorkingDays.officeDefault*StdWrkHrs), formatTime(workTime.totWorkingdays*StdWrkHrs), awt, rwt,
                'Working Days : [font=fonts/GoogleSans-Regular.ttf]\n \n DEFAULT << Office Working Days \n TARGET << Artist Working Days \n INCOMPLETE << Leaves[/font]', calTotWorkingDays.officeDefault, workTime.totWorkingdays, '-', calTotWorkingDays.artistLeaves]
        for i in range(len(details)):
            lbl = PopLabel(text=str(details[i]))
            if i in [0, 5, 10, 15]:
                lbl.size_hint_x = 0.60
                lbl.background_color = (0.5, 0.5, 0.5, 1)
            else:
                lbl.size_hint_x = 0.10

            if i in [0, 1, 2, 3, 4]:
                lbl.size_hint_y = 0.25
            self.add_widget(lbl)"""

def pop():
    tab = MonPop()
    popup = ModalView(size_hint=(0.95, 0.85))
    popup.add_widget(tab)
    popup.open()
