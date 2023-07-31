from kivy.lang.builder import Builder
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
import json

Builder.load_string(
"""
<FollowingCard>:
    app: app
    size_hint_y: None
    height: '100dp'
    width: '100dp'
    elevation: 0
    md_bg_color: [0, 0, 0, 0]
    radius: '10dp', 
    font_size: '15sp'
    ripple_behavior: False
    FitImage:
        radius: 10
        source: root.thumbnail
        pos_hint: {'center_x':.5, 'center_y':.5}
        opacity: .8

"""
)

class FollowingCard(MDCard):

    name = StringProperty()
    thumbnail = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        print(self.thumbnail)

    def on_release(self, *args):
        print(self.thumbnail)
        data = {
            "name": self.name
        }
        with open("assets//Files//Active_User.json", 'r') as file:
            user = json.load(file)
            username= user["username"]
        if username == self.data["name"]:
            self.manager.set_current("profile")
        else:
            with open("assets//Files//Other_User.json", 'w') as file:
                json.dump(data, file, indent=4)
        self.app.root.set_current("other_profile")
        return super().on_release(*args)
