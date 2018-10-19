from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder

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

        tw = str(round(TWH[len(TWH)-1].total_seconds()/3600, 2)).split(".")
        tw[1]= str(round((int(tw[1])/100)*60))
        tw = ".".join(tw)

        aw = str(round(AWH[len(AWH)-1].total_seconds()/3600, 2)).split(".")
        aw[1]= str(round((int(aw[1])/100)*60))
        aw = ".".join(aw)

        nc = str(round(NCH[len(NCH)-1].total_seconds()/3600, 2)).split(".")
        nc[1]= str(round((int(nc[1])/100)*60))
        nc = ".".join(nc)

        ac = str(round(ACH[len(ACH)-1].total_seconds()/3600, 2)).split(".")
        ac[1]= str(round((int(ac[1])/100)*60))
        ac = ".".join(ac)

        infoQ = ['Total Hours :', tw, 'Working Hours :', aw, 'Non-Completed Actual Hours:', nc, 'Additional Hours:', ac]

        for i in range(len(infoQ)):
            infoLabels = infoLbl(text=infoQ[i])
            if i % 2 == 1:
                infoLabels.size_hint_x= 0.30
            info.add_widget(infoLabels)
