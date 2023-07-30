from api.pl_api import *
from api.db_api import *
from db import *

from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout

from functools import partial

class MyLabel(MDLabel):
    pass

class BetDialog(MDBoxLayout):
    pass

class MainWindow(Screen):
    padding = NumericProperty(40)
    spacing = NumericProperty(2)
    dialog = None

    '''
    NavItem - 'Table'
    '''

    def users_table(self):

        app = MDApp.get_running_app()

        first10 = first_ten(app.access_token)

        layout = self.ids.main
        layout.clear_widgets()

        list = ["position", "username", "points", "three_pointers", "one_pointers"]
        header_grid = MDGridLayout(
                cols = 5,
                padding = 5
            )
        for i in list:
            header_grid.add_widget(
                MDLabel(
                    text = i.capitalize()
                )
            )
        layout.add_widget(header_grid)

        for i in first10:
            grid = MDGridLayout(
                cols = 5,
                padding = 5
            )
            for header in list:
                grid.add_widget(
                    MDLabel(
                        text = str(i[header])
                        )
                    )
            layout.add_widget(grid)
        
        me = my_user_info(app.access_token, app.user_id)
        def add_me():
            grid = MDGridLayout(
                cols = 5,
                padding = 5
            )
            for header in list:
                grid.add_widget(
                    MDLabel(
                        text = str(me[header])
                        )
                    )
            layout.add_widget(grid)
        if me["position"] == 11:
            add_me()
        elif me["position"] > 11:
            layout.add_widget(
                MDLabel(
                text = '...'
                )
            )
            add_me()
    
    def show_full_table(self, instance):
        pass
            
    '''
    NavItem - 'Premier League Table'
    '''

    def pl_table(self):
        app = MDApp.get_running_app()

        widget_height = app.root.height / 21  - (self.padding * 2) / 21 - 40/21 - 60/21

        self.ids.boxlayout.clear_widgets()
        self.ids.boxlayout2.clear_widgets()

        headings = ["", "Club", "MP", "W", "D", "L", "Pts", "GF", "GA", "GD"]
        headings_layout = MDGridLayout(cols=2, adaptive_height=True, md_bg_color = (1, 1, 1, 1))
        headings_layout2 = MDGridLayout(cols=8, adaptive_height=True, md_bg_color = (1, 1, 1, 1))

        for i in headings:
            if i == "":
                headings_layout.add_widget(MDLabel(text=i,
                                                size_hint_y = None,
                                                height = widget_height))
            elif i == "Club":
                headings_layout.add_widget(MDLabel(text=i,
                                                size_hint_y = None,
                                                height = widget_height,
                                                size_hint_x = 2))
            elif i == "Pts":
                headings_layout2.add_widget(MDLabel(text=i,
                                                size_hint_y = None,
                                                height = widget_height,
                                                bold=True))
            else:
                headings_layout2.add_widget(MDLabel(text=i,
                                                size_hint_y = None,
                                                height = widget_height))
                
        self.ids.boxlayout.add_widget(headings_layout)
        self.ids.boxlayout2.add_widget(headings_layout2)

        position = 1
        for i in pl.positions.keys():
            gridlayout = MDGridLayout(cols=2, adaptive_height=True, md_bg_color = (1, 1, 1, 1))
            gridlayout2 = MDGridLayout(cols=8, adaptive_height=True, md_bg_color = (1, 1, 1, 1))
            gridlayout.add_widget(MDLabel(text=str(position),
                                          adaptive_height=False,
                                          size_hint_y = None,
                                          height = widget_height))
            gridlayout.add_widget(MDLabel(text=str(pl.positions[i]["name"]),
                                          adaptive_height=False,
                                          size_hint_y = None,
                                          height = widget_height,
                                          size_hint_x = 2))
            for i2 in pl.positions[i].keys():
                if i2 == "points":
                    gridlayout2.add_widget(MDLabel(text=str(pl.positions[i][i2]),
                                                  size_hint_y = None,
                                                  height = widget_height,
                                                  bold=True))
                elif i2 != "id" and i2 != "name": 
                    # We do not need the team id when displaying premier league table.
                    # Name column is already included.
                    gridlayout2.add_widget(MDLabel(text=str(pl.positions[i][i2]),
                                                   size_hint_y = None,
                                                   height = widget_height))
            self.ids.boxlayout.add_widget(gridlayout)
            self.ids.boxlayout2.add_widget(gridlayout2)
            position += 1

        self.ids.boxlayout.md_bg_color = '#212121' # app.theme_cls.primary_color
    
    '''
    NavItem - 'PostBet'
    '''
    
    def what_gameweek(self, gameweek):
        # When no gameweek entered this statement will find out
        # what gameweek we are currently in
        if gameweek == 0:
            b = 0
            for week in pl.matches.keys():
                for match_id in pl.matches[week].keys():
                    if pl.matches[week][match_id]["started"] == False:
                        gameweek = week
                        b = 1
                        break
                if b == 1:
                    break
        self.gameweek = 38 if gameweek == 0 else gameweek
    
    def bets(self, gameweek=0):

        self.what_gameweek(gameweek)

        # This will hold score TextField widgets
        self.codes = {}

        # A list of all match codes in the current gameweek
        self.codes_list = [match_id for match_id in pl.matches[self.gameweek].keys()]

        app = MDApp.get_running_app()
        layout = self.ids.my_main_layout
        layout.clear_widgets()
        layout_height = app.root.height * 1.5

        header = MDLabel(
            text = f'Gameweek {self.gameweek}',
            halign = 'center'
        )
        self.ids.header.add_widget(header)

        grid = MDGridLayout(
            cols = 3,
            size_hint_y = None,
            adaptive_height = True
        )
        layout.add_widget(grid)
        layout.add_widget(
            MDBoxLayout(
                size_hint_y = None,
                height = app.root.height / 2
            )
        )
        
        grid_layout1 = MDGridLayout(
            size_hint_y = None,
            adaptive_height = True,
            cols = 2,
            spacing = 10
            )
    
        self.grid_layout2 = MDGridLayout(
            size_hint_y = None,
            adaptive_height = True,
            cols = 2,
            spacing = 10,
            padding = [60, 0, 60, 0]
            )

        grid_layout3 = MDGridLayout(
            size_hint_y = None,
            adaptive_height = True,
            cols = 2,
            spacing = 10
            )

        for game in self.codes_list:

            self.team1 = MyLabel(
                text = str(pl.teams[pl.matches[self.gameweek][game]["team1"]]["name"]),
                size_hint = (0.3, None),
                height = layout_height / 10,
                valign = "bottom",
                halign = "center"
                )
            grid_layout1.add_widget(self.team1)

            self.goal1 = MyLabel(
                text = str(pl.matches[self.gameweek][game]["goals1"]),
                size_hint = (0.1, None),
                height = layout_height / 10,
                valign = "middle",
                halign = "center"
                )
            grid_layout1.add_widget(self.goal1)

            another_layout = MDGridLayout(
                size_hint_y = None,
                height = layout_height / 10,
                cols = 1,
                padding = [0, 20, 0, 0]
            )
            self.guess1 = MDTextField(
                multiline = False,
                input_type = 'number'
                )
            another_layout.add_widget(self.guess1)
            self.grid_layout2.add_widget(another_layout)
            
            another_layout2 = MDGridLayout(
                size_hint_y = None,
                height = layout_height / 10,
                cols = 1,
                padding = [0, 20, 0, 0]
            )
            self.guess2 = MDTextField(
                multiline = False,
                input_type = 'number'
                )
            another_layout2.add_widget(self.guess2)
            self.grid_layout2.add_widget(another_layout2)

            self.goal2 = MyLabel(
                text = str(pl.matches[self.gameweek][game]["goals2"]),
                size_hint = (0.1, None),
                height = layout_height / 10,
                valign = "middle",
                halign = "center"
                )
            grid_layout3.add_widget(self.goal2)

            self.team2 = MyLabel(
                text=str(pl.teams[pl.matches[self.gameweek][game]["team2"]]["name"]),
                size_hint = (0.3, None),
                height = layout_height / 10,
                valign = "middle",
                halign = "center"
                )
            grid_layout3.add_widget(self.team2)

            # Assigning the textfield widgets to a match code in a dictionary
            # so I can access it when submitting the score guesses
            self.codes[game] = {}
            self.codes[game]["guess1"] = self.guess1
            self.codes[game]["guess2"] = self.guess2

        grid.add_widget(grid_layout1)
        grid.add_widget(self.grid_layout2)
        grid.add_widget(grid_layout3)

        self.when_text_validate()
        self.display_previous_guesses()
    
    def when_text_validate(self):

        def next(value, instance):
            # This focuses on the next widget
            widget = self.grid_layout2.children[value].children[0]
            widget.focus = True
            self.ids.the_scroll.scroll_to(widget, padding = 180)

        # grid_layout2 contains layouts that contain text fields
        # when 'enter' is pressed the focus will move to the next widget
        i = 0
        for layout in self.grid_layout2.children:
            if i == 0:
                # last widget
                pass
            else:
                layout.children[0].bind(on_text_validate=partial(next, i - 1))
            i = i + 1
    
    def display_previous_guesses(self):
        
        app = MDApp.get_running_app()
        does_exist = False
        bets = get_all_bets_by_user_id(app.access_token)
        if bets["status_code"] == 200:
            for bet in bets["list"]:
                code = bet['match_id']
                if code in self.codes_list:
                    does_exist = True
                    break
            if does_exist == True:
                for bet in bets["list"]:
                    try:
                        code = bet['match_id']
                        guess1 = bet['goal1']
                        guess2 = bet['goal2']
                        self.codes[code]["guess1"].text = str(guess1)
                        self.codes[code]["guess2"].text = str(guess2)
                    except KeyError:
                        pass
        else:
            pass

    def previous_gameweek(self):

        if self.gameweek == 1:
            pass
        else:
            self.gameweek -= 1
            self.bets(self.gameweek)


    def next_gameweek(self):

        if self.gameweek == 38:
            pass
        else:
            self.gameweek += 1
            self.bets(self.gameweek)

    
    def do_bets(self):

        #Sending input to the server
        app = MDApp.get_running_app()
        matches = []
        list_guess1 = []
        list_guess2 = []
        for code in self.codes.keys():
            guess1 = self.codes[code]["guess1"].text
            guess2 = self.codes[code]["guess2"].text
            if guess1 == "":
                self.codes[code]["guess1"].text = "0"
            if guess2 == "":
                self.codes[code]["guess2"].text = "0"
            matches.append(code)
            list_guess1.append(guess1)
            list_guess2.append(guess2)

        update_bets = update_multiple_bets(str(app.access_token), matches, list_guess1, list_guess2)

        if update_bets["status_code"] == 200:
            self.open_dialog("Your predictions were submitted successfully!")
        elif update_bets["status_code"] == 405:
            self.open_dialog("Cannot create/update predictions once the gameweek has started.")
    
    def open_dialog(self, message):

        app = MDApp.get_running_app()
        if not self.dialog:
            okay_button = MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                    )
            self.dialog = MDDialog(
                title="Name your league",
                type='custom',
                content_cls = BetDialog(),
                buttons=[
                    okay_button
                ]
            )
            okay_button.bind(on_release=self.exit_dialog)
        
        self.dialog.content_cls.children[0].text = message
        self.dialog.open()
    
    def exit_dialog(self, instance):

        self.dialog.content_cls.children[0].text = ''
        self.dialog.dismiss()

    '''
    NavItem - 'More'
    '''    
    
    def logout(self):

        self.manager.current = "LoginWindow"
        app = MDApp.get_running_app()
        revoke_jwt(app.access_token)
    
    def delete_account(self):
        
        app = MDApp.get_running_app()
        delete_account(app.access_token, app.user_id)
        self.manager.current = "CreateUser"
