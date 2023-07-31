from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivy.lang.builder import Builder
from kivy.properties import DictProperty, StringProperty, NumericProperty
from kivy.clock import Clock
from components.dialog import PDialog
from components.boxlayout import PBoxLayout
import json
import os

Builder.load_string(
"""
#:import hex kivy.utils.get_color_from_hex

<PostCard>:
    app: app
    size_hint: None, None
    height: '100dp'
    width: '100dp'
    elevation: 0
    md_bg_color: [0, 0, 0, 0]
    radius: '10dp', 
    font_size: '15sp'
    MDFloatLayout:
        FitImage:
            radius: 10
            source: root.thumbnail
            pos_hint: {'center_x':.5, 'center_y':.5}
            opacity: .8

        MDCheckbox:
            pos_hint: {'right':.95, 'top':.9}
            size_hint: None, None
            size: '20dp', '20dp'
            disabled: True
            opacity: 0
            checkbox_icon_down: 'checkbox-marked-circle'
            checkbox_icon_normal: 'checkbox-blank-circle-outline'
        MDLabel:
            text: ''
            pos_hint: {'top':.2, 'x':.04}
            size_hint_y: None
            height: self.texture_size[1]
            # padding: '5dp', 0
            bold: True
            font_size: '12sp'

<PostCardExpanded>:
    orientation: "vertical"
    adaptive_height: True
    padding: dp(15)
    spacing: dp(10)

    ListItem:
        id: views
        text: "Views"
        secondary_text: root.Views + " Views"
        icon: "eye"
        bg_color: hex("#2C5F2D")
        text_color: [1,1,1,1]

    ListItem:
        id: likes
        text: "Likes"
        secondary_text: root.Likes + " Likes"
        icon: "heart"
        bg_color: hex("#0063B2FF")
        text_color: [1,1,1,1]
        
"""
)

class PostCard(MDCard):
    id = StringProperty()
    source = StringProperty()
    thumbnail = StringProperty()
    scheduled_event = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.scheduled_event is not None:
                self.scheduled_event.cancel()
                self.scheduled_event = None
            if touch.is_double_tap:
                self.statistics()
            else:
                double_tap_wait_s = .5
                self.scheduled_event = Clock.schedule_once(self.open_video, double_tap_wait_s)

    def statistics(self, *args):
        PDialog(content=PostCardExpanded(self.id)).open()
    
    def open_video(self, *args):
        with open("assets//Files//Videos.json", encoding='utf-8') as file:
            self.videos = json.load(file)
        for profile in self.videos["videos"]:
            if profile['id'] == self.id:
                self.video = {
                    'id': profile['id'],
                    'name':profile['name'],
                    'source':profile['video'],
                    'caption':profile['caption'],
                    'profile_pic':profile['profile_pic'],
                    'likes':str(len(profile['likes'])),
                    'views':profile['views']
                }
        with open('assets//Files//Current.json', 'r') as file:
            data = json.load(file)
            data["Video"] = self.video
        with open('assets//Files//Current.json', 'w') as file:
            json.dump(data, file, indent=4)

        self.app.root.set_current("videos", side="up")

class PostCardExpanded(PBoxLayout):
    Views = StringProperty("0")
    Likes = StringProperty("0")

    def __init__(self, vid_id, **kwargs):
        super().__init__(**kwargs)
        with open('assets//Files//Videos.json', 'r') as file:
            data = json.load(file)
        for video in data['videos']:
            if video['id'] == vid_id:
                self.Views = video['views']
                self.Likes = str(len(video['likes']))
