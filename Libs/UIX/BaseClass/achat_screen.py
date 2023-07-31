import json

from kivy.properties import ListProperty

from components.boxlayout import PBoxLayout
from components.dialog import PDialog
from components.screen import PScreen


class AChatScreen(PScreen):

    chats = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open("assets//Files//Chat//Chats.json") as f:
            self.data = json.load(f)

        for chat in self.data:
            user_data = {
                "text": chat,
                "secondary_text": self.data[chat]["message"],
                "time": self.data[chat]["time"],
                "image": self.data[chat]["image"],
                "unread_messages": self.data[chat]["unread_messages"],
                "on_release": lambda x={
                    "name": chat,
                    **self.data[chat],
                }: self.goto_chat_screen(x),
            }
            self.chats.append(user_data)

    def goto_chat_screen(self, user):
        self.manager.set_current("chat")
        chat_screen = self.manager.get_screen("chat")
        chat_screen.user = user
        chat_screen.chat_logs = []
        chat_screen.title = user["name"]
        chat_screen.get_message()

    def show_menu(self):
        PDialog(content=MenuDialogContent()).open()


class MenuDialogContent(PBoxLayout):
    pass