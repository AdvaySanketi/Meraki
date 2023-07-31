import webbrowser
from kivymd.uix.card import MDCard
from kivy.lang.builder import Builder
from kivy.utils import platform
from kivy.properties import DictProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.modalview import ModalView

Builder.load_string("""
#: import Window kivy.core.window.Window
#:import hex kivy.utils.get_color_from_hex

#region
<ArticleCard>:
    orientation: 'vertical'
    spacing: dp(4)
    size_hint: [None, None]
    height: dp(180) + title.height
    width: Window.width*.9
    BoxLayout:
        size_hint_y: .7
        RelativeLayout:
            AsyncImage:
                id: cover
                source: root.cover
                opacity: 0
            Widget:
                canvas.before:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        size: self.size[0], self.size[1]
                        pos: self.pos
                        radius: [self.height*.2]
                        texture: cover.texture

    BoxLayout:
        size_hint_y: None
        height: dp(28) + title.height
        orientation: "vertical"
        spacing: dp(4)
        Label:
            id: title
            text: root.title
            font_size: "16sp"
            font_name: "assets//Fonts//Poppins//Poppins-Regular.ttf"
            size_hint_y: None
            text_size: (Window.width*.9, None)
            size: self.texture_size
            color: [1,1,1,1]
        BoxLayout:
            size_hint_y: None
            height: dp(16)
            spacing: dp(8)
            Text:
                text: root.publisher
                font_size: "12sp"
                font_name: "assets//Fonts//Poppins//Poppins-Regular.ttf"
                color: [1,1,1,1]
            Label:
                text: root.date
                font_size: "12sp"
                font_name: "assets//Fonts//Poppins//Poppins-Regular.ttf"
                color: [1,1,1,1]
                halign: 'right'
                size_hint_x: .4
            
#endregion
<ArticleTile>:
    size_hint_y: None
    height: dp(42) + title.height
    padding: dp(4)
    spacing: dp(8)
    BoxLayout:
        size_hint_y: None
        spacing: dp(12)
        AnchorLayout:
            size_hint_x: None
            width: dp(42)
            pos_hint: {"center_y": .5} if len(root.title) < 115 else {"center_y": .7}
            BoxLayout:
                size_hint: [None, None]
                size: [dp(42), dp(42)]
                RelativeLayout:
                    AsyncImage:
                        id: cover
                        source: root.cover
                        opacity: 0
                    Widget:
                        canvas.before:
                            Color:
                                rgba: [1,1,1,1]
                            RoundedRectangle:
                                size: dp(70), dp(70)
                                pos: self.pos
                                radius: [self.height*.1]
                                texture: cover.texture
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(18) + title.height
            spacing: dp(4)
            Label:
                id: title
                text: root.title
                font_size: "16sp"
                font_name: "assets//Fonts//Poppins//Poppins-Regular.ttf"
                size_hint_y: None
                text_size: (Window.width*.6, None)
                size: self.texture_size
                color: [230/255,230/255,250/255]
            BoxLayout:
                size_hint_y: None
                height: dp(16)
                spacing: dp(8)
                Text:
                    text: root.date
                    font_size: "12sp"
                    font_name: "assets//Fonts//Poppins//Poppins-Regular.ttf"
                    color: [1,1,1,1]
                    halign: 'right'
                    size_hint_x: .4

<ArticleView>:
    background_color: [0,0,0,1]
    background: ""
    BoxLayout:
        orientation: "vertical"
        AnchorLayout:
            size_hint_y: None
            height: dp(54)
            padding: dp(12)
            anchor_x: "left"
            BoxLayout:
                size_hint_x: None
                width: self.height
                canvas.before:
                    Color:
                        rgba: [0,0,0,0]
                    RoundedRectangle:
                        size: self.size[0], self.size[1]
                        pos: self.pos
                        radius: [self.height*.15]
                MDFloatingActionButton:
                    icon: "chevron-left"
                    pos_hint: {"center_y": .5}
                    font_size: sp(40)
                    theme_icon_color: "Custom"
                    icon_color: hex("#FEE715FF")
                    md_bg_color: [0,0,0,0]
                    icon_size: "40sp"
                    ripple_scale: 0
                    on_release:
                        root.dismiss()
        BoxLayout:
            ScrollView:
                do_scroll: [False, True]
                size_hint_y: None
                height: self.parent.height
                GridLayout:
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(18)
                    padding: dp(18), dp(8)
                    ArticleCard:
                        id: art
                        clickable: False
                    Label:
                        id: content
                        text: root.content
                        font_size: "16sp"
                        font_name: "assets//Fonts//Poppins//Poppins-Regular.ttf"
                        size_hint_y: None
                        text_size: (Window.width*.9, None)
                        size: self.texture_size
                        color: [1,1,1,1]
                    AnchorLayout:
                        size_hint_y: None
                        anchor_x: 'center'
                        MDRoundFlatButton:
                            text: "Continue Reading..."
                            size_hint_y: None
                            height: dp(42)
                            padding: dp(18)
                            on_release:
                                root.open_link()
"""
)

class Article(BoxLayout, ButtonBehavior):
    title = StringProperty("")
    cover = StringProperty("")
    link = StringProperty("")
    author = StringProperty("")
    publisher = StringProperty("")
    content = StringProperty("")
    date = StringProperty("")
    clickable = BooleanProperty(True)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.view_article()
        return super().on_touch_up(touch)

    def view_article(self, *args):
        if self.clickable:
            av = ArticleView()
            av.content = self.content
            av.link = self.link

            art = av.ids.art
            art.title = self.title
            art.cover = self.cover
            art.publisher = self.publisher
            art.date = self.date

            av.open()

class ArticleCard(Article):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ArticleTile(Article):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ArticleView(ModalView):
    title = StringProperty("")
    cover = StringProperty("")
    link = StringProperty("")
    author = StringProperty("")
    publisher = StringProperty("")
    content = StringProperty("")
    date = StringProperty("")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def open_link(self):
        if platform == "android":
            from jnius import autoclass, cast
            Intent = autoclass("android.content.Intent")
            Uri = autoclass("android.net.Uri")
            PythonActivity = autoclass("org.kivy.android.PythonActivity")

            i = Intent(Intent.ACTION_VIEW)
            i.setData(Uri.parse(self.link))

            current_activity = cast('android.app.Activity', PythonActivity.mActivity)
            current_activity.startActivity(i)
        else:
            webbrowser.open(self.link)