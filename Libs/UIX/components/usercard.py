from kivy.lang.builder import Builder
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import CommonElevationBehavior
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, DictProperty, NumericProperty
import json

Builder.load_string("""
<UserCard>:
    app: app
    ripple_behavior: True
    size_hint_y: None
    height: '50dp'
    md_bg_color: [0, 0, 0, 1]
    padding: '5dp', '5dp'
    spacing: '5dp'
    elevation: 0
    ripple_behavior: True
    MDFloatLayout:
        size_hint: None, None
        width: '40dp'
        height: '40dp'
        pos_hint: {'center_y':.5}
        FitImage:
            id: image
            radius: 20,
            source: root.image
            pos_hint: {'center_x':.5, 'center_y':.5}
            size_hint_y: None
            height: '40dp'
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(4)
        Label:
            text: root.username
            bold: True
            shorten: True
            shorten_from: 'right'
            size_hint_y: None
            text_size: self.width, None
            height: self.texture_size[1]
        Label:
            text: root.bio
            font_size: '12sp'
            shorten: True
            shorten_from: 'right'
            adaptive_height: True
            size_hint_y: None
            text_size: self.width, None
            height: self.texture_size[1]
    Label:
        text: "User"
        size_hint_x: None
        size: self.texture_size
        bold: True
"""
)

class UserCard(MDCard, CommonElevationBehavior):
    username = StringProperty('')
    bio = StringProperty('')
    image = StringProperty('')

    def on_release(self, *args):
        self.data = {
            "name": self.username
        }
        with open("assets//Files//Other_User.json", 'w') as file:
            json.dump(self.data, file, indent=4)
        self.app.root.set_current(screen_name = "other_profile", side='up')
        return super().on_release(*args)