from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import ColorProperty, OptionProperty
from kivy.utils import get_color_from_hex as gch

from core import font_definitions

class ThemableBehavior(EventDispatcher):
    def __init__(self, **kwargs):
        self.theme_cls = MDApp.get_running_app().theme_cls
        super().__init__(**kwargs)

#font_definitions.register_fonts()