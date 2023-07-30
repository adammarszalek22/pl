from api.pl_api import *
from api.db_api import *

from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
from threading import Thread


class LoginWindow(Screen):
    is_thread_finished = 0

    def do_log_in(self):

        # Creating a new thread for the log_in function so that the spinner can be started
        # Once log_in function is finished, is_thread_finished will be set to 1
        # And then change_screen function will take effect
        # This makes it much smoother than using the Clock.schedule_once() function on its own
        self.ids.spinner.active = True
        thread = Thread(target=self.log_in)
        thread.start()
        Clock.schedule_once(self.change_screen, 0.01)

    def log_in(self):

        self.ids.info.text = ''
        username = self.ids.login.text
        password = self.ids.password.text
        # Trying to get data from fantasy premier league API. Cannot login if there is no data
        pl.get_data()
        if pl.connection == True:
            try:
                app = MDApp.get_running_app()
                login_details = login(username, password)
                code = login_details["code"]
                if code == 200:
                    app.access_token = login_details["access_token"]
                    app.refresh_token = login_details["refresh_token"]
                    app.user_id = login_details["user_id"]
                    self.is_thread_finished = 1
                elif code == 401:
                    message = login_details["message"]
                    if message == "User not found":
                        self.ids.login.helper_text = "User not found"
                        self.ids.login.error = True
                    elif message == "Wrong password":
                        self.ids.password.helper_text = "Wrong password"
                        self.ids.password.error = True
                    self.is_thread_finished = 2
            except requests.exceptions.ConnectionError:
                # If pl.connection returns true then device is connected to the internet. 
                # This means there is problem on our end (e.g. server not running)
                self.ids.info.text = "There is a problem on our end. We are trying to fix it..."
                self.is_thread_finished = 2
            except json.decoder.JSONDecodeError:
                self.ids.info.text = 'Unknown error'
                self.is_thread_finished = 2
        else:
            self.ids.info.text = 'Please make sure you\'re connected to the internet. Then try again.'
            self.is_thread_finished = 2
            
                
    
    def change_screen(self, dt):

        if self.is_thread_finished == 1:
            self.manager.transition = NoTransition()
            self.manager.current = 'MainWindow'
            self.ids.spinner.active = False
            self.is_thread_finished = 0
        elif self.is_thread_finished == 2:
            self.ids.spinner.active = False
            self.is_thread_finished = 0
        else:
            Clock.schedule_once(self.change_screen, 0.01)
        
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