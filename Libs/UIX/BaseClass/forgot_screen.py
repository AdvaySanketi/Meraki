from kivy.animation import Animation
from kivy.properties import ColorProperty
import json
from components.screen import PScreen
from components.toast import toast

password = ''

class ForgotScreen(PScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def verify(self, username, pin, filename='assets//Files//User.json'):
        global password
        with open(filename,'r') as file:
            file_data = json.load(file)
            for user in file_data["Users"]:
                if user['username'] == username:
                    if user['pin'] == pin:
                        Flag = "Verified"
                        password = user['password']
                        break
                    else:
                        Flag = "Wrong Pin"
                        break
                else:
                    Flag = "Unknown"
            return Flag

    def forget(self):
        global password
        username = self.ids.username.text
        pin = self.ids.pin.text
        if username == '' or pin == '':
            Flag = "Empty"
        else:
            Flag = self.verify(username, pin)
        if Flag == "Verified":
            self.manager.set_current("login")
            toast(f"Your Password is {password}")
        elif Flag == "Wrong pin":
            toast("Wrong pin. Please Try Again")
        elif Flag == "Unknown":
            toast("User Not Found")
        elif Flag == "Empty":
            toast("Please Enter all the Details")
