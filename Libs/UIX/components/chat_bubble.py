from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty, ColorProperty
import time
from components.boxlayout import PBoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from  kivy.utils import get_color_from_hex as hex
import json

Builder.load_string("""
#:import hex kivy.utils.get_color_from_hex

<ChatBubble>
    orientation: 'vertical'
    app: app
    size_hint_x: None
    #size_hint: [None, None]
    height: self.minimum_height
    #width: Window.width*.9
    canvas.before:
        Color:
            rgba: root.bg_color #hex('#FFBF00') if root.send_by_user else root.bg_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius:
                [dp(8), dp(8), (dp(-5), dp(5)), dp(8)] if root.send_by_user \
                else [(dp(-5), dp(5)), dp(8), dp(8), dp(8)]
    PLabel:
        text: root.text
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]
        padding: [dp(8), dp(8)]
        text_color: 0, 0, 0, 1
        font_name: 'assets//Fonts//Poppins//Poppins-Regular.ttf'
    PLabel:
        text: "Video"
        halign: "right"
        opacity: 1 if root.video else 0
        size_hint_y: None
        height: dp(20)
        padding: [dp(8), dp(8)]
        text_color: 0, 0, 0, 1
        text_size: self.width, None
        font_name: 'assets//Fonts//Poppins//Poppins-Regular.ttf'
    PLabel:
        text: root.time
        halign: "right"
        size_hint_y: None
        height: dp(20)
        padding: [dp(8), dp(8)]
        text_color: 0, 0, 0, 1
        text_size: self.width, None
        font_name: 'assets//Fonts//Poppins//Poppins-Regular.ttf'
    
"""
)


class ChatBubble(MDBoxLayout):
    text = StringProperty()
    raw_time = StringProperty()
    time = StringProperty('time')
    send_by_user = BooleanProperty(False)
    video = BooleanProperty(False)
    id = StringProperty('0')
    bg_color = ColorProperty()
    selected = []
    starttime = 0
    endtime = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = hex('#FF922B')

    def on_touch_down(self, touch):
        self.starttime = time.time()
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.endtime = time.time()
        lapsed = self.endtime - self.starttime
        if lapsed < 1 and self.collide_point(*touch.pos):
            if self.bg_color == [.1,.1,1,.5]:
                if self.send_by_user:
                    self.bg_color = hex('#FFBF00')
                else:
                    self.bg_color = hex('#FF922B')
            elif self.video:
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
        if lapsed > 2 and self.collide_point(*touch.pos):
            self.bg_color = [.1,.1,1,.5]
            self.selected.append(self.raw_time)
        return super().on_touch_up(touch)