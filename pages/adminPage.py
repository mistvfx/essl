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
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.spinner import Spinner
from kivy.lang import Builder

from . import excelIO
import threading
from pages import usersList, settings
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
<excelImpButton>:
    text: "Excel Import"
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
            text: "Excel Import"
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

<refButton>:
    text: 'REFRESH'
    color: (1, 1, 1, 0)
    background_color: (0, 0, 0, 0)
    pos_hint: {'right':1, 'bottom':1}
    size_hint: (0.1, 0.1)
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
    Image:
        id: refImg
        source: 'icons/refresh.zip'
        size: self.parent.size
        y: self.parent.y
        x: self.parent.x
        anim_delay: -1
        anim_loop: 1

<setButton>:
    text: 'SETTINGS'
    color: (1, 1, 1, 0)
    background_color: (0, 0, 0, 0)
    pos_hint: {'left':1, 'bottom':1}
    size_hint: (0.1, 0.1)
    Image:
        id: setImg
        source: 'icons/settings.zip'
        size: self.parent.size
        y: self.parent.y
        x: self.parent.x
        anim_delay: -1
        anim_loop: 1
""")
class excelImpButton(Button, MouseOver):
    def on_hover(self):
        self.background_color = (1, 0, 1, 0.5)

    def on_exit(self):
        self.background_color = (0, 0, 0, 0)

class ExcelExport(Spinner, MouseOver):
    def on_hover(self):
        self.background_color = (1, 0, 1, 0.5)

    def on_exit(self):
        self.background_color = (0, 0, 0, 0)

class ExcelExported(Popup):
    pass

class refButton(Button, MouseOver):
    def on_hover(self):
        self.background_color = (1, 1, 1, 0.5)

    def on_exit(self):
        self.background_color = (0, 0, 0, 0)

    def on_press(self):
        self.ids.refImg.anim_delay = 0.01

    def on_release(self):
        self.ids.refImg.anim_delay = -1

class setButton(Button, MouseOver):
    def on_hover(self):
        self.ids.setImg.anim_delay = 0.1

    def on_exit(self):
        self.ids.setImg.anim_delay = -1

class AdminPage(Screen):
    def __init__(self, **args):
        super(AdminPage, self).__init__(**args)
        self.user()

    def user(self):

        def callback(instance):
            if(instance.text == 'Excel Import'):
                self.excelOpen()
            """if(instance.text == 'Excel Export'):
                excelIO.excelExport(date.text)
                ExcelExported().open()"""
            if(instance.text == 'REFRESH'):
                usersList.date.append(date.text)
            if(instance.text == 'SETTINGS'):
                settings.Settings()

        def callexcel(spinner, text):
            if text == 'DAY':
                excelIO.excelExport(date.text)
            if text == 'MONTH':
                excelIO.exportMonth(date.text.split(".")[1], date.text.split(".")[2])


        adminLayout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        self.add_widget(adminLayout)

        controlLayout = BoxLayout(orientation='horizontal', size_hint=(1, 0.06),
                                    spacing=5)
        listLayout = FloatLayout(size_hint=(1, 1))
        adminLayout.add_widget(controlLayout)
        adminLayout.add_widget(listLayout)

        excelImportBtn = excelImpButton()
        excelImportBtn.bind(on_release=callback)
        controlLayout.add_widget(excelImportBtn)

        date = DatePicker(size_hint=(0.5, 1), pHint=(0.35, 0.35))
        controlLayout.add_widget(date)

        excelExport = ExcelExport()
        excelExport.bind(text=callexcel)
        controlLayout.add_widget(excelExport)

        refreshBtn = refButton()
        refreshBtn.bind(on_release=callback)

        settingsBtn = setButton()
        settingsBtn.bind(on_release=callback)

        usersListManip.getUserInfo()
        usersList.date.append(date.text)
        userList = usersList.userList()
        userList.size_hint = (1, 1)
        listLayout.add_widget(userList)
        listLayout.add_widget(refreshBtn)
        listLayout.add_widget(settingsBtn)

    def excelOpen(self):

        popupLayout = BoxLayout(orientation='vertical')
        buttonLayout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

        file = FileChooserListView(path='/home/')
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
