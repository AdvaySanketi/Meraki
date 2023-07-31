from kivy.animation import Animation
from kivy.properties import ColorProperty
import os
import random
from twilio.rest import Client

from components.screen import PScreen
from components.toast import toast


class MSignScreen(PScreen):
    bg_color = ColorProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = self.theme_cls.primary_color

    def sign_up(self):
        mobile = self.ids.mobile.text
        otp = self.ids.otp.text
        if mobile == '':
            toast("Please Enter all the Details")
        elif otp == '':
            toast("Please enter OTP sent to your mobile number")
        else:
            self.manager.set_current("signup")
            toast("Please Fill in your Details to jump in!")
    
    def otp(self):
        mobile = self.ids.mobile.text
        otp = random.randint(9999,100000)
        account_sid = 'AC204391dad7aad719c6cf4505c0fc6311'
        auth_token = '2cbabd873517bb61a410ee2f0ecc0be6'

        client = Client(account_sid, auth_token)
        message = client.messages.create(
                body=f'''Welcome to Meraki
                Please enter the OTP - {otp} - to sign up to Meraki
                Thank You :D''',
                from_ = '+919679257467',
                to = '+91' + mobile
            )

        print(message.sid)
