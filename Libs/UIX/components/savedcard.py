from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivy.lang.builder import Builder
from kivy.properties import DictProperty, StringProperty, NumericProperty
import json

Builder.load_string(
"""
#:import hex kivy.utils.get_color_from_hex

<SavedCard>:
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

class SavedCard(MDCard):
    id = StringProperty()
    name = StringProperty()
    source = StringProperty()
    thumbnail = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

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