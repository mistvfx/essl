from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.label import Label
#from kivy.app import runTouchApp
from kivy.app import App
from kivy.lang import Builder

io = ['I/O']*1
time = ['TIME']*1
door = ['DOOR']*1

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
""")

class dataLbl(Label):
    pass

class dataTable(ScrollView):
    def __init__(self, **args):
        super(dataTable, self).__init__(**args)
        self.as_popup="True"
        self.size_hint=(1, 1)
        #self.size=(Window.width, Window.height)
        self.tableUI()

    def tableUI(self):
        global io, time, door
        #print(time)
        layout = GridLayout(cols=3, spacing=5, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))

        i=1; j=1; k=1;
        while i < len(io):
            lbl = dataLbl(text=str(io[i]), size_hint_y=None, height=40)
            layout.add_widget(lbl)
            while j < len(time):
                lbl = dataLbl(text=str(time[j]), size_hint_y=None, height=40)
                layout.add_widget(lbl)
                while k < len(door):
                    lbl = dataLbl(text=str(door[k]), size_hint_y=None, height=40)
                    layout.add_widget(lbl)
                    k+=1
                    break
                j+=1
                break
            i+=1
        self.add_widget(layout)
        del io[:]; del time[:]; del door[:];
