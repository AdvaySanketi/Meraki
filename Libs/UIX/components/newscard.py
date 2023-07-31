from kivymd.uix.card import MDCard
from kivy.lang.builder import Builder
from kivy.properties import DictProperty, StringProperty, NumericProperty

Builder.load_string("""
<NewsCard>:
    app: app
    size_hint_y: None
    height: '100dp'
    width: '100dp'
    elevation: 0
    md_bg_color: [0, 0, 0, 1]
    radius: '10dp', 
    font_size: '15sp'
    ripple_behavior: False
    MDFloatLayout:
        md_bg_color: 0,0,0,1
        Label:
            text: root.title
            font_size: "18sp"
            text_size : self.size
            halign : "center"
            valign : "center"
            size_hint: .2, .2
            pos_hint:{"center_x": .3, "center_y": .8}
"""
)

class NewsCard(MDCard):

    title = StringProperty("test")
    def __init__(self, **kwargs):
        print(self.title)
        super().__init__(**kwargs)

