from kivy.lang import Builder
from KivyCalendar import DatePicker
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.textinput import TextInput
from kivy.graphics import *

from db import leaveData, ExchangeMail
from pages import Dialog
from pages.specialFeatures import *

Data = []
id = 0

Builder.load_string("""
<LvLbl@Label>:
    font_name: 'fonts/GoogleSans-Bold.ttf'
    size_hint_x: 0.1
    size_hint_y: None
    text_size: self.width, None
    height: self.texture_size[1]
    halign: "center"
    valign: "middle"
    color: (0, 0, 0, 1)
    pos_hint: {'center_y':0.82, 'center_x':0.25}
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size

<LvIn>:
    font_name: 'fonts/GoogleSans-Regular.ttf'
    multiline: False
    write_tab: False
    background_color: (1, 1, 1, 0)
    size_hint: (0.75, 0.75)
    pos_hint: {'top':0.8, 'center_x':0.5}
    on_text: root.update_padding()
    padding_x: (self.width - self.text_width) / 2
    padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
    canvas.before:
        Color:
            rgba: (158/255, 158/255, 158/255, 1) #GERY-LIGHT
        Line:
            width: 2
            rectangle: (self.x, self.y, self.width, self.height)

<CDatePicker@DatePicker>:
    background_color: (1, 1, 1, 0)
    font_name: 'fonts/GoogleSans-Regular.ttf'
    size_hint: (0.75, 0.75)
    pos_hint: {'top':0.8, 'center_x':0.5}
    padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
    canvas.before:
        Color:
            rgba: (0, 0, 0, 1)
        Line:
            width: 2
            rectangle: (self.x, self.y, self.width, self.height)

<LvFlt>:
    size_hint_y: 0.4

<LeaveLayout>:
    orientation: 'horizontal'
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        spacing: 2
        #### TOP LABEL ####
        Label:
            text: 'Leave Request Form'
            font_name: 'fonts/GoogleSans-Bold.ttf'
            size_hint_y: 0.02
            canvas.before:
                Color:
                    rgba: (117/255, 117/255, 117/255, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size

        #### UNAME, DEPT ####

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.05

            #### UANME ####
            LvFlt:
                pos: self.pos
                size: self.size
                size_hint_y: 1
                LvIn:
                    id: uname
                    readonly: True
                LvLbl:
                    text: 'Name'
                    size_hint_x: 0.15

            #### ID ####
            LvFlt:
                pos: self.pos
                size: self.size
                size_hint_y: 1
                LvIn:
                    id: eid
                    readonly: True
                LvLbl:
                    text: 'ID'
                    size_hint_x: 0.06

            #### DEPT ####
            LvFlt:
                pos: self.pos
                size: self.size
                size_hint_y: 1
                LvIn:
                    id: dept
                    readonly: True
                LvLbl:
                    text: 'Dept'
                    size_hint_x: 0.13

        #### DATE RANGE ####
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.05

            #### FROM ####
            LvFlt:
                pos: self.pos
                size: self.size
                size_hint_y: 1
                CDatePicker:
                    id: fromDate
                    pHint: (0.25, 0.25)
                    on_text: root.total_days()
                LvLbl:
                    text: 'FROM'
                    size_hint_x: 0.12

            #### TO ####
            LvFlt:
                pos: self.pos
                size: self.size
                size_hint_y: 1
                CDatePicker:
                    id: toDate
                    pHint: (0.25, 0.25)
                    on_text: root.total_days()
                LvLbl:
                    text: 'TO'

        #### LEAVE TYPE, TOTAL LEAVES####
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.06
            spacing: 1
            canvas.before:
                Color:
                    rgba: (0, 0, 0, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size

            #### EL ####
            LvFlt:
                pos: self.pos
                size_hint: (0.25, 1)
                canvas.before:
                    Color:
                        rgba: (1, 1, 1, 1)
                    Rectangle:
                        pos: self.pos
                        size: self.size
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint: (0.3, 0.25)
                    pos_hint: {'top':0.9, 'right':0.3}
                    CheckBox:
                        id: el
                        background_checkbox_normal: 'icons/checkbox/off.png'
                        background_checkbox_down: 'icons/checkbox/on_red.png'
                    Label:
                        id: avail_el
                        text: 'EL: 0'
                        color: (0, 0, 0, 1)
                LvIn:
                    id: el_days
                    size_hint: (0.5, 0.5)
                    pos_hint: {'center_x':0.5, 'top':0.5}
                    on_text: root.check_total_days()

            #### CL ####
            LvFlt:
                pos: self.pos
                size_hint: (0.25, 1)
                canvas.before:
                    Color:
                        rgba: (1, 1, 1, 1)
                    Rectangle:
                        pos: self.pos
                        size: self.size
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint: (0.30, 0.25)
                    pos_hint: {'top':0.9, 'right':0.30}
                    CheckBox:
                        id: cl
                        background_checkbox_normal: 'icons/checkbox/off.png'
                        background_checkbox_down: 'icons/checkbox/on_red.png'
                    Label:
                        id: avail_cl
                        text: 'CL: 0'
                        color: (0, 0, 0, 1)
                LvIn:
                    id: cl_days
                    size_hint: (0.5, 0.5)
                    pos_hint: {'center_x':0.5, 'top':0.5}
                    on_text: root.check_total_days()

            #### LOP ####
            LvFlt:
                pos: self.pos
                size_hint: (0.25, 1)
                canvas.before:
                    Color:
                        rgba: (1, 1, 1, 1)
                    Rectangle:
                        pos: self.pos
                        size: self.size
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint: (0.25, 0.25)
                    pos_hint: {'center_x':0.5, 'center_y':0.5}
                    CheckBox:
                        id: lop
                        background_checkbox_normal: 'icons/checkbox/off.png'
                        background_checkbox_down: 'icons/checkbox/on_orange.png'
                    Label:
                        text: 'LOP'
                        color: (0, 0, 0, 1)

            #### TOTAL LEAVE DAYS ####
            LvFlt:
                pos: self.pos
                size_hint: (0.25, 1)
                canvas.before:
                    Color:
                        rgba: (1, 1, 1, 1)
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    id: total_day
                    color: (0, 0, 0, 1)
                    size_hint: (0.25, 0.25)
                    pos_hint: {'center_x':0.5, 'center_y':0.5}

        LvFlt:
            pos: self.pos
            size_hint: (1, 0.2)
            LvIn:
                id: reason
                write_tab: False
                multiline: True
            LvLbl:
                text: 'Reason'

        LvFlt:
            pos: self.pos
            size_hint_y: 0.025
            LvBtn:
                text: 'Request for Leave'
                pos_hint: {'center_x':0.6, 'center_y':0.5}
                on_release: root.request_for_leave()
            LvBtn:
                text: 'Cancel'
                pos_hint: {'center_x':0.86, 'center_y':0.5}
                on_release: root.cancel()

<LvBtn>:
    font_name: 'fonts/GoogleSans-Medium.ttf'
    size_hint: (0.25, 1)
    background_color: (1, 1, 1, 0)
    color: (0, 0, 0, 1)

<FbLabel@Label>:
    color: (0, 0, 0, 1)
    font_name: 'fonts/GoogleSans-Bold.ttf'
    markup: True
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size


<Feedback>:
    orientation: 'horizontal'
    size_hint_y: None
    height: 25
    spacing: 1
    canvas.before:
        Color:
            rgba: (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    FbLabel:
        id: from_date
        text: 'FROM'
    FbLabel:
        id: to_date
        text: 'TO'
    FbLabel:
        id: type
        text: 'TYPE'
    FbLabel:
        id: app_date
        text: 'Applied Date'
    FbLabelScroll:
        id: reasons
        FbLabel:
            id: reason
            size_hint_y: None
            height: self.texture_size[1]*1.5
            text_size: self.width, None
            text: 'REASON'
    FbLabel:
        id: status
        text: 'STATUS'
""")
class LvIn(TextInput):
    text_width = NumericProperty()

    def update_padding(self, *args):
        self.text_width = self._get_text_width(
            self.text,
            self.tab_width,
            self._label_cached
        )

class LvBtn(Button, MouseOver):
    def on_hover(self):
        self.color = (1, 1, 1, 1)
        with self.canvas.before:
                Color(117/255, 117/255, 225/255, 1)
                Rectangle(pos= self.pos, size= self.size)

    def on_exit(self):
        self.color = (0, 0, 0, 1)
        with self.canvas.before:
                Color(1, 1, 1, 1)
                Rectangle(pos= self.pos, size= self.size)

class Feedback(BoxLayout):
    pass

class LvFlt(FloatLayout):
    pass

class FbLabelScroll(ScrollView):
    pass

class FeedbackLayout(ScrollView):
    def __init__(self, id):
        super().__init__()

        #global Data
        #id = str(Data[len(Data)-1][1])

        fbSign = {'P': '[color=#64DD17]APPROVED[/color]',
                  'LR': '[color=#9E9E9E]APPROVAL PENDING[/color]',
                  'R': '[color=#D50000]REJECTED[/color]',
                  'PE': 'PERMISSION'}

        layout = GridLayout(cols=1, spacing=3, padding=(0, 0, 0, 0), size_hint=(1, None))
        layout.bind(minimum_height=layout.setter('height'))

        dets = leaveData.getFeedback(id)

        layout.add_widget(Feedback())

        for data in dets:
            fb = Feedback()
            fb.ids.from_date.text = '[font=fonts/GoogleSans-Regular.ttf] {} [/font]'.format(data[0])
            fb.ids.to_date.text = '[font=fonts/GoogleSans-Regular.ttf] {} [/font]'.format(str(data[1]))
            fb.ids.type.text = '[font=fonts/GoogleSans-Regular.ttf] {} [/font]'.format(str(data[2]))
            fb.ids.app_date.text = '[font=fonts/GoogleSans-Regular.ttf] {} [/font]'.format(str(data[4]))
            fb.ids.reason.text = '[font=fonts/GoogleSans-Regular.ttf] {} [/font]'.format(data[5])
            marquee = Animation(scroll_y=-1, duration=10.0)
            marquee.start(fb.ids.reasons)
            fb.ids.status.text = fbSign['{}'.format(data[3])]
            layout.add_widget(fb)

        self.add_widget(layout)

def feedbackPop(id):
    #view = ModalView(size_hint=(None, None), size=(400, 400))
    view = ModalView(size_hint=(0.7, 0.5), background_color=(0, 0, 0, 0.6))
    fbl = FeedbackLayout(id)
    view.add_widget(fbl)
    view.open()

class LeaveLayout(BoxLayout):
    def __init__(self, **args):
        super(LeaveLayout, self).__init__(**args)
        global Data
        leave_data = leaveData.get_leaves_data(Data[len(Data)-1][1])
        self.ids.uname.text = Data[len(Data)-1][0]
        self.ids.eid.text = str(Data[len(Data)-1][1])
        self.ids.dept.text = Data[len(Data)-1][2]

        self.ids.avail_el.text = 'EL: {}'.format(leave_data[0])
        self.ids.avail_cl.text = 'CL: {}'.format(leave_data[1])
        #self.ids.leaveDays.text = int(self.ids.toDate.text.split["."][0]) - int(self.ids.fromDate.text.split["."][0])
        #print(self.ids.fromDate.text().split["."][0])

    def total_days(self):
        from datetime import datetime

        fro = datetime.strptime(self.ids.fromDate.text, '%d.%m.%Y').date()
        to = datetime.strptime(self.ids.toDate.text, '%d.%m.%Y').date()

        try:
            if fro != None and to != None:
                delta = to - fro
                self.ids.total_day.text = '{}'.format(delta.days+1)
        except Exception as e:
            print(e)
            pass

    def check_total_days(self):
        if self.ids.el.active and self.ids.el_days.text != '':
            el = int(self.ids.el_days.text)
        else:
            el = 0
        if self.ids.cl.active and self.ids.cl_days.text != '':
            cl = int(self.ids.cl_days.text)
        else:
            cl = 0

        if self.ids.total_day.text == '':
            return 0

        if (el + cl) != int(self.ids.total_day.text) or el > int(self.ids.avail_el.text.split(":")[-1]) or cl > int(self.ids.avail_cl.text.split(":")[-1]):
            if self.ids.el.active:
                with self.ids.el_days.canvas.before:
                        Color(225/255, 117/255, 117/255, 1)
                        Line(width= 2, rectangle= (self.ids.el_days.x, self.ids.el_days.y, self.ids.el_days.width, self.ids.el_days.height))
            if self.ids.cl.active:
                with self.ids.cl_days.canvas.before:
                        Color(225/255, 117/255, 117/255, 1)
                        Line(width= 2, rectangle= (self.ids.cl_days.x, self.ids.cl_days.y, self.ids.cl_days.width, self.ids.cl_days.height))
        elif (el + cl) == int(self.ids.total_day.text):
            if self.ids.el.active:
                with self.ids.el_days.canvas.before:
                        Color(117/255, 225/255, 117/255, 1)
                        Line(width= 2, rectangle= (self.ids.el_days.x, self.ids.el_days.y, self.ids.el_days.width, self.ids.el_days.height))
            if self.ids.cl.active:
                with self.ids.cl_days.canvas.before:
                        Color(117/255, 225/255, 117/255, 1)
                        Line(width= 2, rectangle= (self.ids.cl_days.x, self.ids.cl_days.y, self.ids.cl_days.width, self.ids.cl_days.height))

    def request_for_leave(self):
        id = self.ids.eid.text
        from_date = self.format_date(self.ids.fromDate.text)
        to_date = self.format_date(self.ids.toDate.text)
        if self.ids.el.active and self.ids.cl.active:
            type = '{}-{}:{}-{}'.format('EL', self.ids.el_days.text, 'CL', self.ids.cl_days.text)
        elif self.ids.el.active and not self.ids.cl.active:
            type = '{}-{}'.format('EL', self.ids.el_days.text)
        elif self.ids.cl.active and not self.ids.el.active:
            type = '{}-{}'.format('CL', self.ids.cl_days.text)
        elif self.ids.lop.active:
            type = 'LOP'
        reason = self.ids.reason.text

        eup = ExchangeMail.send_mail([id, from_date, to_date, type, reason])
        up = leaveData.upload_to_db(id, from_date, to_date, type, reason)
        if up == 1:
            from pages import kivytoast
            kivytoast.toast('Leave request has been successfully submitted', (0, 1, 0, 0.5), length_long=True)

    def format_date(self, date):
        date = date.split(".")
        return ("{}-{}-{}".format(date[2], date[1], date[0]))
