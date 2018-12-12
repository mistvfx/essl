from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder
import datetime

from pages import table

closeBtn = Button()
TWH = [0]*1
AWH = [0]*1
NCH = [0]*1
ACH = [0]*1

Builder.load_string("""
<hdrLayout>:
    orientation: 'horizontal'
    size_hint: (1, 0.10)
    canvas.before:
        Color:
            rgba: (0, 0, 0, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<tblLayout>:
    orientation: 'horizontal'
    canvas.before:
        Color:
            rgba: (0, 0, 0, 1)
        Rectangle:
            size: self.size
            pos: self.pos

<infoLbl>:
    color: (0, 0, 0, 1)
    bold: True
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            size: self.size
            pos: self.pos
""")

class hdrLayout(BoxLayout):
    pass

class tblLayout(BoxLayout):
    pass

class infoLbl(Label):
    pass

def formatTime(time):
    seconds = time.total_seconds()
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)

    return ('{}:{}'.format(hours, minutes))

class infoTab(BoxLayout):
    def __init__(self, **args):
        super(infoTab, self).__init__(**args)
        self.popUI()

    def popUI(self):
        overallLayout = BoxLayout(orientation='vertical')
        self.add_widget(overallLayout)

        """ Defining Header and closeBtn """

        headerLayout = hdrLayout()
        overallLayout.add_widget(headerLayout)

        header = GridLayout(cols=3, size_hint=(0.65, 1))
        headerLayout.add_widget(header)
        headers = ['I/O', 'TIME', 'DOOR']
        for i in range(3):
            headerLabel = Label(text=headers[i], bold=True)
            header.add_widget(headerLabel)

        global closeBtn
        headerLayout.add_widget(closeBtn)

        """ Table and info """

        tableLayout = tblLayout()
        overallLayout.add_widget(tableLayout)

        tab = table.dataTable()
        tab.size_hint=(0.65, 1)
        tableLayout.add_widget(tab)

        """ Defining Info """

        info = GridLayout(cols=2, size_hint=(0.35, 1))
        tableLayout.add_widget(info)

        global TWH, AWH, NCH, ACH

        #tw = ("%.2f"%(round(TWH[len(TWH)-1].total_seconds()/3600, 2)))
        tw = formatTime(TWH[len(TWH)-1])

        #aw = ("%.2f"%(round(AWH[len(AWH)-1].total_seconds()/3600, 2)))
        aw = formatTime(AWH[len(AWH)-1])

        #nc = ("%.2f"%(round(NCH[len(NCH)-1].total_seconds()/3600, 2)))
        nc = formatTime(NCH[len(NCH)-1])

        #ac = ("%.2f"%(round(ACH[len(ACH)-1].total_seconds()/3600, 2)))
        ac = formatTime(ACH[len(ACH)-1])

        infoQ = ['Total Hours :', tw, 'Working Hours :', aw, 'Non-Completed Actual Hours:', nc, 'Additional Hours:', ac]

        for i in range(len(infoQ)):
            infoLabels = infoLbl(text=infoQ[i])
            if i % 2 == 1:
                infoLabels.size_hint_x= 0.30
            info.add_widget(infoLabels)

class infoTabAdmin(BoxLayout):
    def __init__(self, **args):
        super(infoTabAdmin, self).__init__(**args)
        self.popUI()

    def popUI(self):
        overallLayout = BoxLayout(orientation='vertical')
        self.add_widget(overallLayout)

        """ Defining Header and closeBtn """

        headerLayout = hdrLayout()
        overallLayout.add_widget(headerLayout)

        header = GridLayout(cols=4, size_hint=(0.55, 1))
        headerLayout.add_widget(header)
        headers = ['I/O', 'TIME', 'DOOR', 'Access Type']
        for i in range(4):
            headerLabel = Label(text=headers[i], bold=True)
            header.add_widget(headerLabel)

        global closeBtn
        headerLayout.add_widget(closeBtn)

        """ Table and info """

        tableLayout = tblLayout()
        overallLayout.add_widget(tableLayout)

        tab = table.dataTableAdmin()
        tab.size_hint=(0.55, 1)
        tableLayout.add_widget(tab)

        """ Defining Info """

        info = GridLayout(cols=2, size_hint=(0.45, 1))
        tableLayout.add_widget(info)

        global TWH, AWH, NCH, ACH

        #tw = ("%.2f"%(round(TWH[len(TWH)-1].total_seconds()/3600, 2)))
        tw = formatTime(TWH[len(TWH)-1])

        #aw = ("%.2f"%(round(AWH[len(AWH)-1].total_seconds()/3600, 2)))
        aw = formatTime(AWH[len(AWH)-1])

        #nc = ("%.2f"%(round(NCH[len(NCH)-1].total_seconds()/3600, 2)))
        nc = formatTime(NCH[len(NCH)-1])

        #ac = ("%.2f"%(round(ACH[len(ACH)-1].total_seconds()/3600, 2)))
        ac = formatTime(ACH[len(ACH)-1])

        infoQ = ['Total Hours :', tw, 'Working Hours :', aw, 'Non-Completed Actual Hours:', nc, 'Additional Hours:', ac]

        for i in range(len(infoQ)):
            infoLabels = infoLbl(text=infoQ[i])
            if i % 2 == 1:
                infoLabels.size_hint_x= 0.30
            info.add_widget(infoLabels)
