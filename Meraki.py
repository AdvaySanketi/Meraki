from kivy.utils import platform
from kivy.core.window import Window
from kivymd.app import MDApp
import os
import sys
import json

root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.join(root_dir, "Libs", "AppLibs"))
sys.path.insert(0, os.path.join(root_dir, "Libs", "UIX"))

from utils.configparser import config
from root import Root
from androspecific import statusbar

if platform != "android":
    Window.size = (350, 650)
    Window.left = 1175
    Window.top = 100


class MerakiApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title = "Meraki"
        self.icon = "assets/Images/logo.png"

        self.theme_cls.theme_style = config.get_theme_style()

        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"

    def build(self):
        self.root = Root()
        try:
            with open('assets//Files//Active_User.json', 'r') as file:
                data = json.load(file)
            screen = "daily_login"
        except Exception as E:
            screen = "auth"
        self.root.set_current("profile")

    def on_start(self):
        statusbar.set_color(self.theme_cls.primary_color)

