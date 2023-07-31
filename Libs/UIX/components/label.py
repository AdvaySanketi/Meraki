from kivy.lang import Builder
from kivy.properties import ColorProperty, StringProperty
from kivy.uix.label import Label

from components.adaptive_widget import AdaptiveWidget
from core.theming import ThemableBehavior

Builder.load_string("""
<PLabel>
    font_name: 'assets/Fonts/Poppins/Poppins-Regular.ttf'
    color:
        self.text_color if self.text_color \
        else self.theme_cls.text_color

<PIcon>
    font_name: 'Icons'
    font_size: sp(40)

<Text>:
    text_size: self.size
    valign: "middle"
    font_name: "assets//Fonts//Poppins//Poppins-Regular.ttf"
    shorten_from: "right"
    shorten: True
    color: [0,0,0,1]
    markup: True
"""
)


class PLabel(ThemableBehavior, AdaptiveWidget, Label):
    text_color = ColorProperty(None)


class PIcon(PLabel):
    icon = StringProperty()

class Text(Label):
    def __init__(self, **kw):
        super().__init__(**kw)
