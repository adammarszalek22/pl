from api.pl_api import *
from api.db_api import *

from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition


class CreateUser(Screen):
    def create_user_app(self):
        username = self.ids.login.text
        password = self.ids.password.text
        password2 = self.ids.password2.text
        pl.get_data()
        try:
            if pl.connection == False:
                self.ids.info.text = 'Please make sure you\'re connected to the internet. Then try again.'
            elif password == password2 and\
                create_user(username, password)["code"] == 201 and\
                pl.connection == True:
                app = MDApp.get_running_app()
                app.access_token, app.refresh_token, app.user_id = login(username, password)
                self.manager.current = 'MainWindow'
            elif password != password2:
                self.ids.password2.helper_text = "Passwords don't match."
                self.ids.password2.error = True
            else:
                self.ids.login.helper_text = 'User already exists.'
                self.ids.login.error = True
        except requests.exceptions.ConnectionError:
            self.ids.info.text = "There is a problem on our end. We are working hard to fix it"

    def password(self):
        if self.ids.password.password == True:
            self.ids.password.password = False
            self.ids.password.icon_left = "eye"
            Clock.schedule_once(self.focus1, 0.05)
        else:
            self.ids.password.password = True
            self.ids.password.icon_left = "eye-off"
            Clock.schedule_once(self.focus1, 0.05)
    
    def focus1(self, dt):
        self.ids.password.focus = True
    
    def password2(self):
        if self.ids.password2.password == True:
            self.ids.password2.password = False
            self.ids.password2.icon_left = "eye"
            Clock.schedule_once(self.focus2, 0.05)
        else:
            self.ids.password2.password = True
            self.ids.password2.icon_left = "eye-off"
            Clock.schedule_once(self.focus2, 0.05)
    
    def focus2(self, dt):
        self.ids.password2.focus = True