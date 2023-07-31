from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivy.lang.builder import Builder
from kivy.properties import DictProperty, StringProperty, NumericProperty
import json

Builder.load_string(
"""
<CircularAvatarImage>
    app: app
    size_hint: None, None
    size: 62, 100
    elevation: 0
    md_bg_color: 0,0,0,0
    ripple_behavior: False

    MDRelativeLayout:
        size_hint: None, None
        size: 60, 100

        Circle:
            radius: [50,]
            size: 60, 60
            md_bg_color: 0, 0, 0, 1
        
        Circle:
            radius: [50,]
            size: 55, 55
            md_bg_color: 1, 1, 1, 1

        # profile picture
        FitImage:
            source: root.avatar 
            size_hint: None, None
            size: 53, 53
            radius: [53]
            pos_hint: {"center_x": 0.5,"center_y": 0.6}



<Circle@MDCard>
    size_hint: None, None
    elevation: 0
    pos_hint: {"center_x": 0.5,"center_y": 0.6}

"""
)


class CircularAvatarImage(MDCard):
    avatar = StringProperty()
    name = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.data = {
                "name": self.name
            }
            self.view_profile()

    def view_profile(self):
        with open("assets//Files//Other_User.json", 'w') as file:
            json.dump(self.data, file, indent=4)
        self.app.root.set_current(screen_name = "other_profile", side='up')