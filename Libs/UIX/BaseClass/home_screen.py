from components.screen import PScreen
from components.savedcard import SavedCard
from components.circular_avatar_image import CircularAvatarImage
from kivy.properties import ListProperty, ObjectProperty
import json
from datetime import datetime 

class HomeScreen(PScreen):
    saved = ListProperty()
    saved_grid = ObjectProperty()
    following = ListProperty()
    following_grid = ObjectProperty()

    def __init__(self, **kwargs):
        with open('assets//Files//Active_User.json', 'r') as file:
            user_data = json.load(file)
            self.username = user_data['username']
        self.wish_txt = self.get_part_of_day(datetime.now().hour)
        with open('assets//Files//User_Details.json', 'r') as file:
            self.data = json.load(file)
            for data in self.data['Users']:
                if data['username'] == self.username:
                    self.dp = data['profile_pic'] 
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        with open('assets//Files//Following.json', 'r') as file:
            followlst = json.load(file)
        for follow in followlst:
            if follow == self.username:
                names = followlst[follow]
        for name in names:
            namelst = {'name': '', 'avatar': ''}
            namelst['name'] = name['username']
            namelst['avatar'] = name["dp"]
            self.following.append(namelst)
        #self.ids.following_scrl.data = self.following

        with open('assets//Files//Saved.json', 'r') as file:
            self.savedlst = json.load(file)
        for post in self.savedlst['Saved']:
            datalst = {'id':'', 'name':'', 'source':'', 'thumbnail':'', 'likes':''}
            datalst['id'] = post['id']
            datalst['name'] = post['name']
            datalst['source'] = post['video']
            datalst['thumbnail'] = post['thumbnail']
            datalst['likes'] = post['likes']
            self.saved.append(datalst)
        #self.ids.saved_scroll.data = self.saved

        return super().on_pre_enter(*args)
    
    def get_part_of_day(self, hour):
        return (
            "Good Morning"
            if 5 <= hour <= 11
            else "Good Afternoon"
            if 12 <= hour <= 17
            else "Good Evening"
            if 18 <= hour <= 22
            else "Good Night"
        )