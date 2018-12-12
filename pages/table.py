from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
#from kivy.app import runTouchApp
from kivy.app import App
from kivy.lang import Builder

io = ['I/O']*1
time = ['TIME']*1
door = ['DOOR']*1
accType = ['ACCESS TYPE']*1
lvl = 0

Builder.load_string("""
<dataLbl>:
    color: (0, 0, 0, 1)
    bold: True
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<dataLblM>:
    FloatLayout:
        pos: self.parent.pos
        size: self.parent.pos
        Button:
            text: '+/-'
            size_hint_x: 0.20
            pos_hint: {'y':0, 'right':1}
            canvas.before:
                Color:
                    rgba: (0, 0, 0, 0)
                Rectangle:
                    pos: self.pos
                    size: self.size

""")
class dataLbl(Label):
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

class dataLblM(dataLbl):
    pass

class dataTable(ScrollView):
    def __init__(self, **args):
        super(dataTable, self).__init__(**args)
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
                '5': ['ROTO', 'CONFERENCE ROOM']}

        layout = GridLayout(cols=3, spacing=5, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        i=1; j=1; k=1;
        while i < len(io):
            if door[i] not in level[lvl]:
                i += 1; j += 1; k += 1;
                continue
            lbl = dataLbl(text=str(io[i]), size_hint_y=None, height=40)
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
                lbl = dataLbl(text=str(time[j]), size_hint_y=None, height=40)
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
                    lbl = dataLbl(text=str(door[k]), size_hint_y=None, height=40)
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
                '5': ['ROTO', 'CONFERENCE ROOM']}
        #print(io)
        layout = GridLayout(cols=4, spacing=5, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))

        i=1; j=1; k=1; l=1;
        while i < len(io):
            lbl = dataLbl(text=str(io[i]), size_hint_y=None, height=40)
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
                lbl = dataLbl(text=str(time[j]), size_hint_y=None, height=40)
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
                    lbl = dataLbl(text=str(door[k]), size_hint_y=None, height=40)
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
                        lbl = dataLblM(text=str(accType[l]), size_hint_y=None, height=40)
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
                        l+=1
                        break
                    k+=1
                    break
                j+=1
                break
            i+=1
        self.add_widget(layout)
        del io[:]; del time[:]; del door[:];
