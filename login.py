import kivy
from kivy.app import App
kivy.require('1.10.1')
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.core.image import Image
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from kivy.lang import Builder
from kivy import utils

from db.credentialsCheck import checkCredentials
from pages import userPage, adminPage

Builder.load_string("""
<loginScrnBg>:
    Image:
        source: 'icons/bg.jpg'
        allow_stretch: True

<loginButton@Button>:
    text: 'LOGIN'
    color: (1, 1, 1, 0)
    background_color: (0, 0, 0, 0)
    Image:
        source: 'icons/login.png'
        size: self.parent.size
        y: self.parent.y
        x: self.parent.x

<TextBox@TextInput>:
    multiline: False
    write_tab: False
    background_color: (1, 1, 1, 1) if self.focus else (1, 1, 1, 0.5)

<loginBG>:
    size_hint: 1, 0.35
    orientation: 'vertical'
    canvas.before:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            size: self.size
            pos: self.pos

    padding: 10
    spacing: 2


<loginScrn>:
    padding: 10
    orientation: 'horizontal'
    size_hint: 0.65, 0.75
    canvas.before:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            size: self.size
            pos: self.pos
    Image:
        size_hint_x: 0.75
        source: 'icons/logo.png'
""")

class loginScrnBg(AnchorLayout):
    pass

class loginButton(Button):
    pass

class TextBox(TextInput):
    pass

class loginBG(BoxLayout):
    pass

class loginScrn(BoxLayout):
    pass

class loginWindow(Screen):
    def __init__(self, **args):
        super(loginWindow, self).__init__(**args)
        #with self.canvas.before:
        #    Rectangle(source='icons/mist_logo.jpg', pos=self.pos, size=Window.size)
        self.login()

    def login(self):
        anchorLayout = loginScrnBg(anchor_x='center', anchor_y='center')
        #with anchorLayout.canvas.before:
        #    Rectangle(source = 'icons/bg.jpg', size = Window.size, pos = self.pos)
        self.add_widget(anchorLayout)

        loginSetup = loginScrn()
        anchorLayout.add_widget(loginSetup)

        #layout = loginBG(orientation='vertical', padding=10, spacing = 2, size_hint=(0.3, 0.3))
        loginAnchor = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.35)
        loginSetup.add_widget(loginAnchor)

        layout = loginBG()
        loginAnchor.add_widget(layout)

        loginLabel = Label(text='LOGIN', bold=True, color=(0, 0, 0, 1))
        #self.username = TextInput(text='USERNAME', multiline=False, padding=5)
        self.username = TextBox(hint_text='USERNAME')
        self.password = TextBox(hint_text='PASSWORD', password=True)

        def callback(instance):
            if(instance.text == 'LOGIN'):
                self.checkLogin()
            if(instance.text == 'LOGOUT'):
                ScreenManagement.sm.remove_widget(userPage.UserPage())
                ScreenManagement.sm.current = 'login'

        #loginButton = Button(text='LOGIN')
        loginBtn = loginButton()
        loginBtn.bind(on_release=callback)

        logoutButton = Button(text='LOGOUT', size_hint=(0.1, 0.1), pos_hint={'right':1, 'top':1})
        logoutButton.bind(on_press=callback)
        userPage.logoutButton = logoutButton

        layout.add_widget(loginLabel)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(loginBtn)

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

class mistApp(App):
    def build(self):
        self.title = 'MIST ARTIST TIME TRACKER'
        return ScreenManagement().sm

if __name__ == '__main__':
    mistApp().run()
