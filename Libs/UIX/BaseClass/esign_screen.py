import smtplib
from email.message import EmailMessage
from kivy.animation import Animation
from kivy.properties import ColorProperty

from components.screen import PScreen
from components.toast import toast


class ESignScreen(PScreen):
    bg_color = ColorProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = self.theme_cls.primary_color

    def sign_up(self):
        email = self.ids.email.text
        otp = self.ids.otp.text
        if email == '':
            toast("Please Enter all the Details")
        elif otp == '':
            toast("Please enter OTP sent to your email")
        else:
            self.manager.set_current("signup")
            toast("Please Fill in your Details to jump in!")
    
    def otp(self):
        email = self.ids.email.text
        body = '''
        Hello, this is a test
        '''
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("asd.jade.007@gmail.com", "asdfghj209")
        s.sendmail('asd.jade.007@gmail.com',email,body)
        s.quit()

