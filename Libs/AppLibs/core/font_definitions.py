from kivy.core.text import LabelBase

fonts_path = "assets/Fonts/"

fonts = [
    {
        "name": "Lexend",
        "fn_regular": fonts_path + "Lexend-Regular.ttf",
        "fn_bold": fonts_path + "Lexend-Bold.ttf",
    },
    {
        "name": "LexendThin",
        "fn_regular": fonts_path + "Lexend-Thin.ttf",
    },
    {
        "name": "LexendLight",
        "fn_regular": fonts_path + "Lexend-Light.ttf",
    },
    {
        "name": "LexendMedium",
        "fn_regular": fonts_path + "Lexend-Medium.ttf",
    },
    {
        "name": "Abruptly",
        "fn_regular": fonts_path + "Abruptly.ttf",
    },
    {
        "name": "Flor",
        "fn_regular": fonts_path + "Flor.ttf",
    },
    {
        "name": "Honeybee",
        "fn_regular": fonts_path + "Honeybee.ttf",
    },
    {
        "name": "Library",
        "fn_regular": fonts_path + "Library.ttf",
    },
    {
        "name": "Vegan",
        "fn_regular": fonts_path + "Vegan.ttf",
    },
    {
        "name": "Poppins",
        "fn_regular": fonts_path + "Poppins/Poppins-Regular.ttf",
    },
    {
        "name": "PSBold",
        "fn_regular": fonts_path + "Poppins/Poppins-SemiBold.ttf",
    },
    {
        "name": "PBold",
        "fn_regular": fonts_path + "Poppins/Poppins-Bold.ttf",
    },
    {
        "name": "PEBold",
        "fn_regular": fonts_path + "Poppins/Poppins-ExtraBold.ttf",
    },
    {
        "name": "Icons",
        "fn_regular": fonts_path + "Feather.ttf",
    },
]


def register_fonts():
    for font in fonts:
        LabelBase.register(**font)
