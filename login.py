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
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.uix.behaviors.touchripple import TouchRippleBehavior
from kivy.lang import Builder
from kivy.graphics.texture import Texture
from kivy import utils
from kivy.vector import Vector
import tempfile
from kivy.config import Config

from db.credentialsCheck import checkCredentials
from pages import adminPage
from pages.specialFeatures import *

Window.maximize()
Config.set('input', 'mouse', 'mouse,disable_multitouch')

Builder.load_string("""
<LoginScrnBg>:
    canvas:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: (49/255, 27/255, 146/255, 1)
        Rectangle:
            size: self.size[0], self.size[1]
            pos: self.pos[0], self.pos[1]
        Color:
            rgba: (230/255, 81/255, 0/255, 1)
        Rectangle:
            size: self.size[0]*0.5, self.size[1]
            pos: self.pos[0], self.pos[1]

<LoginScrn>:
    padding: 10
    orientation: 'horizontal'
    size_hint: 1, 0.75
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            size: self.size[0], self.size[1]
            pos: self.pos[0], self.pos[1]
    Image:
        size_hint_x: 0.75
        source: 'icons/logo.png'

<LoginBG>:
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

<Lbl>:
    font_name: 'fonts/GoogleSans-Bold.ttf'
    size_hint_x: 0.20
    size_hint_y: None
    text_size: self.width, None
    size: self.texture_size
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
            size: self.texture_size

<In>:
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
            rgba: (0.5, 0, 1, 0.85)
        Line:
            width: 2
            rectangle: (self.x, self.y, self.width, self.height)

<MaterialTextBox>:
    size_hint_y: 1

<LoginButton>:
    id: loginBtn
    text: 'LOGIN'
    color: (0, 0, 0, 1)
    size_hint: (0.75, 0.75)
    font_name: 'fonts/moon-bold.otf'
    font_size: 20
    background_color: (0, 0, 0, 0)
    canvas.before:
        Color:
            rgba: (0, 0, 0, 1)
        Line:
            rectangle: (self.pos[0], self.pos[1], self.size[0], self.size[1])

<LogoutButton>:
    color: (0, 0, 0, 0)
    background_color: (0, 0, 0, 0)
    size: (min(self.width, self.height), min(self.width, self.height))
    canvas:
        Color:
            rgba: ((0.5,0.5,1,0.85) if self.state == "normal" else (0.5,0.5,0.5,1))
        Rectangle:
            source: 'icons/logout.png'
            pos: self.pos
            size: self.size

<LoginWindow>:
    LoginScrnBg:
        anchor_x: 'center'
        anchor_y: 'center'
        LoginScrn:
            AnchorLayout:
                anchor_x: 'center'
                anchor_y: 'center'
                size_hint_x: 0.35
                LoginBG:
                    Label:
                        text:'ARTIST LOGIN'
                        bold:True
                        color:(0, 0, 0, 1)
                        font_size:25
                        font_name:'fonts/moon-bold.otf'
                    MaterialTextBox:
                        In:
                            id: username
                            hint_text: 'USERNAME'
                        Lbl:
                            text: 'UserName'
                    MaterialTextBox:
                        In:
                            id: password
                            hint_text: 'PASSWORD'
                            password: True
                        Lbl:
                            text: 'Password'
                    BoxLayout:
                        orientation:'horizontal'
                        CheckBox:
                            size_hint_x:0.25
                            color:(0, 0, 0, 1)
                            on_active: root.cbActive
                        Label:
                            text:'REMEMBER ME'
                            font_name: 'fonts/GoogleSans-Medium.ttf'
                            color:(0, 0, 0, 1)
                    FloatLayout:
                        LoginButton:
                            pos_hint: {'center_x':0.5, 'center_y':0.5}
                            on_release: root.checkLogin()

""")
class Lbl(Label):
    pass

class LogoutButton(Button):
    pass

class LoginScrnBg(AnchorLayout):
    pass

class LoginButton(Button, MouseOver):
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

class MaterialTextBox(FloatLayout):
    pass

class In(TextInput):
    text_width = NumericProperty()

    def update_padding(self, *args):
        self.text_width = self._get_text_width(
            self.text,
            self.tab_width,
            self._label_cached
        )

class LoginBG(BoxLayout):
    pass

class LoginScrn(BoxLayout):
    pass

class LoginWindow(Screen):
    def __init__(self, **args):
        super(LoginWindow, self).__init__(**args)
        self.login()

    def login(self):
        try:
            with open("%s/mttup.txt"%(tempfile.gettempdir()), "r") as f:
                res = str(f.read(4))
                self.ids.username.text = res
                self.ids.password.text = res
                #self.checkLogin()
        except Exception as e:
            print(e)
            pass

    def callback(instance):
        if(instance.text == 'LOGOUT'):
            ScreenManagement.sm.current = ScreenManagement.sm.previous()
            #ScreenManagement.sm.remove_widget(userPage.UserPage())
            ScreenManagement.sm.current = 'login'

    def cbActive(cb, value):
        if value:
            with open("%s/mttup.txt"%(tempfile.gettempdir()), "w") as f:
                f.write(self.ids.password.text)
        else:
            with open("%s/mttup.txt"%(tempfile.gettempdir()), "w") as f:
                f.write("")

    def checkLogin(self):
        login = checkCredentials(self.ids.username.text, self.ids.password.text)

        if login == 1:
            ScreenManagement.sm.add_widget(adminPage.AdminPage(name='admin'))
            ScreenManagement.sm.current = 'admin'
        elif login[0] == 2:
            from pages import userPage
            ScreenManagement.sm.add_widget(userPage.UserPage(name='user'))
            ScreenManagement.sm.current = 'user'
        else:
            print("Wrong Login")

class ScreenManagement(ScreenManager):
    sm = ScreenManager()
    sm.add_widget(LoginWindow(name='login'))

class mistApp(App):
    def build(self):
        self.title = 'MIST TIME TRACKER'
        return ScreenManagement().sm

if __name__ == '__main__':
    mistApp().run()
