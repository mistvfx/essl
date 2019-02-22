from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.splitter import Splitter
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
import threading
from kivy.clock import Clock
from kivy.properties import *
from kivy.app import App
from kivy.lang import Builder

from db import userSettings, getInfo

io = ['I/O']*1
time = ['TIME']*1
door = ['DOOR']*1
accType = ['ACCESS TYPE']*1

lvl = 0
id = 0
date = 0

Builder.load_string("""
<DataBox>:
    orientation: 'horizontal'
    spacing: 1
    DataLbl:
        id: ios
    DataLbl:
        id: time
    DataLbl:
        id: door
    DataLbl:
        id: acc_type

<DataLbl>:
    color: (0, 0, 0, 1)
    markup: True
    bold: True
    background_color: (1, 1, 1, 1)
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size

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

#<DataTable>:
#    data: root.details
#    viewclass: 'DataBox'
#    RecycleBoxLayout:
#        size_hint: (1,None)
#        height: self.minimum_height
#        spacing: 2
#        orientation: 'vertical'
#        canvas.before:
#            Color:
#                rgba: (0, 0, 0, 1)
#            Rectangle:
#                size: self.size
#                pos: self.pos

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

#class DataBox(BoxLayout):
class DataBox(RecycleDataViewBehavior, BoxLayout):
    index = None

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.ids.ios.text = data['io']['text']
        self.ids.time.text = data['time']['text']
        self.ids.door.text = data['door']['text']
        self.ids.acc_type.text = data['acc_type']['text']
        return super(DataBox, self).refresh_view_attrs(
            rv, index, data)


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
    details = ListProperty(None)
    def __init__(self, **args):
        super(DataTable, self).__init__(**args)
        self.level = { '1': ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'TRAINING-1', 'IT', 'HR', 'SERVER ROOM', 'STORE'],
                       '2': ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'TRAINING-1', 'HR'],
                       '3': ['MM', 'ROTO', 'PAINT', 'CONFERENCE ROOM', 'TRAINING-1'],
                       '4': ['MM', 'ROTO', 'CONFERENCE ROOM'],
                       '5': ['ROTO', 'CONFERENCE ROOM'],
                       '6': ['MM', 'CONFERENCE ROOM', 'TRAINING-1'],
                       '7': ['ROTO', 'CONFERENCE ROOM', 'TRAINING-1']}
        self.size_hint=(1, 1)
        getInfo.get_IO_info(id, date)
        self.tableUI()

    def tableUI(self):
        global io, time, door, lvl, accType

        layout = GridLayout(cols=3, spacing=2, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        i=0; j=0; k=0;
        while i < len(io):
            if door[i] not in self.level[lvl] and door[i] != 'MAINDOOR':
                i += 1; j += 1; k += 1;
                continue
            lbl = DataLbl(text=str(io[i]), size_hint_y=None, height=40)
            try:
                if door[i] in self.level[lvl] and io[i] in ['In', 'IN'] and door[i+1] == door[i] and io[i+1] in ['Out', 'OUT']:
                    lbl.set_bgGreen()
                elif door[i-1] in self.level[lvl] and io[i-1] in ['In', 'IN'] and door[i-1] == door[i] and io[i] in ['Out', 'OUT']:
                    lbl.set_bgGreen()
                elif door[i] in self.level[lvl]:
                    lbl.set_bgRed()
            except:
                pass
            layout.add_widget(lbl)
            while j < len(time):
                lbl = DataLbl(text=str(time[j]), size_hint_y=None, height=40)
                try:
                    if door[i] in self.level[lvl] and io[i] in ['In', 'IN'] and door[i+1] == door[i] and io[i+1] in ['Out', 'OUT']:
                        lbl.set_bgGreen()
                    elif door[i-1] in self.level[lvl] and io[i-1] in ['In', 'IN'] and door[i-1] == door[i] and io[i] in ['Out', 'OUT']:
                        lbl.set_bgGreen()
                    elif door[i] in self.level[lvl]:
                        lbl.set_bgRed()
                except:
                    pass
                layout.add_widget(lbl)
                while k < len(door):
                    lbl = DataLbl(text=str(door[k]), size_hint_y=None, height=40)
                    try:
                        if door[i] in self.level[lvl] and io[i] in ['In', 'IN'] and door[i+1] == door[i] and io[i+1] in ['Out', 'OUT']:
                            lbl.set_bgGreen()
                        elif door[i-1] in self.level[lvl] and io[i-1] in ['In', 'IN'] and door[i-1] == door[i] and io[i] in ['Out', 'OUT']:
                            lbl.set_bgGreen()
                        elif door[i] in self.level[lvl]:
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
        del io[:]; del time[:]; del door[:]; del accType[:]

class DataTableAdmin(ScrollView):
    def __init__(self, **args):
        super(DataTableAdmin, self).__init__(**args)
        self.as_popup="True"
        self.size_hint=(1, 1)
        #self.size=(Window.width, Window.height)
        self.tableUI()

    def tableUI(self):
        global io, time, door, accType
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

        i=0; j=0; k=0; l=0;
        while i < len(io):
            lbl = DataLbl(text=str(io[i]), size_hint_y=None, height=40)
            try:
                if door[i] in level[lvl] and io[i] in ['In', 'IN'] and door[i+1] == door[i] and io[i+1] in ['Out', 'OUT']:
                    lbl.set_bgGreen()
                elif door[i-1] in level[lvl] and io[i-1] in ['In', 'IN'] and door[i-1] == door[i] and io[i] in ['Out', 'OUT']:
                    lbl.set_bgGreen()
                elif door[i] in level[lvl]:
                    lbl.set_bgRed()
            except:
                pass
            layout.add_widget(lbl)
            while j < len(time):
                lbl = DataLbl(text=str(time[j]), size_hint_y=None, height=40)
                try:
                    if door[i] in level[lvl] and io[i] in ['In', 'IN'] and door[i+1] == door[i] and io[i+1] in ['Out', 'OUT']:
                        lbl.set_bgGreen()
                    elif door[i-1] in level[lvl] and io[i-1] in ['In', 'IN'] and door[i-1] == door[i] and io[i] in ['Out', 'OUT']:
                        lbl.set_bgGreen()
                    elif door[i] in level[lvl]:
                        lbl.set_bgRed()
                except:
                    pass
                layout.add_widget(lbl)
                while k < len(door):
                    lbl = DataLbl(text=str(door[k]), size_hint_y=None, height=40)
                    try:
                        if door[i] in level[lvl] and io[i] in ['In', 'IN'] and door[i+1] == door[i] and io[i+1] in ['Out', 'OUT']:
                            lbl.set_bgGreen()
                        elif door[i-1] in level[lvl] and io[i-1] in ['In', 'IN'] and door[i-1] == door[i] and io[i] in ['Out', 'OUT']:
                            lbl.set_bgGreen()
                        elif door[i] in level[lvl]:
                            lbl.set_bgRed()
                    except:
                        pass
                    layout.add_widget(lbl)
                    while l < len(accType):
                        lbl = DataLbl(text=str(accType[l]), size_hint_y=None, height=40)
                        try:
                            if door[i] in level[lvl] and io[i] in ['In', 'IN'] and door[i+1] == door[i] and io[i+1] in ['Out', 'OUT']:
                                lbl.set_bgGreen()
                            elif door[i-1] in level[lvl] and io[i-1] in ['In', 'IN'] and door[i-1] == door[i] and io[i] in ['Out', 'OUT']:
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
        del io[:]; del time[:]; del door[:]; del accType[:]
