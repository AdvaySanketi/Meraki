from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.lang.builder import Builder

Builder.load_string(
"""
<StoryCreator>
    size_hint: None, None
    size: 62, 100
    elevation: 0
    padding: 5
    spacing: 5
    md_bg_color: 0,0,0,0

    MDRelativeLayout:
        size_hint: None, None
        size: 60, 100

        Circle:
            radius: [50, ]  
            size: 60, 60
            md_bg_color: 1, 1, 1, 1
        
        Circle:
            radius: [50, ]  
            size: 55, 55
            md_bg_color: 1, 1, 1, 1

        FitImage:
            source: root.avatar
            size_hint: None, None
            size: 53, 53
            radius: [53]
            pos_hint: {"center_x": 0.5,"center_y": 0.6}   
        
        Circle:
            size_hint: None, None
            size: 17, 17
            md_bg_color: 1, 1, 1, 1
            radius: [17, ]
            pos_hint: {"center_x": 0.8,"center_y": 0.4}

<Circle@MDCard>
    size_hint: None, None
    elevation: 0
    pos_hint: {"center_x": 0.5,"center_y": 0.6}   
"""
)


class StoryCreator(MDCard):
    avatar = StringProperty()