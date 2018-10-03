import calendar
import datetime
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from db import monthlyWrkHours

month = []
months = ['January ', 'Feburary ', 'March ', 'April ', 'May ', 'June ', 'July ', 'August ', 'September ', 'October ', 'November ', 'December ']

def workTime():
    StdWrkHrs = datetime.timedelta(hours=8, minutes=29, seconds=59)
    global month, months

    mon = month[len(month)-1].split("-")
    workTime.year = int(mon[1])
    workTime.mont = int(months.index(mon[0])+1)
    Sundays = len([1 for i in calendar.monthcalendar(int(mon[1]), months.index(mon[0])+1) if i[6] != 0])
    No_of_days = calendar.monthrange(int(mon[1]), months.index(mon[0])+1)
    totWorkingdays = (No_of_days[1] - Sundays)
    workTime.totWorkingTime = StdWrkHrs * totWorkingdays

def ActualWorkingTime():
    return(monthlyWrkHours.calMonWrkHrs(workTime.year, workTime.mont))

class MonPop(GridLayout):
    def __init__(self, **args):
        super(MonPop, self).__init__(**args)
        self.cols = 2
        self.popUI()

    def popUI(self):
        actWorkingTime = ActualWorkingTime()
        details = ['Total Working Time : ', workTime.totWorkingTime, 'Actual Working Time :', actWorkingTime, 'Required Work Time :', (workTime.totWorkingTime-actWorkingTime)]
        for i in range(len(details)):
            lbl = Label(text=str(details[i]))
            self.add_widget(lbl)

def pop():
    tab = MonPop()
    popup = Popup(title="MONTHLY INFORMATION", content=tab, size_hint=(0.85, 0.85))
    popup.open()
