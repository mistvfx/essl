from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from KivyCalendar import DatePicker
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.spinner import Spinner
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.vector import Vector

from . import excelIO
import threading
from pages import usersList, settings, leaveDet
from pages.specialFeatures import *
from db import usersListManip

Builder.load_string("""
<AdminPage>:
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 5
        BoxLayout:
            id: controlLayout
            orientation: 'horizontal'
            size_hint: (1, 0.06)
            spacing: 5
            ExcelImport:
                on_release: self.excelOpen()
            CDatePicker:
                id: date
                text: "SELECT DATE"
                size_hint: (0.5, 1)
                pHint: (0.35, 0.35)
                on_text: self.changeDate()
            ExcelExport:
                on_text: self.callexcel(self.text, date.text)
        FloatLayout:
            id: listLayout
            size_hint: (1, 1)

<ExcelImport>:
    text: "Import Excel"
    size_hint: (0.5, 1)
    color: (0, 0, 0, 0)
    background_color: (1, 1, 1, 0)
    StackLayout:
        pos: self.parent.pos
        size: self.parent.size
        orientation: 'lr-tb'
        Image:
            source: 'icons/importExcel.png'
            size_hint_x: None
        Label:
            size_hint_x: None
            text: "Import Excel"
            font_name: 'fonts/moon-bold.otf'
            color: (0, 0, 0, 1)

<ExcelExport>:
    text: "Excel Export"
    values: ('DAY', 'MONTH')
    size_hint: (0.5, 1)
    color: (0, 0, 0, 0)
    background_color: (0, 0, 0, 0)
    StackLayout:
        pos: self.parent.pos
        size: self.parent.size
        orientation: 'lr-tb'
        Image:
            source: 'icons/exportExcel.png'
            size_hint_x: None
        Label:
            size_hint_x: None
            text: "Excel Export"
            font_name: 'fonts/moon-bold.otf'
            color: (0, 0, 0, 1)

<ExcelExported>:
    size_hint: 0.5, 0.5
    background_color: (0, 0, 0, 0)
    Image:
        source: 'icons/export.gif'
        size: self.parent.size
        y: self.parent.y
        x: self.parent.x
        keep_data: True

<SetButton>:
    text: 'SETTINGS'
    color: (1, 1, 1, 0)
    background_color: (0, 0, 0, 0)
    pos_hint: {'left':1, 'bottom':1}
    size_hint: (0.05, 0.1)
    canvas:
        Color:
            rgba: (1,1,1,0)
        Ellipse:
            pos: self.pos
            size: self.size
    Image:
        id: setImg
        source: 'icons/settings.zip'
        size: self.parent.size
        anim_delay: -1
        anim_loop: 1

<LeaveDetails>
    text: 'Leave Details'
    color: (1, 1, 1, 0)
    background_color: (0, 0, 0, 0)
    pos_hint: {'y':0.1}
    size_hint: (0.05, 0.1)
    canvas:
        Color:
            rgba: (1,1,1,1)
        Ellipse:
            source: 'icons/attendance.png'
            pos: self.pos
            size: self.size
""")

class CDatePicker(DatePicker):
    def changeDate(self):
        usersList.date = self.text

class LeaveDetails(Button, MouseOver):
    def on_release(self, *args):
        pop = Popup(title= 'Leave Details', content= leaveDet.LeaveDetLayout(), size_hint= (0.98, 0.98))
        pop.open()
        return True

    def collide_point(self, x, y):
          return Vector(x, y).distance(self.center) <= self.width / 2

    def on_hover(self):
        self.background_color = (1, 0.5, 0.5, 0.5)

    def on_exit(self):
        self.background_color = (0, 0, 0, 0)

class ExcelImport(Button, MouseOver):
    def on_hover(self):
        self.background_color = (1, 0, 1, 0.5)

    def on_exit(self):
        self.background_color = (0, 0, 0, 0)

    def excelOpen(self):

        popupLayout = BoxLayout(orientation='vertical')
        buttonLayout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

        from pathlib import Path
        home = str(Path.home())
        file = FileChooserListView(path=home)
        popupLayout.add_widget(file)
        popupLayout.add_widget(buttonLayout)

        def callback(instance):
            if(instance.text == 'OPEN'):
                self.filePopup.dismiss()
                #excelIO.excelManip(file.selection)
                excelIO.threads(file.selection)

        openBtn = Button(text='OPEN')
        openBtn.bind(on_press=callback)
        buttonLayout.add_widget(openBtn)

        closeBtn = Button(text='Cancel')
        buttonLayout.add_widget(closeBtn)

        self.filePopup = Popup(title='Choose Excel', content=popupLayout, size_hint=(0.75, 0.75 ))
        closeBtn.bind(on_press=self.filePopup.dismiss)
        self.filePopup.open()

class ExcelExport(Spinner, MouseOver):
    def callexcel(self, text, date):
        if text == 'DAY':
            excelIO.excelExport(date)
            #try:
            #    excelIO.excelExport(date)
            #except Exception as e:
            #    from pages import kivytoast
            #    kivytoast.toast(str(e), (1, 0, 0, 0.5), length_long=True)
        if text == 'MONTH':
            try:
                excelIO.exportMonth(date.split(".")[1].zfill(2), date.split(".")[2].zfill(2))
            except:
                from pages import kivytoast
                kivytoast.toast('Please Select Date / Error', (1, 0, 0, 0.5), length_long=True)

    def on_hover(self):
        self.background_color = (1, 0, 1, 0.5)

    def on_exit(self):
        self.background_color = (0, 0, 0, 0)

class ExcelExported(Popup):
    pass

class SetButton(Button, MouseOver):
    def on_release(self, *args):
        settings.Settings()

    def collide_point(self, x, y):
          return Vector(x, y).distance(self.center) <= self.width / 2

    def on_hover(self):
        self.ids.setImg.anim_delay = 0.1

    def on_exit(self):
        self.ids.setImg.anim_delay = -1

class AdminPage(Screen):
    def __init__(self, **args):
        super(AdminPage, self).__init__(**args)
        self.user()

    def user(self):
        userList = usersList.UserList()
        userList.size_hint = (1, 1)
        self.ids.listLayout.add_widget(userList)
        self.ids.listLayout.add_widget(SetButton())
        self.ids.listLayout.add_widget(LeaveDetails())
