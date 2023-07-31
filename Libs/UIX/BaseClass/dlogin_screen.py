from components.screen import PScreen
from components.toast import toast
import json

class DLoginScreen(PScreen):
    def __init__(self, **kwargs):
        try:
            with open('assets//Files//Active_User.json', 'r') as file:
                self.data = json.load(file)
        except:
            pass
        self.user = self.data['username']
        self.pin = self.data['pin']
        self.input_pin = ''
        super().__init__(**kwargs)
    
    def input(self, num):
        if num == 'b' and len(self.input_pin) > 0:
            self.input_pin = list(self.input_pin)
            self.input_pin.pop()
            self.input_pin = ''.join(self.input_pin)
            count = len(self.input_pin) + 1
            if count == 1:
                self.ids.one.icon = "checkbox-blank-circle-outline"
            elif count == 2:
                self.ids.two.icon = "checkbox-blank-circle-outline"
            elif count == 3:
                self.ids.three.icon = "checkbox-blank-circle-outline"
            elif count == 4:
                self.ids.four.icon = "checkbox-blank-circle-outline"
            elif count == 5:
                self.ids.five.icon = "checkbox-blank-circle-outline"
        elif num != 'b':
            if len(self.input_pin) < 4:
                self.input_pin += str(num)
                count = len(self.input_pin)
                if count == 1:
                    self.ids.one.icon = "checkbox-blank-circle"
                elif count == 2:
                    self.ids.two.icon = "checkbox-blank-circle"
                elif count == 3:
                    self.ids.three.icon = "checkbox-blank-circle"
                elif count == 4:
                    self.ids.four.icon = "checkbox-blank-circle"
            else:
                self.ids.five.icon = "checkbox-blank-circle"
                self.input_pin += str(num)
                self.verify()

    def verify(self):
        if self.input_pin == self.pin:
            self.manager.set_current('home')
        else:
            toast("Wrong pin, Try Again")
