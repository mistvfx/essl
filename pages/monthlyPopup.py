import calendar
import datetime
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.lang import Builder

from db import monthlyWrkHours
import time

Builder.load_string("""
<MonPop>:
    spacing: 10
    padding: (10, 10, 10, 10)
    canvas.before:
        Color:
            rgba: (0, 0, 0, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<PopLabel>:
    color: (0, 0, 0, 1)
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            size: self.size
            pos: self.pos
""")

month = []
months = ['January ', 'Feburary ', 'March ', 'April ', 'May ', 'June ', 'July ', 'August ', 'September ', 'October ', 'November ', 'December ']

def calTotWorkingDays(totDays, curMonth, givMonth, curDate, givYear):
    holidays = monthlyWrkHours.getHolidays()
    calTotWorkingDays.artistLeaves = monthlyWrkHours.calArtistLeave(givYear, givMonth, curDate)
    #calTotWorkingDays.officeDefault = totDays
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
            if day == curDate and givMonth == curMonth:
                #print(days, hDays, calTotWorkingDays.artistLeaves)
                calTotWorkingDays.officeDefault = days-hDays
                return days-hDays-calTotWorkingDays.artistLeaves
            days += 1

    #print(days-hDays)

    calTotWorkingDays.officeDefault = days-hDays
    return days-hDays-calTotWorkingDays.artistLeaves


def workTime():
    StdWrkHrs = datetime.timedelta(hours=8, minutes=29, seconds=59)
    global month, months

    mon = month[len(month)-1].split("-")
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

    return ('{}:{}'.format(hours, minutes))

class PopLabel(Label, ):
    pass

class MonPop(GridLayout):
    def __init__(self, **args):
        super(MonPop, self).__init__(**args)
        self.cols = 5
        self.popUI()

    def popUI(self):
        DefTotWrkHrs = datetime.timedelta(hours=10, minutes=0, seconds=0)
        StdWrkHrs = datetime.timedelta(hours=8, minutes=29, seconds=59)
        actWorkingTime = ActualWorkingTime()
        totWorkingTime = TotalWorkingTime()
        if workTime.tarWorkingTime-actWorkingTime < datetime.timedelta():
            reqWorkTime = datetime.timedelta()
        else:
            reqWorkTime = (workTime.tarWorkingTime-actWorkingTime)

        if workTime.totWorkingdays*DefTotWrkHrs > totWorkingTime:
            reqTotTime = formatTime(workTime.totWorkingdays*DefTotWrkHrs-totWorkingTime)
        else:
            reqTotTime = formatTime(datetime.timedelta())

        twt = formatTime(totWorkingTime)

        tawt = formatTime(workTime.tarWorkingTime)

        awt = formatTime(actWorkingTime)

        rwt = formatTime(reqWorkTime)

        """'Total Target Actual Working Hours : \n ( %d * 8:30 )'%(workTime.totWorkingdays), '-', '-', tawt,"""

        details = ['PARTICULARS', 'DEFAULT', 'TARGET', 'CURRENT', 'INCOMPLETE',
                'Total Working Hours : \n \n DEFAULT << 10:00:00 X No. of DEFAULT Working Days \n TARGET << 10:00:00 X No. of TARGET Working Days \n CURRENT << Sum of Daily Total Working Hours', formatTime(calTotWorkingDays.officeDefault*DefTotWrkHrs), formatTime(workTime.totWorkingdays*DefTotWrkHrs), twt, reqTotTime,
                'Actual Working Hours : \n \n DEFAULT << 08:30:00 X No. of DEFAULT Working Days \n TARGET << 08:30:00 X No. of TARGET Working Days \n CURRENT << Sum of Daily Actual Working Hours', formatTime(calTotWorkingDays.officeDefault*StdWrkHrs), formatTime(workTime.totWorkingdays*StdWrkHrs), awt, rwt,
                'Working Days : \n \n DEFAULT << Office Working Days \n TARGET << Artist Working Days \n INCOMPLETE << Leaves', calTotWorkingDays.officeDefault, workTime.totWorkingdays, '-', calTotWorkingDays.artistLeaves]
        for i in range(len(details)):
            lbl = PopLabel(text=str(details[i]))
            if i in [0, 5, 10, 15]:
                lbl.size_hint_x = 0.60
                lbl.background_color = (0.5, 0.5, 0.5, 1)
            else:
                lbl.size_hint_x = 0.10

            if i in [0, 1, 2, 3, 4]:
                lbl.size_hint_y = 0.25
            self.add_widget(lbl)

def pop():
    tab = MonPop()
    popup = Popup(title="MONTHLY INFORMATION", content=tab, size_hint=(0.95, 0.85))
    popup.open()
