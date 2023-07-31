from kivy.properties import ObjectProperty, ListProperty
from components.screen import PScreen
from components.toast import toast
from components.boxlayout import PBoxLayout
from components.dialog import PDialog
import json
import webbrowser

class OtherProfileScreen(PScreen):

    posts = ListProperty()
    post_grid = ObjectProperty()

    def __init__(self, **kwargs):
        with open('assets//Files//Other_User.json', 'r') as file:
            self.data = json.load(file)
        self.username = self.data['name']
        with open('assets//Files//User_Details.json', 'r') as file:
            self.data = json.load(file)
            for data in self.data['Users']:
                if data['username'] == self.username:
                    self.bio_text = data['bio']
                    self.link_txt = data['link']
                    self.dp = data['profile_pic']
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
        
        self.check_follow()
        
        return super().on_pre_enter(*args)

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

    def menu(self):
        PDialog(content=EditDialogContent()).open()

    def follow(self):
        data = {
            'username' : self.username,
            'dp' : self.dp
        }
        with open("assets//Files//Active_User.json", 'r') as file:
            username = json.load(file)['username']
        with open("assets//Files//Following.json", 'r') as file:
            following = json.load(file)
        for follow in following:
            if follow == username:
                if data in following[follow]:
                    following[follow].remove(data)
                    self.ids.follow.text = "Follow"
                    toast("Unfollowed " + self.username + " Successfully")
                else:
                    following[follow].append(data)
                    self.ids.follow.text = "Unfollow"
                    toast("Followed " + self.username + " Successfully")
        with open("assets//Files//Following.json", 'w') as file:
            json.dump(following, file, indent = 4)

    def check_follow(self):
        data = {
            'username' : self.username,
            'dp' : self.dp
        }
        with open("assets//Files//Active_User.json", 'r') as file:
            username = json.load(file)['username']
        with open("assets//Files//Following.json", 'r') as file:
            following = json.load(file)
        for follow in following:
            if follow == username:
                if data in following[follow]:
                    self.ids.follow.text = "Unfollow"
                else:
                    self.ids.follow.text = "Follow"

class EditDialogContent(PBoxLayout):
    pass

