from kivy.lang import Builder
from KivyCalendar import DatePicker
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from db import leaveData
from pages import Dialog

Data = []

Builder.load_string("""
<LeaveLayout>:
    orientation: 'vertical'
    BoxLayout:
        orientation: 'horizontal'
        Label:
            text: 'Name'
        TextInput:
            id: uname
            multiline: False
            readonly: True
            write_tab: False
    BoxLayout:
        orientation: 'horizontal'
        Label:
            text: 'Employee ID'
        TextInput:
            id: eid
            multiline: False
            readonly: True
            write_tab: False
    BoxLayout:
        orientation: 'horizontal'
        Label:
            text: 'Department'
        TextInput:
            id: dept
            multiline: False
            readonly: True
            write_tab: False
    BoxLayout:
        orientation: 'horizontal'
        Label:
            text: 'Date Range'
        DatePicker:
            id: fromDate
            pHint: (0.25, 0.25)
        DatePicker:
            id: toDate
            pHint: (0.25, 0.25)
    BoxLayout:
        orientation: 'horizontal'
        Label:
            text: 'Reason'
        TextInput:
            id: reason
            write_tab: False
    Button:
        text: 'Request for Leave'
        on_release: root.request_for_leave()
""")

class LeaveLayout(BoxLayout):
    def __init__(self, **args):
        super(LeaveLayout, self).__init__(**args)
        global Data
        self.ids.uname.text = Data[len(Data)-1][0]
        self.ids.eid.text = str(Data[len(Data)-1][1])
        self.ids.dept.text = Data[len(Data)-1][2]
        #self.ids.leaveDays.text = int(self.ids.toDate.text.split["."][0]) - int(self.ids.fromDate.text.split["."][0])
        #print(self.ids.fromDate.text().split["."][0])

    def request_for_leave(self):
        id = self.ids.eid.text
        from_date = self.format_date(self.ids.fromDate.text)
        to_date = self.format_date(self.ids.toDate.text)
        reason = self.ids.reason.text

        up = leaveData.upload_to_db(id, from_date, to_date, reason)
        if up == 1:
            def callback(instance):
                if instance.text == 'OK':
                    pop.dismiss()
                    return 0
            closePopBtn = Button(text="OK", size_hint=(1, 0.25))
            closePopBtn.bind(on_release=callback)
            pop = Dialog.dialog("Success !!!", "Leave request has been successfully submitted", closePopBtn)
            pop.open()

    def format_date(self, date):
        date = date.split(".")
        return ("{}-{}-{}".format(date[2], date[1], date[0]))
