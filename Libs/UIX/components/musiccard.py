from kivy.lang.builder import Builder
from kivymd.uix.card import MDCardSwipe, MDCard
from kivymd.uix.behaviors import CommonElevationBehavior
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, DictProperty, NumericProperty
import json
from pytube import YouTube
import youtube_dl
import pafy
import urllib.request
from youtubesearchpython import VideosSearch
import os

from Libs.UIX.components.toast import toast

Builder.load_string("""
<MusicCard>:
    app: app
    ripple_behavior: True
    size_hint_y: None
    height: '50dp'
    md_bg_color: [0, 0, 0, 1]
    anchor: 'right'
    elevation: 0
    max_opened_x: '50dp'
    type_swipe: 'hand'
    # width: 5
    # size_hint_x: None
    MDCardSwipeLayerBox:        
        MDCard:
            orientation: 'vertical'
            elevation: 0
            MDIcon:
                id: trash
                icon: 'delete-outline'
                halign: 'right'
                padding: '10dp', 0
                md_bg_color: [0, 0, 0, 0]
                md_bg_color_disabled: [0, 0, 0, 0]
    MDCardSwipeFrontBox:
        elevation: 0
        MDCard:
            padding: '5dp', '5dp'
            spacing: '5dp'
            elevation: 0
            ripple_behavior: True

            MDIcon:
                icon: 'drag-horizontal-variant'
                font_size: '15sp'
                size_hint_x: None
                width: self.texture_size[1]
            MDFloatLayout:
                id: fl
                size_hint: None, None
                width: '40dp'
                height: '40dp'
                pos_hint: {'center_y':.5}
                FitImage:
                    id: image
                    radius: 20,
                    source: root.image
                    pos_hint: {'center_x':.5, 'center_y':.5}
                    opacity: .5 if root.active == True else 1
                    size_hint_y: None
                    height: '40dp'
                IconBtn: 
                    icon: 'align-vertical-bottom' if root.active == True else ''
                    pos_hint: {'center_x':.5,  'center_y':.5}
                    size_hint: None, None
                    font_size: '20dp'
                    ripple_behavior: False
            MDBoxLayout:
                orientation: 'vertical'
                MDLabel:
                    text: root.track_name
                    bold: True
                    shorten: True
                    shorten_from: 'right'
                MDLabel:
                    text: root.singer
                    font_size: '12sp'
                    shorten: True
                    shorten_from: 'right'
            Label:
                text: root.time
                size_hint_x: None
                size: self.texture_size
                bold: True

<MusicCardPlaylist>:
    size_hint_y: None
    height: '50dp'
    md_bg_color: [0, 0, 0, 1]
    anchor: 'right'
    elevation: 0
    max_opened_x: '50dp'
    type_swipe: 'auto'
    MDCardSwipeLayerBox:        
    MDCardSwipeFrontBox:
        MDCard:
            ripple_behavior: True
            padding: '5dp', '5dp'
            spacing: '5dp'
            elevation: '1dp'
            IconBtn:
                icon: 'drag-horizontal-variant'
                font_size: '20dp'
                size_hint_x: None
                pos_hint: {'center_y':.5}
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
                    opacity: .5 if root.active == True else 1
                    size_hint_y: None
                    height: '40dp'
                IconBtn: 
                    icon: 'align-vertical-bottom' if root.active == True else ''
                    pos_hint: {'center_x':.5,  'center_y':.5}
                    size_hint: None, None
                    font_size: '20dp'
                    ripple_behavior: False
            MDBoxLayout:
                orientation: 'vertical'
                MDLabel:
                    text: root.track_name
                    bold: True
                    shorten: True
                    shorten_from: 'right'
                MDLabel:
                    text: root.singer
                    font_size: '12sp'
                    shorten: True
                    shorten_from: 'right'
            Label:
                text: root.time
                size_hint_x: None
                size: self.texture_size
                bold: True  
            IconBtn:
                icon: 'close'
                font_size: '20dp'
                halign: 'center'
                size_hint_x: None
                md_bg_color: [0, 0, 0, 0]
                md_bg_color_disabled: [0, 0, 0, 0]
                pos_hint: {'center_y':.5}

<MusicCardNormal>:
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
        id: fl
        size_hint: None, None
        width: '40dp'
        height: '40dp'
        pos_hint: {'center_y':.5}
        FitImage:
            id: image
            radius: 20,
            source: root.image
            pos_hint: {'center_x':.5, 'center_y':.5}
            opacity: .5 if root.active == True else 1
            size_hint_y: None
            height: '40dp'
        IconBtn: 
            icon: 'align-vertical-bottom' if root.active == True else ''
            pos_hint: {'center_x':.5,  'center_y':.5}
            size_hint: None, None
            font_size: '20dp'
            ripple_behavior: False
    MDBoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: root.track_name
            bold: True
            shorten: True
            shorten_from: 'right'
        MDLabel:
            text: root.singer
            font_size: '12sp'
            shorten: True
            shorten_from: 'right'
    Label:
        text: root.time
        size_hint_x: None
        size: self.texture_size
        bold: True
"""
)

class MusicCard(MDCardSwipe):
    time = StringProperty()
    image = StringProperty()
    track_name = StringProperty()
    singer = StringProperty()
    path = StringProperty()
    length = NumericProperty()
    active = BooleanProperty(defaultvalue=False)
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if (touch.time_end - touch.time_start) > .5:
                self.open_card()
                return True
            self.load_music()
         
        return super().on_touch_up(touch)
    
    def load_music(self):
        self.dat = {'time':self.time, 'image':self.image, 'track_name':self.track_name, 'singer':self.singer, 'path':self.path, 'length':self.length,}
        with open('assets//Files//Current.json', 'r') as file:
            data = json.load(file)
            data["Song"] = self.dat
        with open('assets//Files//Current.json', 'w') as file:
            json.dump(data, file, indent=4)
        if self.app.root.has_screen('music_player'):
            self.app.root.get_screen('music_player').play()
        self.app.root.set_current(screen_name = "music_player", side='up')

class MusicCardPlaylist(MDCardSwipe):
    track_name = StringProperty('')
    singer = StringProperty('')
    time = StringProperty('')
    image = StringProperty('')
    active = BooleanProperty(defaultvalue=False)

class MusicCardNormal(MDCard, CommonElevationBehavior):
    track_name = StringProperty('')
    singer = StringProperty('')
    time = StringProperty('')
    image = StringProperty('')
    link = StringProperty('')
    active = BooleanProperty(defaultvalue=False)
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.load_music()
         
        return super().on_touch_up(touch)
    
    def load_music(self):
        try:
            video = pafy.new(self.link)
            videosSearch = VideosSearch(self.link, limit = 1)
            best = video.getbestaudio(preftype = "mp3")
            best.download(filepath= "assets//Songs//Individual//" + video.title + ".mp3", quiet = True)
            thumb_url = videosSearch.result()['result'][0]['thumbnails'][0]['url']
            urllib.request.urlretrieve(thumb_url, 'assets//Songs//thumb.jpg')
        except Exception as e:
            print(e)
            
        '''yt = YouTube(self.link,
        on_complete_callback = self.complete_func)

        video = yt.streams.filter(only_audio=True).first()

        out_file = video.download(output_path="assets//Songs//Individual//")

        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)'''


    def complete_func(self, *args):
        toast("Download Completed Successfully")