from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.splitter import Splitter
#from kivy.app import runTouchApp
from kivy.app import App
from kivy.lang import Builder

from db import userSettings

io = ['I/O']*1
time = ['TIME']*1
door = ['DOOR']*1
accType = ['ACCESS TYPE']*1
lvl = 0
id = 0
date = 0

Builder.load_string("""
<DataLbl>:
    color: (0, 0, 0, 1)
    bold: True
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<DataLblM>:
    FloatLayout:
        pos: self.parent.pos
        size: self.parent.size
        Button:
            text: '+/-'
            bold: True
            size_hint: (0.20, 0.6)
            pos_hint: {'y':0, 'right':1}
            on_release: root.openRegPop()
            canvas.before:
                Color:
                    rgba: (0, 0, 0, 0)
                Rectangle:
                    pos: self.pos
                    size: self.size

""")
class DataLbl(Label):
    def set_bgRed(self):
        with self.canvas.before:
            Color(1, 0, 0, 0.50)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def set_bgGreen(self):
        with self.canvas.before:
            Color(0, 1, 0, 0.50)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class DataLblM(DataLbl):
    def getInfo(self, data):
        self.data = data

    def openRegPop(self):
        global id, date
        TF = userSettings.TimingFix(id, date)
        RT = userSettings.RemTime(id, date, self.data[0], self.data[1], self.data[2], self.data[3])
        setLayout = BoxLayout(orientation = 'horizontal')
        REG = Splitter(sizable_from = 'right', rescale_with_parent = True, keep_within_parent = True)
        REG.add_widget(TF)
        setLayout.add_widget(REG)
        setLayout.add_widget(RT)
        #REG.add_widget(setLayout)
        popup = Popup(title="TIMING FIX", content=setLayout, size_hint=(0.65, 0.65))
        popup.open()

class DataTable(ScrollView):
    def __init__(self, **args):
        super(DataTable, self).__init__(**args)
        self.as_popup="True"
        self.size_hint=(1, 1)
        #self.size=(Window.width, Window.height)
        self.tableUI()

    def tableUI(self):
        global io, time, door, lvl
        level = { '1': ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'TRAINING-1', 'IT', 'HR', 'SERVER ROOM', 'STORE'],
                '2': ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'TRAINING-1', 'HR'],
                '3': ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'TRAINING-1'],
                '4': ['MM', 'ROTO', 'CONFERENCE ROOM'],
                '5': ['ROTO', 'CONFERENCE ROOM'],
                '6': ['MM', 'CONFERENCE ROOM', 'TRAINING-1'],
                '7': ['ROTO', 'CONFERENCE ROOM', 'TRAINING-1']}

        layout = GridLayout(cols=3, spacing=5, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        i=1; j=1; k=1;
        while i < len(io):
            if door[i] not in level[lvl] and door[i] != 'MAINDOOR':
                i += 1; j += 1; k += 1;
                continue
            lbl = DataLbl(text=str(io[i]), size_hint_y=None, height=40)
            try:
                if door[i] in level[lvl] and io[i] == 'In' and door[i+1] == door[i] and io[i+1] == 'Out':
                    lbl.set_bgGreen()
                elif door[i-1] in level[lvl] and io[i-1] == 'In' and door[i-1] == door[i] and io[i] == 'Out':
                    lbl.set_bgGreen()
                elif door[i] in level[lvl]:
                    lbl.set_bgRed()
            except:
                pass
            layout.add_widget(lbl)
            while j < len(time):
                lbl = DataLbl(text=str(time[j]), size_hint_y=None, height=40)
                try:
                    if door[i] in level[lvl] and io[i] == 'In' and door[i+1] == door[i] and io[i+1] == 'Out':
                        lbl.set_bgGreen()
                    elif door[i-1] in level[lvl] and io[i-1] == 'In' and door[i-1] == door[i] and io[i] == 'Out':
                        lbl.set_bgGreen()
                    elif door[i] in level[lvl]:
                        lbl.set_bgRed()
                except:
                    pass
                layout.add_widget(lbl)
                while k < len(door):
                    lbl = DataLbl(text=str(door[k]), size_hint_y=None, height=40)
                    try:
                        if door[i] in level[lvl] and io[i] == 'In' and door[i+1] == door[i] and io[i+1] == 'Out':
                            lbl.set_bgGreen()
                        elif door[i-1] in level[lvl] and io[i-1] == 'In' and door[i-1] == door[i] and io[i] == 'Out':
                            lbl.set_bgGreen()
                        elif door[i] in level[lvl]:
                            lbl.set_bgRed()
                    except:
                        pass
                    layout.add_widget(lbl)
                    k+=1
                    break
                j+=1
                break
            i+=1
        self.add_widget(layout)
        del io[:]; del time[:]; del door[:];

class dataTableAdmin(ScrollView):
    def __init__(self, **args):
        super(dataTableAdmin, self).__init__(**args)
        self.as_popup="True"
        self.size_hint=(1, 1)
        #self.size=(Window.width, Window.height)
        self.tableUI()

    def tableUI(self):
        global io, time, door
        level = { '1': ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'TRAINING-1', 'IT', 'HR', 'SERVER ROOM', 'STORE'],
                '2': ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'TRAINING-1', 'HR'],
                '3': ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'TRAINING-1'],
                '4': ['MM', 'ROTO', 'CONFERENCE ROOM'],
                '5': ['ROTO', 'CONFERENCE ROOM'],
                '6': ['MM', 'CONFERENCE ROOM', 'TRAINING-1'],
                '7': ['ROTO', 'CONFERENCE ROOM', 'TRAINING-1']}
        #print(io)
        layout = GridLayout(cols=4, spacing=5, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))

        i=1; j=1; k=1; l=1;
        while i < len(io):
            lbl = DataLbl(text=str(io[i]), size_hint_y=None, height=40)
            try:
                if door[i] in level[lvl] and io[i] == 'In' and door[i+1] == door[i] and io[i+1] == 'Out':
                    lbl.set_bgGreen()
                elif door[i-1] in level[lvl] and io[i-1] == 'In' and door[i-1] == door[i] and io[i] == 'Out':
                    lbl.set_bgGreen()
                elif door[i] in level[lvl]:
                    lbl.set_bgRed()
            except:
                pass
            layout.add_widget(lbl)
            while j < len(time):
                lbl = DataLbl(text=str(time[j]), size_hint_y=None, height=40)
                try:
                    if door[i] in level[lvl] and io[i] == 'In' and door[i+1] == door[i] and io[i+1] == 'Out':
                        lbl.set_bgGreen()
                    elif door[i-1] in level[lvl] and io[i-1] == 'In' and door[i-1] == door[i] and io[i] == 'Out':
                        lbl.set_bgGreen()
                    elif door[i] in level[lvl]:
                        lbl.set_bgRed()
                except:
                    pass
                layout.add_widget(lbl)
                while k < len(door):
                    lbl = DataLbl(text=str(door[k]), size_hint_y=None, height=40)
                    try:
                        if door[i] in level[lvl] and io[i] == 'In' and door[i+1] == door[i] and io[i+1] == 'Out':
                            lbl.set_bgGreen()
                        elif door[i-1] in level[lvl] and io[i-1] == 'In' and door[i-1] == door[i] and io[i] == 'Out':
                            lbl.set_bgGreen()
                        elif door[i] in level[lvl]:
                            lbl.set_bgRed()
                    except:
                        pass
                    layout.add_widget(lbl)
                    while l < len(accType):
                        lbl = DataLbl(text=str(accType[l]), size_hint_y=None, height=40)
                        try:
                            if door[i] in level[lvl] and io[i] == 'In' and door[i+1] == door[i] and io[i+1] == 'Out':
                                lbl.set_bgGreen()
                            elif door[i-1] in level[lvl] and io[i-1] == 'In' and door[i-1] == door[i] and io[i] == 'Out':
                                lbl.set_bgGreen()
                            elif door[i] in level[lvl]:
                                lbl = DataLblM(text=str(accType[l]), size_hint_y=None, height=40)
                                lbl.getInfo([io[i], time[i], door[i], accType[i]])
                                lbl.set_bgRed()
                        except:
                            pass
                        layout.add_widget(lbl)
                        l+=1
                        break
                    k+=1
                    break
                j+=1
                break
            i+=1
        self.add_widget(layout)
        del io[:]; del time[:]; del door[:];
