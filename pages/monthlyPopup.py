import calendar
import datetime
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from db import monthlyWrkHours
import time

month = []
months = ['January ', 'Feburary ', 'March ', 'April ', 'May ', 'June ', 'July ', 'August ', 'September ', 'October ', 'November ', 'December ']

def calTotWorkingDays(totDays, curMonth, givMonth, curDate, givYear):
    holidays = monthlyWrkHours.getHolidays()
    artistLeaves = monthlyWrkHours.calArtistLeave(givYear, givMonth, curDate)
    days = 0
    hDays = 0
    month = calendar.monthcalendar(givYear, givMonth)
    for week in month:
        for day in week:
            for i in range(len(holidays)):
                if day == holidays[i][0] and givMonth == holidays[i][1]:
                    hDays += 1
            if day == 0 or day == week[6]:
                continue
            if day == curDate and givMonth == curMonth:
                return days-hDays-artistLeaves
            days += 1

    return days-hDays-artistLeaves


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

    totWorkingdays = calTotWorkingDays(No_of_days[1], int(date[1]), workTime.mont, int(date[2]), workTime.year)

    workTime.tarWorkingTime = StdWrkHrs * totWorkingdays

def ActualWorkingTime():
    return(monthlyWrkHours.calMonWrkHrs(workTime.year, workTime.mont))

def TotalWorkingTime():
    return(monthlyWrkHours.calMonTotWrkHrs(workTime.year, workTime.mont))

def formatTime(time):
    seconds = time.total_seconds()
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)

    return ('{}:{}:{}'.format(hours, minutes, seconds))

class MonPop(GridLayout):
    def __init__(self, **args):
        super(MonPop, self).__init__(**args)
        self.cols = 2
        self.popUI()

    def popUI(self):
        actWorkingTime = ActualWorkingTime()
        totWorkingTime = TotalWorkingTime()
        if workTime.tarWorkingTime-actWorkingTime < datetime.timedelta():
            reqWorkTime = datetime.timedelta()
        else:
            reqWorkTime = (workTime.tarWorkingTime-actWorkingTime)

        #twt = ("%.2f"%(round(totWorkingTime.total_seconds()/3600, 2)))
        twt = formatTime(totWorkingTime)

        #tawt = ("%.2f"%(round(workTime.tarWorkingTime.total_seconds()/3600, 2)))
        tawt = formatTime(workTime.tarWorkingTime)

        #awt = ("%.2f"%(round(actWorkingTime.total_seconds()/3600, 2)))
        awt = formatTime(actWorkingTime)

        #rwt = ("%.2f"%(round(reqWorkTime.total_seconds()/3600, 2)))
        rwt = formatTime(reqWorkTime)

        details = ['Total Working Hours (10:00:00): ', twt, 'Total Target Actual Working Hours :', tawt, 'Actual Working Hours :', awt, 'Not Completed Working Hours :', rwt]
        for i in range(len(details)):
            lbl = Label(text=str(details[i]), bold=True)
            self.add_widget(lbl)

def pop():
    tab = MonPop()
    popup = Popup(title="MONTHLY INFORMATION", content=tab, size_hint=(0.85, 0.85))
    popup.open()
