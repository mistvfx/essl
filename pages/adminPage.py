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
from . import excelIO
import threading
from pages import usersList, settings
from db import usersListManip

class AdminPage(Screen):
    def __init__(self, **args):
        super(AdminPage, self).__init__(**args)
        self.user()

    def user(self):

        def callback(instance):
            if(instance.text == 'Excel Import'):
                self.excelOpen()
            if(instance.text == 'Excel Export'):
                excelIO.excelExport(date.text)
            if(instance.text == 'REFRESH'):
                #print(date.text)
                usersList.date.append(date.text)
            if(instance.text == 'SETTINGS'):
                settings.Settings()

        adminLayout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        self.add_widget(adminLayout)

        controlLayout = BoxLayout(orientation='horizontal', size_hint=(1, 0.06),
                                    spacing=5)
        listLayout = FloatLayout(size_hint=(1, 1))
        adminLayout.add_widget(controlLayout)
        adminLayout.add_widget(listLayout)

        excelImportBtn = Button(text="Excel Import", size_hint=(1, 1))
        excelImportBtn.bind(on_press=callback)
        controlLayout.add_widget(excelImportBtn)

        date = DatePicker(size_hint=(0.7, 1), pHint=(0.35, 0.35))
        controlLayout.add_widget(date)

        excelExportBtn = Button(text="Excel Export", size_hint=(1, 1))
        excelExportBtn.bind(on_press=callback)
        controlLayout.add_widget(excelExportBtn)

        refreshBtn = Button(text='REFRESH', pos_hint={'right':1, 'bottom':1}, size_hint=(0.1, 0.1))
        refreshBtn.bind(on_press=callback)

        settingsBtn = Button(text='SETTINGS', pos_hint={'left':1, 'bottom':1}, size_hint=(0.1, 0.1))
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
