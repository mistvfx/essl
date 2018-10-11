from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import StringProperty, ObjectProperty

Builder.load_string("""
<dialogUI>:
    spacing: 5
    orientation: 'vertical'
    size_hint: 1, 1
    Label:
        text: root.msg
        size_hint: (0.75,0.75)
""")

class dialogUI(BoxLayout):
    msg = StringProperty()
    button = ObjectProperty(None)
    def __init__(self, content, btn):
        super(dialogUI, self).__init__()
        self.msg = content
        self.add_widget(btn)

class dialog(Popup):
    def __init__(self, title, content, btn):
        super(dialog, self).__init__()
        self.size_hint = (0.50, 0.25)
        self.title = title
        self.content = dialogUI(content, btn)
