from kivy.animation import Animation
from kivy.properties import DictProperty, ListProperty, StringProperty
from Libs.UIX.components.chat_bubble import ChatBubble

from components.boxlayout import PBoxLayout
from components.dialog import PDialog
from components.screen import PScreen
from components.toast import toast
from random import choice

import socket
import random
import json
from threading import Thread
from datetime import datetime

class ChatScreen(PScreen):
    user = DictProperty()
    title = StringProperty()
    chat_logs = ListProperty()
    num = str(choice([1,2,3,4,5,6,7,8]))
    chat_bg = f"assets/Images/Backgrounds/bg ({num}).jpg"

    def __init__(self, **kw):
        super().__init__(**kw)
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.node.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port_and_ip = ('192.168.1.6', 12345)
        print(f"[*] Connecting to {port_and_ip[0]}:{port_and_ip[1]}...")
        self.separator_token = "<SEP>"
        self.node.connect(port_and_ip)
        print(f"[+] Connected to {port_and_ip[0]}:{port_and_ip[1]}")
        with open("assets//Files//Active_User.json", 'r') as file:
            data = json.load(file)
        self.username = data['username']
        always_receive = Thread(target=self.receive)
        always_receive.daemon = True
        always_receive.start()

    def receive(self):
        while True:
            message = self.node.recv(1024).decode()
            message = message.split(',')
            time = message[0]
            name = message[1]
            text = message[2]
            raw_time = message[3]
            if name == self.user['name']:
                self.chat_logs.append(
                    {
                        "text": text,
                        "time": time,
                        "raw_time": raw_time,
                        "send_by_user": False,
                    }
                )
                with open(self.file_loc, 'r') as file:
                    self.messages = json.load(file)
                    self.messages[self.user['name']].append(
                        {
                            "message": text,
                            "time": time,
                            "send_by_user": "False",
                            "raw_time": raw_time,
                        }
                    )
                with open(self.file_loc, 'w') as file:
                    json.dump(self.messages, file, indent= 4)

    def send(self, text, vid=False, id=0):
        if not text:
            return

        date_now = datetime.now().strftime('%d %b %H:%M')
        raw_time = datetime.now().strftime('%d %b %H:%M:%S')

        if vid:
            self.chat_logs.append(
                {"text": text, "time": date_now, "raw_time": raw_time, "send_by_user": True, "video": True, "id": id, "pos_hint": {"right": 1}}
            )
        else:
            self.chat_logs.append(
                {"text": text, "time": date_now, "raw_time": raw_time, "send_by_user": True, "pos_hint": {"right": 1}}
            )
        
        to_send = f"{date_now},{self.username},{text},{raw_time}"
        self.node.send(to_send.encode())

        with open(self.file_loc, 'r') as file:
            self.messages = json.load(file)
            self.messages[self.user['name']].append(
                {
                    "message": text,
                    "time": date_now,
                    "send_by_user": "True",
                    "raw_time": raw_time,
                }
            )
        with open(self.file_loc, 'w') as file:
            json.dump(self.messages, file, indent= 4)

        self.scroll_to_bottom()
        self.ids.field.text = ""

    def show_user_info(self):
        PDialog(
            content=UserInfoDialogContent(
                title=self.user["name"],
                image=self.user["image"]
            )
        ).open()

    def get_message(self):
        name = self.user['name']
        self.file_loc = f"assets//Files//Chat//Chats//{name}.json"
        with open(self.file_loc, 'r') as file:
            data = json.load(file)
            messages = data[name]
        for message in messages:
            if message['send_by_user'] == "False":
                send = False
                self.chat_logs.append(
                    {
                        "text": message['message'],
                        "time": message['time'],
                        "raw_time": message['raw_time'],
                        "send_by_user": send,
                    }
                )
            else:
                send = True
                self.chat_logs.append(
                    {
                        "text": message['message'],
                        "time": message['time'],
                        "raw_time": message['raw_time'],
                        "send_by_user": send,
                        "pos_hint": {"right": 1}
                    }
            )
        self.scroll_to_bottom()

    def share_video(self, username, id):
        text = f"Watch this awesome video by {username}  (¬‿¬)"
        self.send(text, vid=True, id=id)

    def scroll_to_bottom(self):
        rv = self.ids.chat_rv
        box = self.ids.box
        if rv.height < box.height:
            Animation.cancel_all(rv, "scroll_y")
            Animation(scroll_y=0, t="out_quad", d=0.5).start(rv)

    def delete(self):
        for rt in ChatBubble.selected:
            for message in self.chat_logs:
                if message['raw_time'] == rt:
                    self.chat_logs.remove(message)
        #DELETE FROM JSON FILE
        name = self.user['name']
        self.file_loc = f"assets//Files//Chat//Chats//{name}.json"
        with open(self.file_loc, 'r') as file:
            data = json.load(file)
        for rt in ChatBubble.selected:
            for message in data[name]:
                if message['raw_time'] == rt:
                    data[name].remove(message)
        with open(self.file_loc, 'w') as file:
            json.dump(data, file, indent = 4)
        toast(f"{len(ChatBubble.selected)} messages deleted")

    def deselect(self):
        pass

class UserInfoDialogContent(PBoxLayout):
    title = StringProperty()
    image = StringProperty()

    def view_profile(self):
        data = {
            "name": self.title
        }
        with open("assets//Files//Other_User.json", 'w') as file:
            json.dump(data, file, indent=4)
