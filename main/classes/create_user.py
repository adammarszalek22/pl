from api.pl_api import *
from api.db_api import *

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock, mainthread
from threading import Thread

class CreateUser(Screen):

    def do_create_user(self):
        
        self.ids.info.text = ''

        # using threading to allow the spinner to work
        self.ids.spinner.active = True

        thread = Thread(target=self.create_the_user)
        thread.start()

    def create_the_user(self):

        app = MDApp.get_running_app()

        username = self.ids.login.text
        password = self.ids.password.text
        password2 = self.ids.password2.text

        # Trying to get data from fantasy premier league API. Cannot login if there is no data
        pl.get_data()

        if not pl.connection:
            self.ids.info.text = 'Please make sure you\'re connected to the internet. Then try again.'
            self.is_thread_finished = 2

        try:
            new_user = create_user(username, password, password2)
            status_code = new_user["status_code"]
            if status_code == 201:
                login_details = login(username, password)
                app.access_token = login_details["access_token"]
                app.refresh_token = login_details["refresh_token"]
                app.user_id = login_details["user_id"]
                self.change_screen()
            elif status_code == 401:
                self.ids.password2.error = True
                self.ids.spinner.active = False
            else:
                self.ids.login.helper_text = 'User already exists.'
                self.ids.login.error = True
                self.ids.spinner.active = False
        except requests.exceptions.ConnectionError:
            # Same as in login window. If this error comes up then internet works fine 
            # but there's another problem (probably server not working)
            self.ids.info.text = "There is a problem on our end. We are working hard to fix it"
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
    
    def do_they_match(self, instance):

        password = self.ids.password.text
        password2 = self.ids.password2.text
        if instance.focus == False and password != password2:
            self.ids.password2.error = True