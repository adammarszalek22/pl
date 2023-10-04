from api.pl_api import *
from api.db_api import *

from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from threading import Thread


class CreateUser(Screen):
    is_thread_finished = 0

    def do_create_user(self):
        
        # Creating a new thread for the create_user_app function so that the spinner can be started
        # Once create_user_app function is finished, is_thread_finished will be set to 1
        # And then change_screen function will take effect
        # This makes it much smoother than using the Clock.schedule_once() function on its own
        self.ids.spinner.active = True
        thread = Thread(target=self.create_user_app)
        thread.start()
        Clock.schedule_once(self.change_screen, 0.01)

    def create_user_app(self):

        self.ids.info.text = ''
        username = self.ids.login.text
        password = self.ids.password.text
        password2 = self.ids.password2.text
        # Trying to get data from fantasy premier league API. Cannot login if there is no data
        pl.get_data()
        if pl.connection == True:
            try:
                new_user = create_user(username, password, password2)
                code = new_user["code"]
                if code == 201:
                    app = MDApp.get_running_app()
                    login_details = login(username, password)
                    app.access_token = login_details["access_token"]
                    app.refresh_token = login_details["refresh_token"]
                    app.user_id = login_details["user_id"]
                    self.is_thread_finished = 1 # go to next screen
                elif code == 401:
                    self.ids.password2.error = True
                    self.is_thread_finished = 2 # stay in the current screen
                else:
                    self.ids.login.helper_text = 'User already exists.'
                    self.ids.login.error = True
                    self.is_thread_finished = 2 # stay in the current screen
            except requests.exceptions.ConnectionError:
                # Same as in login window. If this error comes up then internet works fine 
                # but there's another problem (probably server not working)
                self.ids.info.text = "There is a problem on our end. We are working hard to fix it"
                self.is_thread_finished = 2
            except json.decoder.JSONDecodeError:
                self.ids.info.text = 'Unknown error'
                self.is_thread_finished = 2
        else:
            self.ids.info.text = 'Please make sure you\'re connected to the internet. Then try again.'
            self.is_thread_finished = 2


    def change_screen(self, dt):

        if self.is_thread_finished == 1:
            self.manager.get_screen('MainWindow').bets()
            self.manager.get_screen('MainWindow').pl_table()
            self.manager.get_screen('MainWindow').users_table()
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