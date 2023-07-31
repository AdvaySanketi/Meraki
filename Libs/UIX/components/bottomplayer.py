from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ObjectProperty, ListProperty
from kivy.lang.builder import Builder
from BaseClass.music_screen import MusicScreen

Builder.load_string(
"""
<BottomPlayer>:
    app: app
    size_hint: None, None
    height: '60dp'
    width: '250dp'
    pos_hint: {'right':1}
    radius: '30dp', 0, 0, 0
    md_bg_color: app.theme_cls.primary_color
    padding: '10dp'
    spacing: '5dp'
    FitImage:
        id: image
        radius: 20,
        source: root.image
        pos_hint: {'center_x':.5, 'center_y':.5}
        size_hint: None, None
        height: '30dp'
        width: '30dp'
    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        pos_hint: {'center_y':.5}
        spacing: '5dp'
        MDLabel:
            text: root.track_name
            bold: True
            size_hint_y: None
            height: self.texture_size[1]
            shorten_from: 'right'
            shorten: True
        MDLabel:
            text: root.singer
            font_size: '12sp'
            size_hint_y: None
            height: self.texture_size[1]
            bold: True
            shorten_from: 'right'
            shorten: True
    MDIconButton:
        icon: 'chevron-up'
        pos_hint: {'center_y':.5}                

"""
)

class BottomPlayer(MDCard):
    track_name = StringProperty('x')
    singer = StringProperty('y')
    image = StringProperty('assets//Images//logo.png')
    active = BooleanProperty(defaultvalue=False)

