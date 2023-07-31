from components.screen import PScreen

import json
from datetime import datetime
from components.savedcard import SavedCard

from components.circular_avatar_image import CircularAvatarImage


class HomePage(PScreen):
    
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
    
    def on_enter(self):
        self.__init__()
        self.list_stories()
        self.list_posts()

    def list_stories(self):
        self.ids.stories.clear_widgets()
        with open('assets//Files//Following.json', 'r') as file:
            followlst = json.load(file)
        for follow in followlst:
            if follow == self.username:
                data = followlst[follow]
                for name in data:
                    self.ids.stories.add_widget(CircularAvatarImage(
                        avatar = name["dp"],
                        name = name['username']
                    ))
    
    def list_posts(self):
        self.ids.timeline.clear_widgets()
        with open('assets//Files//Saved.json', 'r') as file:
            data = json.load(file)
            for post in data['Saved']:
                self.ids.timeline.add_widget(SavedCard(
                    id = post["id"],
                    name = post["name"],
                    source = post["video"],
                    thumbnail = post["thumbnail"]
                ))

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
