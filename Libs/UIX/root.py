import json

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty

class NumericInput(TextInput):
    min_value = NumericProperty()
    max_value = NumericProperty()
    def __init__(self, *args, **kwargs):
        TextInput.__init__(self, *args, **kwargs)
        self.input_filter = 'int'
        self.multiline = False

class Root(ScreenManager):

    previous_screen = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self._goto_previous_screen)
        with open("screens.json") as f:
            self.screens_data = json.load(f)
            #print(self.screens_data)

    def set_current(self, screen_name, side="left", quick=False):
        if not self.has_screen(screen_name):
            screen = self.screens_data[screen_name]
            print(screen)
            Builder.load_file(screen["kv"])
            exec(screen["import"])
            screen_object = eval(screen["object"])
            screen_object.name = screen_name
            self.add_widget(screen_object)

        self.previous_screen = {"name": self.current, "side": side}
        self.transition.direction = side
        self.transition.duration = 0 if quick else 0.4
        self.current = screen_name
        print(self.screen_names)

    def _goto_previous_screen(self, instance, key, *args):
        if key == 27:
            self.goto_previous_screen()
            return True
        return False

    def goto_previous_screen(self):
        if self.previous_screen:
            if not self.previous_screen["name"] == "auth":
                self.set_current(
                    self.previous_screen["name"],
                    side="right"
                    if self.previous_screen["side"] == "left"
                    else "left",
                )
                self.previous_screen = None
