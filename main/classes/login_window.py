from api.pl_api import *
from api.db_api import *

from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition


class LoginWindow(Screen):
    def log_in(self):
        username = self.ids.login.text
        password = self.ids.password.text
        # Trying to get data from fantasy premier league API. Cannot login if there is no data
        pl.get_data()
        if pl.connection == False:
            self.ids.info.text = 'Please make sure you\'re connected to the internet. Then try again.'
        else:
            try:
                app = MDApp.get_running_app()
                app.access_token, app.refresh_token, app.user_id = login(username, password)
                self.manager.transition = NoTransition()
                self.manager.current = 'MainWindow'
            except requests.exceptions.ConnectionError:
                # If pl.connection returns true then device is connected to the internet. 
                # This means there is problem on our end (e.g. server not running)
                self.ids.info.text = "There is a problem on our end. We are trying to fix it..."
            except ValueError:
                if login(username, password) == "User not found":
                    self.ids.login.helper_text = "User not found"
                    self.ids.login.error = True
                elif login(username, password) == "Wrong password":
                    self.ids.password.helper_text = "Wrong password"
                    self.ids.password.error = True
        
    def password(self):
        if self.ids.password.password == True:
            self.ids.password.password = False
            self.ids.password.icon_left = "eye"
            Clock.schedule_once(self.focus, 0.05)
        else:
            self.ids.password.password = True
            self.ids.password.icon_left = "eye-off"
            Clock.schedule_once(self.focus, 0.05)
    
    def focus(self, dt):
        self.ids.password.focus = True