from api.pl_api import *
from api.db_api import *

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

class ViewScoreWindow(Screen):

    def scores(self):
        
        app = MDApp.get_running_app()
        user_info = my_user_info(app.access_token, app.user_id)
        self.ids.username.text = str(user_info["username"])
        self.ids.position.text = str(user_info["position"])
        self.ids.points2.text = str(user_info["points"])
        self.ids.three_pointers.text = str(user_info["three_pointers"])
        self.ids.one_pointers.text = str(user_info["one_pointers"])