from kivy.properties import ObjectProperty, ListProperty
from components.screen import PScreen
from components.toast import toast
from components.boxlayout import PBoxLayout
from components.dialog import PDialog
import json
import webbrowser
from kivymd.uix.filemanager import MDFileManager
from kivy.utils import platform

class ProfileScreen(PScreen):

    posts = ListProperty()
    post_grid = ObjectProperty()

    def __init__(self, **kwargs):
        with open('assets//Files//Active_User.json', 'r') as file:
            self.data = json.load(file)
        self.username = self.data['username']
        with open('assets//Files//User_Details.json', 'r') as file:
            self.data = json.load(file)
            for data in self.data['Users']:
                if data['username'] == self.username:
                    self.bio_text = data['bio']
                    self.link_txt = data['link']
                    self.dp = data['profile_pic']

        self.file_manager = MDFileManager(
            select_path = self.select_path,
            exit_manager = self.exit_manager
        )
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        self.__init__()
        self.posts = []
        with open('assets//Files//Videos.json', 'r') as file:
            self.videos = json.load(file)
        for video in self.videos['videos']:
            post = {'id':"",'source':"",'thumbnail':""}
            if video['name'] == self.username:
                post['id'] = video['id']
                post['source'] = video['video']
                post['thumbnail'] = video['thumbnail']
                self.posts.append(post)
        return super().on_pre_enter(*args)

    def open_file_manager(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.INTERNET,
            ])

        self.file_manager.show('/')
    
    def select_path(self, path):
        self.ids.dp.icon = path
        with open('assets//Files//User_Details.json', 'r') as file:
            details = json.load(file)
            for user in details['Users']:
                if user['username'] == self.username:
                    user['profile_pic'] = path

        with open('assets//Files//User_Details.json', 'w') as file:
            json.dump(details, file, indent=4)
        toast("Profile Photo Changed Successfully")
        self.exit_manager(path)
    
    def exit_manager(self, path):
        self.file_manager.close()

    def edit(self):
        PDialog(content=EditDialogContent()).open()

    def open_url(self):
        with open('assets//Files//User_Details.json', 'r') as file:
            data = json.load(file)
            for user in data['Users']:
                if user['username'] == self.username:
                    url = user['link']

        if url == "link":
            toast("User has not set up any Link yet")
        else:
            if platform == "android":
                from jnius import autoclass, cast
                Intent = autoclass("android.content.Intent")
                Uri = autoclass("android.net.Uri")
                PythonActivity = autoclass("org.kivy.android.PythonActivity")

                i = Intent(Intent.ACTION_VIEW)
                i.setData(Uri.parse(url))

                current_activity = cast('android.app.Activity', PythonActivity.mActivity)
                current_activity.startActivity(i)
            else:
                webbrowser.open(url)
                

class EditDialogContent(PBoxLayout):
    def account(self):
        PDialog(content=AccountDialogContent()).open()
    def bio(self):
        PDialog(content=BioDialogContent()).open()
    def link(self):
        PDialog(content=LinkDialogContent()).open()

class AccountDialogContent(PBoxLayout):
    def check(self):
        uname = self.ids.username.text
        if uname != '' and uname.startswith('@'):
            with open('assets//Files//Active_User.json', 'r') as file:
                data = json.load(file)
                username = data["username"]
                pin = data['pin']
                data = {
                    "username": uname,
                    "pin": pin
                }

            with open('assets//Files//Active_User.json', 'w') as file:
                json.dump(data, file, indent=4)
            
            with open('assets//Files//User_Details.json', 'r') as file:
                details = json.load(file)
                for user in details['Users']:
                    if user['username'] == self.username:
                        user['username'] = uname

            with open('assets//Files//User_Details.json', 'w') as file:
                json.dump(details, file, indent=4)

            with open('assets//Files//User.json', 'r') as file:
                users = json.load(file)
                for user in users['Users']:
                    if user['username'] == username:
                        user['username'] = uname
            
            with open('assets//Files//User.json', 'w') as file:
                json.dump(users, file, indent=4)

            self.back()
            toast("Your Changes will be reflected Shortly :D")
        else:
            toast("Please enter a Valid Username")
        
    def back(self):
        PDialog(content=EditDialogContent()).open()

class BioDialogContent(PBoxLayout):
    def check(self):
        bio = self.ids.bio.text
        if len(bio) <= 75:
            with open('assets//Files//User_Details.json', 'r') as file:
                details = json.load(file)
                for user in details['Users']:
                    if user['username'] == self.username:
                        user['bio'] = bio

            with open('assets//Files//User_Details.json', 'w') as file:
                json.dump(details, file, indent=4)
            
            self.back()
            toast("Your Changes will be reflected Shortly :D")
        elif bio == '':
            toast("Please Enter a Valid Bio")
        else:
            toast("Your Bio is Longer than 75 Characters")

    def back(self):
        PDialog(content=EditDialogContent()).open()

class LinkDialogContent(PBoxLayout):
    def check(self):
        link = self.ids.link.text
        if link != '':
            with open('assets//Files//User_Details.json', 'r') as file:
                details = json.load(file)
                for user in details['Users']:
                    if user['username'] == self.username:
                        user['link'] = link

            with open('assets//Files//User_Details.json', 'w') as file:
                json.dump(details, file, indent=4)
            self.back()
            toast("Your Changes will be reflected Shortly :D")
        else:
            toast("Please enter a Valid Link")

    def back(self):
        PDialog(content=EditDialogContent()).open()
