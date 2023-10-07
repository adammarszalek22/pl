from api.pl_api import *
from api.db_api import *

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import Screen
from kivy.clock import mainthread

from threading import Thread

class DialogContent(MDBoxLayout):
    pass

class ViewOtherScoreWindow(Screen):
    dialog = None

    def open_dialog(self):

        # Opens dialog where user enters the username of the person whose scores they want to see
        app = MDApp.get_running_app()
        if not self.dialog:
            okay_button = MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                    )
            cancel_button = MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color
                    )
            self.dialog = MDDialog(
                title="Enter username",
                type='custom',
                content_cls = DialogContent(),
                buttons=[
                    okay_button,
                    cancel_button
                ]
            )
            okay_button.bind(on_release=self.stats)
            cancel_button.bind(on_release=self.exit_dialog)
            
        self.dialog.open()

    @mainthread
    def exit_dialog(self, instance):

        self.dialog.content_cls.children[0].text = ''
        self.dialog.dismiss()

    def stats(self, instance):

        thread = Thread(target = self.stats2)
        thread.start()

    def stats2(self):

        app = MDApp.get_running_app()
        self.username = self.dialog.content_cls.children[0].text
        user_info = get_by_username(app.access_token, self.username)

        if user_info["status_code"] == 200 and "username" in user_info.keys():
            self.exit_dialog(self)
            self.ids.username.text = str(user_info["username"])
            self.ids.position.text = str(user_info["position"])
            self.ids.points2.text = str(user_info["points"])
            self.ids.three_pointers.text = str(user_info["three_pointers"])
            self.ids.one_pointers.text = str(user_info["one_pointers"])
        else:
            self.dialog.content_cls.children[0].error = True