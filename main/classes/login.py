from api.pl_api import *
from api.db_api import *

from kivymd.app import MDApp
from kivy.clock import Clock, mainthread
from kivy.uix.screenmanager import Screen
from threading import Thread


class LoginWindow(Screen):

    def do_log_in(self):
        
        self.ids.info.text = ''

        # using threading to allow the spinner to work
        self.ids.spinner.active = True

        thread = Thread(target=self.log_in)
        thread.start()
        
    def log_in(self):
            
        app = MDApp.get_running_app()

        username = self.ids.login.text
        password = self.ids.password.text

        # Trying to get data from fantasy premier league API. Cannot login if there is no data
        pl.get_data()
        if not pl.connection:
            self.ids.info.text = 'Please make sure you\'re connected to the internet. Then try again.'
            self.ids.spinner.active = False

        try:
            login_details = login(username, password)
            status_code = login_details["status_code"]
            if status_code == 200:
                app.access_token = login_details["access_token"]
                app.refresh_token = login_details["refresh_token"]
                app.user_id = login_details["user_id"]
                self.change_screen()
            elif status_code == 401:
                message = login_details["message"]
                if message == "User not found":
                    self.ids.login.error = True
                elif message == "Wrong password":
                    self.ids.password.error = True
                self.ids.spinner.active = False
        except requests.exceptions.ConnectionError:
            # If pl.connection returns true then device is connected to the internet. 
            # This means there is problem on our end (e.g. server not running)
            self.ids.info.text = "There is a problem on our end. We are trying to fix it..."
            self.ids.spinner.active = False
        except json.decoder.JSONDecodeError:
            self.ids.info.text = 'Unknown error'
            self.ids.spinner.active = False
            
                
    @mainthread
    def change_screen(self):

        # self.manager.get_screen('MainWindow').show_gameweek_games()
        # self.manager.get_screen('MainWindow').pl_table()
        # self.manager.get_screen('MainWindow').users_table()
        self.manager.current = 'MainWindow'
        self.ids.spinner.active = False
        
    def password(self):
        # changes icon of the textfield and shows/hides the password

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