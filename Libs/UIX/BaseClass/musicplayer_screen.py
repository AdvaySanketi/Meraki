from os import supports_bytes_environ
from kivy.lang.builder import Builder
from components.screen import PScreen
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, DictProperty, BooleanProperty, OptionProperty, ListProperty
from pygame import mixer, USEREVENT, event
import pygame
from kivy.clock import Clock
from random import randint
import json

class MusicPlayerScreen(PScreen):
    data = DictProperty(defaultvalue={'time':'', 'image':'', 'track_name':'', 'singer':'', 'path':'', 'length':0}) 
    all_data = ListProperty()
    is_playing = BooleanProperty(defaultvalue=True)
    shuffle = BooleanProperty(defaultvalue=True)
    loop = BooleanProperty(defaultvalue=False)
    app = ObjectProperty()
    player = ObjectProperty()

    def __init__(self, **kwargs):
        mixer.init()
        self.SliderEvent = Clock.schedule_interval(self.UpdateSlider, 1)
        super().__init__(**kwargs)

    def on_enter(self, *args):
        if mixer.music.get_busy() == False:
            self.is_playing = True
            self.ids.slider.value = 0
            with open("assets//Files//Song_List.json", 'r') as file:
                songs = json.load(file)
                self.all_data = songs['all_data']
            with open('assets//Files//Current.json', 'r') as file:
                data = json.load(file)
                self.data = data["Song"]
            mixer.music.load(self.data['path'])     
            mixer.music.play()
            self.ids.slider.max = self.calc_max()
            self.c_track_name = self.data['track_name']
            self.c_image = self.data['image']
            self.c_singer = self.data['singer']
        else:
            pass
        return super().on_enter(*args)

    def play(self):
        if self.is_playing == True:      
            mixer.music.pause()
            self.is_playing = False
        else:
            mixer.music.unpause()
            self.is_playing = True
            
        clock = pygame.time.Clock()
        mixer.music.is_playing = True

    def toggle_shuffle(self):
        if self.shuffle == True:
            self.shuffle = False
            return
        self.shuffle = True

    def toggle_loop(self):
        if self.loop == True:
            self.loop = False
            return
        self.loop = True

    def UpdateSlider(self, instance):
        if self.is_playing == True:
            #print(self.ids.slider.value, '    ', self.ids.slider.max)
            if self.ids.slider.value < self.ids.slider.max:
                #print(self.ids.slider.value, '   ', self.ids.slider.max)
                self.ids.slider.value += 0.1
                self.player = self.ids.slider.value
            else:
                print("Song Finished")
                self.is_playing = False
                if self.loop:
                    self.ids.slider.value = self.ids.slider.min
                    mixer.music.set_pos(0)
                    self.is_playing = True
                else:
                    #self.next_music()
                    pass

    def calc_max(self):
        self.original_max = self.ids.slider.max
        m, sec = str(self.ids.slider.max).split('.')
        mins = int(m)*60
        secs = float(sec[0:2])
        time = (mins + secs)/10
        return time

    def on_touch_up(self, touch):
        if self.ids.slider.collide_point(*touch.pos):
            value = (self.ids.slider.value * self.original_max) / (self.ids.slider.max)
            m, sec = str(value).split('.')
            mins = int(m)*60
            secs = float(sec[0:2])
            time = mins + secs
            try:
                mixer.music.set_pos(time)
            except:
                pass
        super().on_touch_up(touch)

    def next_music(self):
        #index = self.shuffle_list()
        index = 0
        self.ids.slider.value = 0
        if self.shuffle:
            self.data = self.all_data[index]
            mixer.music.load(self.data['path'])
            mixer.music.play()
            self.is_playing = True
            self.ids.slider.max = self.calc_max()
            return
        index = self.all_data.index(self.data)
        if index < (len(self.all_data) - 1):
            self.data = self.all_data[index+1]
        else:
            self.data = self.all_data[0]
        mixer.music.load(self.data['path'])
        mixer.music.play()
        self.is_playing = True
        self.ids.slider.max = self.calc_max()

    def prev_music(self):
        index = self.all_data.index(self.data)
        if index > 0:
            self.data = self.all_data[index-1]
        else:
            self.data = self.all_data[len(self.all_data)-1]
        mixer.music.load(self.data['path'])
        mixer.music.play()
        self.is_playing = True

    def shuffle_list(self):
        print(self.all_data)
        index = randint(0, len(self.all_data)-1)
        return index

    def bottomplayer(self, ct):
        pass
