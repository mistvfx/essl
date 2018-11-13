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
from db import usersListManip

Builder.load_string("""
<excelImpButton>:
    text: "Excel Import"
    font_name: 'fonts/moon-bold.otf'
    size_hint: (0.5, 1)
    color: (1, 1, 1, 1)
    background_color: (0, 0, 0, 0)

<ExcelExport>:
    text: "Excel Export"
    values: ('DAY', 'MONTH')
    font_name: 'fonts/moon-bold.otf'
    size_hint: (0.5, 1)
    color: (1, 1, 1, 1)
    background_color: (0, 0, 0, 0)

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
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [70, 70, 50, 50]
    Image:
        source: 'icons/refresh.png'
        size: self.parent.size
        y: self.parent.y
        x: self.parent.x

<setButton>:
    text: 'SETTINGS'
    color: (1, 1, 1, 0)
    background_color: (0, 0, 0, 0)
    pos_hint: {'left':1, 'bottom':1}
    size_hint: (0.1, 0.1)
    Image:
        source: 'icons/setting.png'
        size: self.parent.size
        y: self.parent.y
        x: self.parent.x
""")
class excelImpButton(Button):
    pass

class ExcelExport(Spinner):
    pass

class ExcelExported(Popup):
    pass

class refButton(Button):
    pass

class setButton(Button):
    pass

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
        excelImportBtn.bind(on_press=callback)
        controlLayout.add_widget(excelImportBtn)

        date = DatePicker(size_hint=(0.5, 1), pHint=(0.35, 0.35))
        controlLayout.add_widget(date)

        excelExport = ExcelExport()
        excelExport.bind(text=callexcel)
        controlLayout.add_widget(excelExport)

        refreshBtn = refButton()
        refreshBtn.bind(on_press=callback)

        settingsBtn = setButton()
        settingsBtn.bind(on_press=callback)

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
