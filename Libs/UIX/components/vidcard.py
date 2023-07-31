from kivy.lang.builder import Builder
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import CommonElevationBehavior
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, DictProperty, NumericProperty
import json

Builder.load_string("""
<VidCard>:
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
            text: root.caption
            font_size: '12sp'
            shorten: True
            shorten_from: 'right'
            adaptive_height: True
            size_hint_y: None
            text_size: self.width, None
            height: self.texture_size[1]
    Label:
        text: "Video"
        size_hint_x: None
        size: self.texture_size
        bold: True
"""
)

class VidCard(MDCard, CommonElevationBehavior):
    id = StringProperty('')
    username = StringProperty('')
    caption = StringProperty('')
    image = StringProperty('')

    def on_release(self, *args):
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

        self.app.root.set_current(screen_name = "videos", side='up')
        return super().on_release(*args)