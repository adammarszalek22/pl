from api.db_api import my_user_info

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from threading import Thread

class ViewScoreWindow(Screen):
    user_info = None

    def stats(self):
        
        thread = Thread(target = self.stats2)
        thread.start()

    def stats2(self):
        
        if not self.user_info:
            app = MDApp.get_running_app()
            self.user_info = my_user_info(app.access_token, app.user_id)
            self.ids.username.text = str(self.user_info["username"])
            self.ids.position.text = str(self.user_info["position"])
            self.ids.points2.text = str(self.user_info["points"])
            self.ids.three_pointers.text = str(self.user_info["three_pointers"])
            self.ids.one_pointers.text = str(self.user_info["one_pointers"])