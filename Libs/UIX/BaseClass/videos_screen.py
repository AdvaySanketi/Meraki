import json
from pydoc import isdata
import random
from Libs.UIX.components.toast import toast
from components.screen import PScreen
from components.boxlayout import PBoxLayout
from components.dialog import PDialog
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.video import Video

class VideoScreen(PScreen):
    video_list = []
    start = ""
    def __init__(self, **kw):
        with open("assets//Files//Videos.json", encoding='utf-8') as file:
            self.videos = json.load(file)
        for profile in self.videos["videos"]:
            _data = {
                'id': profile['id'],
                'name':profile['name'],
                'source':profile['video'],
                'caption':profile['caption'],
                'profile_pic':profile['profile_pic'],
                'likes':profile['likes'],
                'views':profile['views']
            }
            self.video_list.append(_data)

        random.shuffle(self.video_list)
        self.temp = self.video_list.copy()
        super().__init__(**kw)
    
    def on_enter(self, prev=None, *args):
        self.ids.saved.icon = 'bookmark-outline'
        self.ids.like.icon = 'heart-outline'
        with open("assets//Files//Current.json", 'r') as file:
            start = json.load(file)
            self.start = start["Video"]
            
        if prev == None and self.start["id"] == "None":
            try:
                self.data = self.temp.pop()
            except:
                self.temp = self.video_list
                self.data = self.temp.pop()
        elif self.start["id"].isdigit():
            self.data = self.start
            with open('assets//Files//Current.json', 'r') as file:
                data = json.load(file)
                data["Video"] = {"id":"None"}
            with open('assets//Files//Current.json', 'w') as file:
                json.dump(data, file, indent=4)
        else:
            self.data = prev
        self.video = Video(source=self.data['source'])
        self.layout.add_widget(self.video)
        self.video.state = 'play'
        self.video.options = {'eos': 'loop'}

        with open("assets//Files//Saved.json", 'r', encoding='utf-8') as file:
            file_data = json.load(file)
            for data in file_data['Saved']:
                if data['id'] == self.data['id']:
                    self.ids.saved.icon = 'bookmark'

        name = self.data['name']
        toast("Video by " + name)

        if name in self.data['likes']:
            self.ids.like.icon = 'heart'

        self.increase_views()
        return super().on_enter(*args)

    def on_pre_leave(self, *args):
        self.video.state = "stop"
        self.layout.remove_widget(self.video)
        return super().on_pre_leave(*args)
    
    def on_touch_down(self, touch):
        self.y_coordinate = touch.y
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        if touch.y > self.y_coordinate:
            self.video.state = "stop"
            self.layout.remove_widget(self.video)
            self.on_enter()
        elif touch.y < self.y_coordinate:
            self.previous()
        return super().on_touch_up(touch)

    def previous(self):
        try:
            prev_index = self.video_list.index(self.data) + 1
            prev = self.video_list[prev_index]
            self.video.state = "stop"
            self.layout.remove_widget(self.video)
            self.on_enter(prev= prev)
        except:
            pass


    def save(self):
        with open("assets//Files//Videos.json", 'r', encoding='utf-8') as file:
            videos = json.load(file)
            for video in videos["videos"]:
                if video["id"] == self.data["id"]:
                    save_vid = {
                        'id': video['id'],
                        'video': video['video'],
                        'name': video['name'],
                        'thumbnail': video['thumbnail']
                    }
        with open("assets//Files//Saved.json", 'r', encoding='utf-8') as file:
            file_data = json.load(file)
            if save_vid not in file_data['Saved']:
                file_data["Saved"].append(save_vid)
                self.ids.saved.icon = 'bookmark'
                toast("Video Saved Successfully")
            else:
                file_data['Saved'].remove(save_vid)
                self.ids.saved.icon = 'bookmark-outline'
                toast("Video Removed from Saved")

        with open("assets//Files//Saved.json", 'w', encoding='utf-8') as file:
            json.dump(file_data, file, indent = 4)
    
    def increase_likes(self):
        with open("assets//Files//Active_User.json", 'r') as file:
            user = json.load(file)
            name= user["username"]
        with open("assets//Files//Videos.json", 'r', encoding='utf-8') as file:
            videos = json.load(file)
            for video in videos["videos"]:
                if video["id"] == self.data["id"]:
                    if name not in video['likes']:
                        self.ids.like.icon = 'heart'
                        video["likes"].append(name)
                    else:
                        self.ids.like.icon = 'heart-outline'
                        video['likes'].remove(name)
        with open("assets//Files//Videos.json", 'w', encoding='utf-8') as file:
            json.dump(videos,file, indent = 4)
    
    def increase_views(self):
        with open("assets//Files//Videos.json", 'r', encoding='utf-8') as file:
            videos = json.load(file)
            for video in videos["videos"]:
                if video["id"] == self.data["id"]:
                    video["views"] = str(int(video["views"]) + 1)
        with open("assets//Files//Videos.json", 'w', encoding='utf-8') as file:
            json.dump(videos,file, indent = 4)

    def see_account(self):
        data = {
            "name": self.data['name']
        }
        with open("assets//Files//Active_User.json", 'r') as file:
            user = json.load(file)
            name= user["username"]
        if name == self.data["name"]:
            self.manager.set_current("profile")
        else:
            with open("assets//Files//Other_User.json", 'w') as file:
                json.dump(data, file, indent=4)
            self.manager.set_current("other_profile")

    def caption(self):
        PDialog(content=CaptionDialogContent(self.data['name'], self.data['caption'], str(len(self.data['likes'])))).open()

    def share_videos(self):
        self.manager.set_current("chat")
        self.manager.get_screen("chat").share_video(username = self.data['name'], id = self.data['id'])

class CaptionDialogContent(PBoxLayout):
    def __init__(self, name, caption, likes, **kw):
        self.name = name
        self.caption = caption
        self.likes = likes
        super().__init__(**kw)
