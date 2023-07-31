from Libs.UIX.components.usercard import UserCard
from Libs.UIX.components.vidcard import VidCard
from components.screen import PScreen
import json
#from googlesearch import search
from youtubesearchpython import VideosSearch
import urllib.request
from kivy.core.window import Window
from components.toast import toast
from components.musiccard import MusicCardNormal
from kivy.properties import ListProperty, BooleanProperty

class SearchScreen(PScreen):

    song_list = ListProperty([])
    user_list = ListProperty([])
    video_list = ListProperty([])
    song_btn = BooleanProperty(False)

    def __init__(self, **kwargs):
        with open('assets/Files/Videos.json', 'r') as file:
            videos = json.load(file)
            self.videos = videos['videos']
        with open('assets/Files/User_Details.json', 'r') as file:
            users = json.load(file)
            self.users = users['Users']
        Window.bind(on_key_down=self._on_keyboard_down)
        super().__init__(**kwargs)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.ids.search.focus and keycode == 40:
            if self.ids.search.text == '':
                toast("Please Enter Text to Search")
            else:
                self.search_results()

    def on_enter(self, *args):
        #self.ids.search_results.clear_widgets()
        return super().on_enter(*args)

    def search_results(self):
        search_txt = self.ids.search.text.lower()
        grid = self.ids.search_results
        grid.clear_widgets()
        
        if search_txt != '':
            self.get_users(search_txt)
            self.get_videos(search_txt)
            try:
                self.get_music(search_txt)
            except:
                toast("Please Try Again after Some Time")

            if self.song_btn:
                self.add_songs(grid)
            else:
                self.add_uservids(grid)

    def add_uservids(self, grid):
        grid.clear_widgets()

        for account in self.user_list:
            user = UserCard()
            user.username = account['username']
            user.bio = account['bio']
            user.image = account['thumbnail']

            grid.add_widget(user)

        for vid in self.video_list:
            video = VidCard()
            video.id = vid['id']
            video.username = vid['user']
            video.caption = vid['caption']
            video.image = vid['thumbnail']

            grid.add_widget(video)

    def add_songs(self, grid):
        grid.clear_widgets()

        for song in self.song_list:
            music = MusicCardNormal()
            music.track_name = song['title']
            music.image = song['thumbnail']
            music.singer = song['singer']
            music.time = song['duration']
            music.link = song['url']
            music.active = False

            grid.add_widget(music)

    def get_users(self, search):
        self.user_list = []
        user_lst = []
        for user in self.users:
            if search in user['username'].lower() or search in user['bio'].lower():
                user_lst.append(user)
        for i in user_lst:
            user = {'username': "", "bio": "", "thumbnail": ""}
            user['username'] = i['username']
            user['bio'] = i['bio']
            user['thumbnail'] = i['profile_pic']
            self.user_list.append(user)

    def get_music(self,search):
        self.song_list = []
        txt = search + ' songs'
        videosSearch = VideosSearch(txt, limit = 3)
        for i in range(3):
            song = {'title': "", "singer": "", "duration": "", "thumbnail": "", "url": ""}
            song['thumbnail'] = videosSearch.result()['result'][i]['thumbnails'][0]['url']
            song['title'] = videosSearch.result()['result'][i]['title']
            song['url'] = videosSearch.result()['result'][i]['link']
            song['duration'] = videosSearch.result()['result'][i]['duration']
            if not song['duration']:
                song['duration'] = "2:69"
            song['singer'] = videosSearch.result()['result'][i]['channel']['name']
            self.song_list.append(song)

    def get_videos(self, search):
        self.video_list = []
        video_lst = []
        for video in self.videos:
            if search in video['name'].lower() or search in video['caption'].lower():
                video_lst.append(video)
        
        for i in video_lst:
            video = {'id': "", 'caption': "", "user": "", "thumbnail": ""}
            video['id'] = i['id']
            video['user'] = i['name']
            video['caption'] = i['caption']
            video['thumbnail'] = i['thumbnail']
            self.video_list.append(video)

    def choose(self, choice):
        grid = self.ids.search_results
        if choice == "uservids":
            self.song_btn = False
            self.add_uservids(grid)
        else:
            self.song_btn = True
            self.add_songs(grid)