import kivy
from kivy.app import App
kivy.require('1.10.1')
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from db.credentialsCheck import checkCredentials
from pages import userPage, adminPage

class loginWindow(Screen):
    def __init__(self, **args):
        super(loginWindow, self).__init__(**args)
        self.login()

    def login(self):
        anchorLayout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.add_widget(anchorLayout)

        layout = BoxLayout(orientation='vertical', padding=10,
                            spacing = 10, size_hint=(0.3, 0.3))
        anchorLayout.add_widget(layout)

        loginLabel = Label(text='LOGIN')
        self.username = TextInput(text='USERNAME', multiline=False,
                                    padding=5)
        self.password = TextInput(text='PASSWORD', multiline=False, password=True)

        def callback(instance):
            if(instance.text == 'LOGIN'):
                self.checkLogin()
            if(instance.text == 'LOGOUT'):
                ScreenManagement.sm.remove_widget(userPage.UserPage())
                ScreenManagement.sm.current = 'login'

        loginButton = Button(text='LOGIN')
        loginButton.bind(on_press=callback)

        logoutButton = Button(text='LOGOUT', size_hint=(0.1, 0.1), pos_hint={'right':1, 'top':1})
        logoutButton.bind(on_press=callback)
        userPage.logoutButton = logoutButton

        layout.add_widget(loginLabel)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(loginButton)

    def checkLogin(self):
        login = checkCredentials(self.username.text, self.password.text)

        if login == 1:
            ScreenManagement.sm.add_widget(adminPage.AdminPage(name='admin'))
            ScreenManagement.sm.current = 'admin'
        elif login == 2:
            ScreenManagement.sm.add_widget(userPage.UserPage(name='user'))
            ScreenManagement.sm.current = 'user'
        else:
            print("Wrong Login")

class ScreenManagement(ScreenManager):
    sm = ScreenManager()
    sm.add_widget(loginWindow(name='login'))
    #sm.add_widget(userPage.UserPage(name='user'))
    #sm.add_widget(adminPage.AdminPage(name='admin'))

class esslApp(App):
    def build(self):
        return ScreenManagement().sm

if __name__ == '__main__':
    esslApp().run()
