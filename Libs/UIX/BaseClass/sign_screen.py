from kivy.animation import Animation
from kivy.properties import ColorProperty
import json
from components.screen import PScreen
from components.toast import toast


class SignScreen(PScreen):
    bg_color = ColorProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = self.theme_cls.primary_color

    def write_json(self, new_data, username, filename='assets//Files//User.json'):
        with open(filename,'r+') as file:
            file_data = json.load(file)
            for user in file_data["Users"]:
                if user["username"] == username:
                    toast("Username already exists")
                    Flag = False
                    return Flag
            file_data["Users"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
            Flag = True
            return Flag

    def sign_in(self):
        self.username = self.ids.username.text
        self.password = self.ids.password.text
        self.pin = self.ids.pin.text
        try:
            email = self.manager.get_screen("email_signup").ids.email.text
            flag = True
        except:
            mobile = self.manager.get_screen("mobile_signup").ids.mobile.text
            flag = False
        if self.username == '' or self.password == '' or self.pin == '':
            toast("Please Enter all the Details")
        elif len(str(self.pin)) != 5:
            toast("Pin should be 5 digits long")
        else:
            if flag == True:
                data = {'username': self.username,
                        'password': self.password,
                        'pin': self.pin,
                        'email': email,
                        'mobile no.': None}
            else:
                data = {'username': self.username,
                        'password': self.password,
                        'pin': self.pin,
                        'email': None,
                        'mobile no.': mobile}
            Flag = self.write_json(data, self.username)
            if Flag == True:
                self.active()
                self.details()
                self.follow()
                self.manager.set_current("profile")
                toast("Welcome to Meraki :D")

    def active(self):
        data = {
            'username': self.username,
            'pin': self.pin
        }
        with open('assets//Files//Active_User.json', 'w') as file:
            json.dump(data, file, indent=4)

    def details(self):
        data = {
            'username': self.username,
            'profile_pic': 'assets//Images//logo.png',
            'bio': 'Hi! Welcome to Meraki :D',
            'link': 'link'
        }
        self.write_json(data, self.username, filename="assets//Files//User_Details.json")

    def follow(self):
        with open("assets//Files//Following.json", 'r') as file:
            following = json.load(file)
        following.update({self.username : []})
        with open("assets//Files//Following.json", 'w') as file:
            json.dump(following, file, indent = 4)