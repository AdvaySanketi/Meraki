from kivy.properties import ObjectProperty, ListProperty, DictProperty
from Libs.UIX.components.toast import toast
from components.screen import PScreen
from kivy.core.window import Window
from kivymd.theming import get_color_from_hex
from kivy.properties import StringProperty
from kivy.utils import platform
import os
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from PIL import Image
from io import BytesIO
from kivy.core.image import Image as CoreImage
import json

class MusicScreen(PScreen):
    nav = ObjectProperty()
    music_grid = ObjectProperty()
    all_data = ListProperty()
    c_singer = StringProperty('')
    c_image = StringProperty('')
    c_track_name = StringProperty("")
    playlist = ""
    cur_song = DictProperty(defaultvalue={'image':'', 'track_name':'', 'singer':''})

    def __init__(self, **kwargs):
        self.song_list = {}
        super().__init__(**kwargs)
    
    def on_pre_enter(self, *args):
        with open("assets//Files//Current.json", 'r') as file:
            cur_song = json.load(file)
            self.cur_song = cur_song["Song"]
        self.song_list = self.get_songs_wn()
        self.all_data = []
        for song in self.song_list:
            data = {'time':'', 'image':'', 'track_name':'', 'singer':'', 'path':'', 'length':''}
            try:
                meta = File(song, easy=True)
                tag = ID3(song)
                raw_length = MP3(song).info.length
                if len(str(int(raw_length % 60))) == 1:
                    length = str(int(raw_length / 60)) + ':' + '0{0}'.format(str(int(raw_length % 60)))
                else:
                    length = str(int(raw_length / 60)) + ':' + '{0}'.format(str(int(raw_length % 60)))

                try:
                    data['track_name'] = meta.tags['title'][0] if 'title' in meta.tags else 'Unknown'
                except:
                    data['track_name'] = 'Unknown'
                try:
                    data['singer'] = meta.tags['artist'][0] if 'artist' in meta.tags else 'Unknown'
                except:
                    data['singer'] = 'Unknown'
                data['time'] = length
                data['length'] = raw_length
                data['path'] = song
                if self.playlist != '' and self.playlist != 'individual':
                    if self.playlist == 'taylor':
                        num = 1
                    elif self.playlist == 'dragons':
                        num = 2
                    elif self.playlist == 'kkumar':
                        num = 3
                    elif self.playlist == 'puth':
                        num = 5
                    elif self.playlist == 'srk':
                        num = 6
                    data['image'] = f'assets/Images/Playlist/{num}.jpg'
                else:
                    data['image'] = "assets//Images//logo.png"
                self.all_data.append(data)
            except Exception as e:
                pass
        with open('assets//Files//Song_List.json', 'w') as file:
            xyz = {
                "all_data" : self.all_data
            }
            json.dump(xyz, file, indent=4)
        return super().on_pre_enter(*args)

    def get_im(self, image_byt, ext):
        buf = BytesIO(image_byt)
        core = CoreImage(buf, ext=ext)
        return core.texture
        
    def get_songs_wn(self):
        song_list = {}
        if self.playlist != '':
            song_dir = 'assets/Songs/' + self.playlist
        else:
            song_dir = 'assets/Songs/individual/'
        for path, dirnames, filenames in os.walk(song_dir):
            for filename in filenames:
                if filename.endswith('.mp3'):
                    full_path = os.path.join(path, filename)
                    song_list[full_path] = ''
        return song_list

    def open_player(self):
        self.manager.set_current("music_player")

    def open_bottomplayer(self):
        self.manager.set_current("music_player", side="up")

    def playlist_id(self, playlist_id):
        self.playlist = playlist_id
        self.on_pre_enter()