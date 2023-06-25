from api.pl_api import *
from api.db_api import *

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition


class CreateLeagueContent(MDBoxLayout):
    pass


class SuccessContent(MDBoxLayout):
    group_id =  StringProperty()


class GroupsWindow(Screen):
    dialog = None
    success_dialog = None

    def open_dialog(self):
        # Opens dialog where user enters the new league/group name
        app = MDApp.get_running_app()
        if not self.dialog:
            create_button = MDFlatButton(
                        text="CREATE",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                    )
            cancel_button = MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color
                    )
            self.dialog = MDDialog(
                title="Name your league",
                type='custom',
                content_cls = CreateLeagueContent(),
                buttons=[
                    create_button,
                    cancel_button
                ]
            )
            create_button.bind(on_release=self.create_league)
            cancel_button.bind(on_release=self.exit_dialog)
        self.dialog.open()

    def create_league(self, instance):
        # Creates the new league in the database
        app = MDApp.get_running_app()
        self._name = self.dialog.content_cls.children[0]
        new_group = create_group(app.access_token, self._name.text)
        try:
            SuccessContent.group_id = str(new_group["id"]) # group_id to be returned to user
            self.dialog.dismiss()
            self.open_success_dialog()
            self._name.text = ''
        except KeyError:
            self._name.helper_text = "A group with that name already exists"
            self._name.error = True

    def exit_dialog(self, instance):
        self.dialog.content_cls.children[0].text = ''
        self.dialog.dismiss()
    
    def open_success_dialog(self):
        # Message that pops up when league is created successfully
        app = MDApp.get_running_app()
        if not self.success_dialog:
            okay_button = MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                    )
            self.success_dialog = MDDialog(
                title="DONE",
                type='custom',
                content_cls = SuccessContent(),
                buttons=[
                    okay_button
                ]
            )
            okay_button.bind(on_release=self.success_dialog.dismiss)
        self.success_dialog.open()