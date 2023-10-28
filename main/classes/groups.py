from api.db_api import create_group, get_group_by_id, join_group

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen


class CreateLeagueContent(MDBoxLayout):
    pass 


class SuccessContent(MDBoxLayout):
    group_id = StringProperty()

class JoinLeagueContent(MDBoxLayout):
    pass

class SuccessJoinContent(MDBoxLayout):
    group_id = StringProperty()
    group_name = StringProperty()


class GroupsWindow(Screen):
    dialog = None
    success_dialog = None
    join_dialog = None
    join_success_dialog = None

    '''
    CREATE LEAGUE
    '''

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
    
    '''
    JOIN LEAGUE
    '''

    def open_dialog_join(self):
        # Opens dialog where user enters the league id
        app = MDApp.get_running_app()
        if not self.join_dialog:
            create_button = MDFlatButton(
                        text="JOIN",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                    )
            cancel_button = MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color
                    )
            self.join_dialog = MDDialog(
                title="Enter league ID",
                type='custom',
                content_cls = JoinLeagueContent(),
                buttons=[
                    create_button,
                    cancel_button
                ]
            )
            create_button.bind(on_release=self.join_league)
            cancel_button.bind(on_release=self.exit_dialog_join)
        self.join_dialog.open()
    
    def join_league(self, instance):
        # Creates the new league in the database
        app = MDApp.get_running_app()
        self.league_id = self.join_dialog.content_cls.children[0]
        dict = get_group_by_id(app.access_token, int(self.league_id.text))
        try:
            id = dict["id"]
            name = dict["name"]
            SuccessJoinContent.group_id = str(id)
            SuccessJoinContent.group_name = str(name)
            self.join_dialog.dismiss()
            self.open_join_success_dialog()
        except KeyError:
            self.league_id.helper_text = "Group does not exist"
            self.league_id.error = True

    def exit_dialog_join(self, instance):
        self.join_dialog.content_cls.children[0].text = ''
        self.join_dialog.dismiss()
    
    def open_join_success_dialog(self):
        # Message that pops up when league is created successfully
        app = MDApp.get_running_app()
        #if not self.join_success_dialog:
        okay_button = MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=app.theme_cls.primary_color,
                )
        cancel_button = MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=app.theme_cls.primary_color,
                )
        self.join_success_dialog = MDDialog(
            title="DONE",
            type='custom',
            content_cls = SuccessJoinContent(),
            buttons=[
                okay_button,
                cancel_button
            ]
        )
        okay_button.bind(on_release=self.join)
        cancel_button.bind(on_release=self.join_success_dialog.dismiss)

        self.join_success_dialog.open()
    
    def join(self, instance):
        app = MDApp.get_running_app()
        join = join_group(app.access_token, int(SuccessJoinContent.group_id))
        if join["status_code"] == 200:
            self.join_success_dialog.dismiss()
        elif join["status_code"] == 409:
            self.join_success_dialog.dismiss()
            self.join_dialog.open()
            self.league_id.helper_text = "You are already a member of this group"
            self.league_id.error = True
