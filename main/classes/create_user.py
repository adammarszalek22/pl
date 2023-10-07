from api.pl_api import *
from api.db_api import create_user, login

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock, mainthread
from threading import Thread
from functools import partial

class CreateUser(Screen):

    def do_create_user(self):

        # clearing previous error messages, if any
        self.ids.info.text = ''

        # starting the spinner which will stop once the login is successful (or not)
        self.ids.spinner.active = True

        # using a different thread for creating the user (otherwise the spinner doesn't work)
        thread = Thread(target=self.create_the_user)
        thread.start()

    def create_the_user(self):

        app = MDApp.get_running_app()

        username = self.ids.login.text
        password = self.ids.password.text
        password2 = self.ids.password2.text

        if not pl.connection:
            # Trying to get data from fantasy premier league API. Cannot create user/login if there is no data.
            pl.get_data()
            if not pl.connection:
                self.ids.info.text = 'Please make sure you\'re connected to the internet. Then try again.'
                self.is_thread_finished = 2

        try:

            new_user = create_user(username, password, password2)
            status_code = new_user["status_code"]

            if status_code == 201:
                login_details = login(username, password)
                # saving details to the app that will be needed for calling other functions
                app.access_token = login_details["access_token"]
                app.refresh_token = login_details["refresh_token"]
                app.user_id = login_details["user_id"]
                # proceed to the app
                self.change_screen()
            elif status_code == 401:
                self.ids.password2.error = True
            else:
                self.ids.login.error = True

        except requests.exceptions.ConnectionError:
            # Same as in login window. If this error comes up then internet works fine 
            # but there's another problem (probably server not working)
            self.ids.info.text = "There is a problem on our end. We are working hard to fix it"

        except json.decoder.JSONDecodeError:
            self.ids.info.text = 'Unknown error'
            
        self.ids.spinner.active = False

    @mainthread
    def change_screen(self):
        
        self.manager.current = 'MainWindow'

    def password(self, textfield):

        icon_names = {
            'eye': 'eye-off',
            'eye-off': 'eye'
        }

        # showing or hiding the password and changing the icon
        textfield.password = not textfield.password
        textfield.icon_left = icon_names[textfield.icon_left]
        # the textfield loses focus after the above lines so restoring it
        Clock.schedule_once(partial(self.focus, textfield), 0.05)
    
    def focus(self, textfield, dt):

        textfield.focus = True
    
    def do_they_match(self, password1, password2):

        # show error message after both passwords have been entered and they do not match
        if not password2.focus and password1.text != password2.text:
            password2.error = True