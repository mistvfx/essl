from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from pages import table

closeBtn = Button()
TWH = [0]*1
AWH = [0]*1
NCH = [0]*1
ACH = [0]*1

class infoTab(BoxLayout):
    def __init__(self, **args):
        super(infoTab, self).__init__(**args)
        self.popUI()

    def popUI(self):
        overallLayout = BoxLayout(orientation='vertical')
        self.add_widget(overallLayout)

        """ Defining Header and closeBtn """

        headerLayout = BoxLayout(orientation='horizontal', size_hint=(1, 0.25))
        overallLayout.add_widget(headerLayout)
        header = GridLayout(cols=3, size_hint=(0.65, None))
        headerLayout.add_widget(header)
        headers = ['I/O', 'TIME', 'DOOR']
        for i in range(3):
            headerLabel = Label(text=headers[i])
            header.add_widget(headerLabel)

        global closeBtn
        headerLayout.add_widget(closeBtn)

        """ Table and info """

        tableLayout = BoxLayout(orientation='horizontal')
        overallLayout.add_widget(tableLayout)
        tab = table.dataTable()
        tab.size_hint=(0.65, 1)
        tableLayout.add_widget(tab)

        """ Defining Info """

        info = GridLayout(cols=2, size_hint=(0.35, 1))
        tableLayout.add_widget(info)

        global TWH, AWH, NCH, ACH

        infoQ = ['Total Hours :', str(round(TWH[len(TWH)-1].total_seconds()/3600, 2)), 'Working Hours :', str(round(AWH[len(AWH)-1].total_seconds()/3600, 2)), 'Non-Completed Actual Hours:', str(round(NCH[len(NCH)-1].total_seconds()/3600, 2)), 'Additional Hours:',
                str(round(ACH[len(ACH)-1].total_seconds()/3600, 2))]

        for i in range(len(infoQ)):
            infoLabels = Label(text=infoQ[i])
            info.add_widget(infoLabels)
