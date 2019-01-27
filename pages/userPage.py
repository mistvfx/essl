from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
#from KivyCalendar import CalendarWidget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from kivy.graphics import *
from kivy.lang import Builder
from kivy.properties import NumericProperty
from pages.navigationdrawer import NavigationDrawer

from db import getInfo, usersListManip
from pages import Calendar, table, navigationdrawer, infoPopup

#logoutButton = Button()
id = ''
user = ''
department = ''
date = ''

def init_data(data):
    global id, username, department
    id = data[0]
    print('id', id)
    user = data[1]
    department = data[2]
    return 0

Builder.load_string("""
#:import Window kivy.core.window.Window
#:import CalendarWidgetM pages.Calendar
#:import InfoTab pages.infoPopup
#:import NavigationDrawer pages.navigationdrawer
<UserPage>:
    NavigationDrawer:
        id: nav
        anim_type: 'fade_in'
        opening_transition: 'in_quint'
        closing_transition: 'out_cubic'
        BoxLayout:
            orientation: 'vertical'
            spacing: 2
            canvas.before:
                Color:
                    rgba: (1, 1, 1, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: 0.08

                # nav-close button
                Button:
                    size_hint_x: 0.40
                    background_normal: 'icons/nav_close.png'
                    background_down: 'icons/nav_close.png'
                    on_release: nav.toggle_state()
                Label:
                    text: 'EXTRAS'
                    color: (0, 0, 0, 1)
            LeaveReqButton:
                on_release: root.callback()
                size_hint_y: 0.1
            LeaveDetBtn:
                size_hint_y: 0.1
            Label:
                text: ''
        FloatLayout:
            size: (Window.width, Window.height)
            canvas.before:
                Color:
                    rgba: (189/255, 189/255, 189/255, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size

            # nav-open button
            Button:
                size_hint: (0.03, 0.06)
                pos_hint: {'top':1}
                on_release: nav.toggle_state()
                background_normal: 'icons/nav_open.png'
                background_down: 'icons/nav_open_1.png'
            UserLabel:
                id: userinfo
                pos_hint: {'center_y':0.98}
            OtherLayout:

            # calendar - daily - monthly
            BoxLayout:
                orientation: 'vertical'
                padding: (25, 0, 25, 25)
                spacing: 5
                size_hint_y: 0.90
                BoxLayout:
                    id: calendar_and_totalinfo
                    orientation: 'horizontal'
                    spacing: 5
                    CalendarWidgetM:
                        size_hint:(1, 1)
                        pos_hint:{'center_y':0.5, 'center_x':0.5}
                    InfoTab:
                        size_hint:(1, 1)
                        BoxLayout:
                            orientation: 'horizontal'
                            size_hint_y: 0.1
                            padding: (20, 15, 20, 15)
                            spacing: 5
                            canvas.before:
                                Color:
                                    rgba: (100/255, 200/255, 80/255, 1)
                                Rectangle:
                                    size: self.size
                                    pos: self.pos
                            Button:
                                text: 'Show Time Logs'
                                font_name: 'fonts/GoogleSans-Bold.ttf'
                                background_color: (1, 1, 1, 0)
                                on_release: root.open_io_pop()
                                canvas.before:
                                    Color:
                                        rgba: (76/255, 175/255, 80/255, 1)
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
                            Button:
                                text: 'TO_BE_ADDED'
                                font_name: 'fonts/GoogleSans-Bold.ttf'
                                background_color: (1, 1, 1, 0)
                                canvas.before:
                                    Color:
                                        rgba: (76/255, 175/255, 80/255, 1)
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
                MonPop:
                    size_hint:(0.75, 0.65)
                    pos_hint: {'center_x':0.5}


<OtherLayout>:
    orientation: 'horizontal'
    size_hint: (0.75, 0.05)
    pos_hint: {'center_y':0.92, 'center_x':0.5}
    spacing: 10
    padding: (10, 0, 0, 10)
    BoxLayout:
        orientation: 'horizontal'
        size_hint_x: 0.15
        canvas.before:
            Color:
                rgba: (1, 1, 1, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        Button:
            background_color: (255, 0, 0, 0.7)
            size_hint_x: 0.2
        InfoLabel:
            text: "Non Completed"
            font_name: 'fonts/GoogleSans-Bold.ttf'
            color: (0, 0, 0, 1)
    BoxLayout:
        orientation: 'horizontal'
        size_hint_x: 0.15
        canvas.before:
            Color:
                rgba: (1, 1, 1, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        Button:
            background_color: (0, 255, 0, 0.7)
            size_hint_x: 0.2
        InfoLabel:
            text: "Completed"
            font_name: 'fonts/GoogleSans-Bold.ttf'
            color: (0, 0, 0, 1)
    BoxLayout:
        orientation: 'horizontal'
        size_hint_x: 0.15
        canvas.before:
            Color:
                rgba: (1, 1, 1, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        Button:
            background_color: (255, 255, 0, 0.7)
            size_hint_x: 0.2
        InfoLabel:
            text: "Absent"
            font_name: 'fonts/GoogleSans-Bold.ttf'
            color: (0, 0, 0, 1)
    BoxLayout:
        orientation: 'horizontal'
        size_hint_x: 0.15
        canvas.before:
            Color:
                rgba: (1, 1, 1, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        Button:
            background_color: (0, 0, 255, 0.7)
            size_hint_x: 0.2
        InfoLabel:
            text: "Holiday"
            font_name: 'fonts/GoogleSans-Bold.ttf'
            color: (0, 0, 0, 1)
    BoxLayout:
        orientation: 'horizontal'
        size_hint_x: 0.15
        canvas.before:
            Color:
                rgba: (1, 1, 1, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        Button:
            background_color: (0.5, 0.5, 0.5, 1)
            size_hint_x: 0.2
        InfoLabel:
            text: "Sat/Sun"
            font_name: 'fonts/GoogleSans-Bold.ttf'
            color: (0, 0, 0, 1)

<UserLabel>:
    size_hint_y: 0.10
    bold: True
    color: (0, 0, 0, 1)
    font_name: 'fonts/moon-bold.otf'
    font_size: 25

<InfoLabel>:
    color: (0, 0, 0, 1)
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size

<LeaveReqButton>:
    text: 'Leave Request'
    background_color: (1, 1, 1, 0)
    canvas.before:
        Color:
            rgba: (0.7, 0.7, 0.7, 1)
        Rectangle:
            pos: self.pos
            size: self.size

<LeaveDetBtn>:
    text: 'Leave Details'
    background_color: (1, 1, 1, 0)
    canvas.before:
        Color:
            rgba: (0.7, 0.7, 0.7, 1)
        Rectangle:
            pos: self.pos
            size: self.size

<MailInfo>:
    orientation: 'vertical'
    FloatLayout:
        pos: self.pos
        size: self.size
        EmIn:
            id: omail
            readonly: False
            font_name: 'fonts/GoogleSans-Regular.ttf'
            multiline: False
            write_tab: False
            background_color: (1, 1, 1, 0)
            size_hint: (0.75, 0.75)
            pos_hint: {'top':0.8, 'center_x':0.5}
            on_text: self.update_padding()
            padding_x: (self.width - self.text_width) / 2
            padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
            canvas.before:
                Color:
                    rgba: (158/255, 158/255, 158/255, 1) #GERY-LIGHT
                Line:
                    width: 2
                    rectangle: (self.x, self.y, self.width, self.height)
        Label:
            text: 'Mail'
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

    Button:
        id: submitBtn
        text: "SUBMIT"
        font_name: 'fonts/GoogleSans-Medium.ttf'
        size_hint: (0.75, 1)
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        background_color: (1, 1, 1, 0)
        on_release: root.submit_email(omail.text)
        canvas.before:
            Color:
                rgba: (117/255, 117/255, 117/255, 1)
            RoundedRectangle:
                pos: self.pos
                size: self.size
""")
class UserPage(Screen):
    def __init__(self, **args):
        super(UserPage, self).__init__(**args)
        self.user()

    def user(self):
        global id, user, department

        print('lbl', id)
        self.ids.userinfo.text = '%s | %s | %s' %(id, user, department)

        haveMail = usersListManip.checkMail(id)
        if haveMail != 1:
            view = ModalView(size_hint=(0.25, 0.20), background_color=(0, 0, 0, 0.6))
            view.add_widget(MailInfo())
            view.open()

    def callback(instance):
        from pages import leaveReq
        leaveReq.Data.append([user, id, department])
        view = ModalView(size_hint=(0.5, 0.75), background_color=(0, 0, 0, 0.6))
        view.add_widget(leaveReq.LeaveLayout())
        view.open()

    def open_io_pop(self):
        infoPopup.UserTable()

class MailInfo(BoxLayout):
    def submit_email(self, mail):
        global id
        usersListManip.submit_email(id, mail)
        self.ids.submitBtn.text = "Thank You, press Esc to exit"

class EmIn(TextInput):
    text_width = NumericProperty()

    def update_padding(self, *args):
        self.text_width = self._get_text_width(
            self.text,
            self.tab_width,
            self._label_cached
        )

class UserLabel(Label):
    pass

class OtherLayout(BoxLayout):
    pass

class InfoLabel(Label):
    pass

class LeaveReqButton(Button):
    pass

class Test(Label):
    pass

class LeaveDetBtn(Button):
    def on_release(self):
        from pages import leaveReq
        global id
        leaveReq.feedbackPop(id)
