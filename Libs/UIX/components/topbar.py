from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang.builder import Builder

Builder.load_string("""
#:import hex kivy.utils.get_color_from_hex

<TopBarMenu>:
    size_hint_y: None
    height: '50dp' 
    spacing: '70dp'
    padding: '20dp', '15dp', '20dp', 0
    MDIconButton:   
        icon: 'arrow-left'
        pos_hint: {'center_x':.1,'center_y':.5}
        theme_icon_color: "Custom"
        icon_color: hex("#FEE715FF")
        md_bg_color: hex("#000000")
        icon_size: "30sp"
        ripple_scale: 0
        on_release:
            if app.root.has_screen("music_player"): app.root.get_screen("music_player").play()
            app.root.set_current("home", side = 'left')

    PLabel:
        text: "Music"
        font_name: "assets\\Fonts\\Vegan.ttf"
        font_size: "22sp"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
            
    MDIconButton:
        icon: 'magnify'
        pos_hint: {'center_x':.1, 'center_y':.5}
        theme_icon_color: "Custom"
        icon_color: hex("#FEE715FF")
        md_bg_color: hex("#000000")
        icon_size: "30sp"
        ripple_scale: 0
        on_release:
            app.root.set_current("search")

<TopBarBack>:
    padding: '10dp', '5dp', 0, 0
    size_hint_y: None
    height: '50dp' 
    spacing: '50dp'
    MDIconButton:   
        icon: 'chevron-left'
        padding: 0    
    SearchFieldHalf:

<TopBarSelected>:
    padding: '10dp', '5dp', 0, 0
    size_hint_y: None
    height: '50dp' 
    spacing: '10dp'
    selected: '0'
    MDIconButton:   
        icon: 'chevron-left'
        padding: 0
    
    MDLabel: 
        text: "{0} selected item".format(root.selected)
        halign: 'center'
        bold: True
    
    MDCheckbox:
        size_hint: None, None
        size: '40dp', '40dp'
        group: 'selection'
"""
)


class TopBarMenu(MDBoxLayout):
    pass


class TopBarBack(MDBoxLayout):
    pass

class TopBarSelected(MDBoxLayout):
    pass