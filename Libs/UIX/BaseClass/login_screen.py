from kivy.animation import Animation
from kivy.properties import ColorProperty
import json

from components.screen import PScreen
from components.toast import toast


class LoginScreen(PScreen):
    bg_color = ColorProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = self.theme_cls.primary_color
    
    def verify(self, username, password, filename='assets//Files//User.json'):
        with open(filename,'r') as file:
            file_data = json.load(file)
            for user in file_data["Users"]:
                if user['username'] == username:
                    if user['password'] == password:
                        self.username = user['username']
                        self.pin = user['pin']
                        Flag = "Verified"
                        break
                    else:
                        Flag = "Wrong Password"
                        break
                else:
                    Flag = "Unknown"
            return Flag

    def sign_in(self):
        username = self.ids.username.text
        password = self.ids.password.text
        if username == '' or password == '':
            Flag = "Empty"
        else:
            Flag = self.verify(username, password)
        if Flag == "Verified":
            self.active()
            self.manager.set_current("home")
            toast("Signed In successfully!")
        elif Flag == "Wrong Password":
            toast("Wrong Password. Please Try Again")
        elif Flag == "Unknown":
            toast("User Not Found")
        elif Flag == "Empty":
            toast("Please Enter all the Details")

    def active(self):
        data = {
            'username': self.username,
            'pin': self.pin
        }
        with open('assets//Files//Active_User.json', 'w') as file:
            json.dump(data, file, indent=4)
