from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.lang.builder import Builder

Builder.load_string(
"""
<PostCard2>:
    orientation: 'vertical'
    size_hint_y: None
    height: "420dp"
    spacing: 2
    elevation: 0

    MDBoxLayout:
        padding: 2
        adaptive_height: True

        OneLineAvatarListItem:
            text: f'[b][size=14]{root.username}[/size][/b]'
            divider: None
            _no_ripple_effect: True

            ImageLeftWidget:
                source: root.avatar 
                radius: [20, ]
        
        MDIconButton:
            icon: 'dots-vertical'
    

    # Post
    FitImage:
        adaptive_height: True
        source: root.post

    # Reactions
    MDBoxLayout:
        padding: 5, 0, 0, 0         
        spacing: 2
        adaptive_height: True 


        MDIconButton:
            icon: 'heart-outline'
        
        MDIconButton:
            icon: 'message-outline'
        
        MDIconButton:
            icon: 'send-outline'
        
        Widget:

        MDIconButton:
            icon: 'bookmark-outline'


    MDBoxLayout:
        orientation: 'vertical'
        padding: 5, 0, 0, 0  
        spacing: 2
        adaptive_height: True 

        MyLabel:   
            text: f'{root.likes} likes'
            bold: True 

        MyLabel:
            markup: True
            text: f'[b]{root.username}[/b] {root.caption}'   

        HalfOpacityLabel:
            text: f'View all {root.comments} comments'
    

    MDBoxLayout:
        padding: 5, 0, 0, 0
        spacing: 2
        adaptive_height: True 

        FitImage:
            source: root.profile_pic
            size_hint: None, None
            size: 20, 20
            radius: [20, ]
        
        HalfOpacityLabel:
            text: 'Add a comment...'
    
    MDBoxLayout:
        padding: 9, 0, 0, 0
        spacing: 0
        adaptive_height: True 

        HalfOpacityLabel:
            font_size: 10
            text: f'{root.posted_ago} ago'




<MyLabel@MDLabel>
    adaptive_height: True
    font_size: 12

<HalfOpacityLabel@MyLabel>:
    theme_text_color: 'Custom'
    text_color: 0, 0, 0, 0.5

"""
)

class PostCard2(MDCard):
    profile_pic = StringProperty()
    avatar = StringProperty()
    username = StringProperty()
    post = StringProperty()
    caption = StringProperty()
    likes = StringProperty()
    posted_ago = StringProperty()
    comments = StringProperty()