import kivy
from kivy.app import App
kivy.require('1.10.1')
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.animation import *
from kivy.core.image import Image
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from kivy.lang import Builder
from kivy.graphics.texture import Texture
from kivy import utils
from kivy.vector import Vector
import tempfile
from kivy.config import Config

from db.credentialsCheck import checkCredentials
from pages import userPage, adminPage
from pages.specialFeatures import *

Window.maximize()
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

Builder.load_string("""
<loginScrnBg>:
    canvas:
        Color:
            rgba: (0.5, 0.5, 1, 0.85)
        Rectangle:
            size: self.size
            pos: self.pos

<loginButton@Button>:
    id: loginBtn
    text: 'LOGIN'
    color: (0, 0, 0, 1)
    font_name: 'fonts/moon-bold.otf'
    font_size: 20
    background_color: (0, 0, 0, 0)
    canvas.before:
        Color:
            rgba: (0, 0, 0, 1)
        Line:
            rectangle: (self.pos[0], self.pos[1], self.size[0], self.size[1])

<userNameBox@TextInput>:
    multiline: False
    write_tab: False
    input_filter: 'int'
    font_name: 'fonts/moon.otf'
    font_size: self.size[1]/3.0
    padding: [self.size[1], self.size[1]/3.5, 10, 10]
    cursor_color: (0, 0, 0, 1)
    background_color: (0.9, 0.9, 0.9, 1) if self.focus else (1, 1, 1, 0.5)
    canvas.after:
        Rectangle:
            source: 'icons/username.png'
            size: (self.size[1], self.size[1])
            pos: self.pos

<passwordBox@TextInput>:
    multiline: False
    write_tab: False
    font_name: 'fonts/moon.otf'
    font_size: self.size[1]/3.0
    padding: [self.size[1], self.size[1]/3.5, 10, 10]
    background_color: (0.9, 0.9, 0.9, 1) if self.focus else (1, 1, 1, 0.5)
    canvas.after:
        Rectangle:
            source: 'icons/password.png'
            size: (self.size[1], self.size[1])
            pos: self.pos

<loginBG>:
    size_hint: 1, 0.50
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
            hsv: 0, 0, 1
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [0, 50, 0, 50]
    Image:
        size_hint_x: 0.75
        source: 'icons/logo.png'

<LogoutButton>:
    color: (0, 0, 0, 0)
    background_color: (0, 0, 0, 0)
    size: (min(self.width, self.height), min(self.width, self.height))
    canvas:
        Color:
            rgba: ((0.5,0.5,0.5,0.5) if self.state == "normal" else (0.5,0.5,0.5,1))
        Rectangle:
            source: 'icons/logout.png'
            pos: self.pos
            size: self.size
""")
class LogoutButton(Button):
    pass
    #def collide_point(self, x, y):
    #    return Vector(x, y).distance(self.center) <= self.width / 2

class loginScrnBg(AnchorLayout):
    pass

class loginButton(Button, MouseOver):
    def on_hover(self):
        self.color = (1, 1, 1, 1)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(size=(self.size), pos=(self.pos))

    def on_exit(self):
        self.color = (0, 0, 0, 1)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(size=(self.size), pos=(self.pos))
            Color(0, 0, 0, 1)
            Line(rectangle=(self.pos[0], self.pos[1], self.size[0], self.size[1]))

class userNameBox(TextInput):
    pass

class passwordBox(TextInput):
    pass

class loginBG(BoxLayout):
    pass

class loginScrn(BoxLayout):
    pass

class loginWindow(Screen):
    def __init__(self, **args):
        super(loginWindow, self).__init__(**args)
        self.login()

    def login(self):
        self.username = userNameBox(hint_text='USERNAME')
        self.password = passwordBox(hint_text='PASSWORD', password=True)
        try:
            with open("%s/mttup.txt"%(tempfile.gettempdir()), "r") as f:
                res = str(f.read(4))
                self.username.text = res
                self.password.text = res
                self.checkLogin()
        except Exception as e:
            print(e)
            pass

        anchorLayout = loginScrnBg(anchor_x='center', anchor_y='center')
        self.add_widget(anchorLayout)

        loginSetup = loginScrn()
        anchorLayout.add_widget(loginSetup)

        #layout = loginBG(orientation='vertical', padding=10, spacing = 2, size_hint=(0.3, 0.3))
        loginAnchor = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_x=0.35)
        loginSetup.add_widget(loginAnchor)

        layout = loginBG()
        loginAnchor.add_widget(layout)

        loginLabel = Label(text='ARTIST LOGIN', bold=True, color=(0, 0, 0, 1), font_size=25, font_name='fonts/moon-bold.otf')
        #self.username = TextInput(text='USERNAME', multiline=False, padding=5)
        #self.username = userNameBox(hint_text='USERNAME')
        #self.password = passwordBox(hint_text='PASSWORD', password=True)

        def callback(instance):
            if(instance.text == 'LOGIN'):
                self.checkLogin()
            if(instance.text == 'LOGOUT'):
                ScreenManagement.sm.current = ScreenManagement.sm.previous()
                #ScreenManagement.sm.remove_widget(userPage.UserPage())
                ScreenManagement.sm.current = 'login'

        def cbActive(cb, value):
            if value:
                with open("%s/mttup.txt"%(tempfile.gettempdir()), "w") as f:
                    f.write(self.password.text)
            else:
                with open("%s/mttup.txt"%(tempfile.gettempdir()), "w") as f:
                    f.write("")

        #loginButton = Button(text='LOGIN')
        loginBtn = loginButton()
        loginBtn.bind(on_release=callback)

        logoutButton = LogoutButton(text='LOGOUT', size_hint=(0.08, 0.08), pos_hint={'left':1, 'top':1})
        logoutButton.bind(on_release=callback)
        userPage.logoutButton = logoutButton

        remLayout = BoxLayout(orientation='horizontal')

        remME = CheckBox(size_hint_x=0.25, color=(0, 0, 0, 1))
        remME.bind(active=cbActive)

        remLbl = Label(text='REMEMBER ME', color=(0, 0, 0, 1))

        remLayout.add_widget(remME)
        remLayout.add_widget(remLbl)

        layout.add_widget(loginLabel)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(remLayout)
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
        self.title = 'MIST TIME TRACKER'
        return ScreenManagement().sm

if __name__ == '__main__':
    mistApp().run()
