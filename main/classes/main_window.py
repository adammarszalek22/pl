from api.pl_api import *
from api.db_api import *
from db import *

from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from threading import Thread

from functools import partial

from kivy.metrics import dp

import time


class MyLabel(MDLabel):
    pass

class BetDialog(MDBoxLayout):
    pass

class GlobalTable(MDBoxLayout):
    pass

class MainWindow(Screen):
    padding = NumericProperty(40)
    spacing = NumericProperty(2)
    dialog = None
    table_dialog = None

    '''
    NavItem - 'Table'
    '''

    def users_table(self):

        app = MDApp.get_running_app()

        # getting the 10 best users
        first10 = first_ten(app.access_token)

        list = ["position", "username", "points", "three_pointers", "one_pointers"]
        grid = self.ids.grid
        grid.clear_widgets()

        try:
            for i in first10:
                for header in list:
                    self.label = MDLabel(
                            text = str(i[header])
                            )
                    self.label.font_size = "12dp"
                    grid.add_widget(self.label)
            
            me = my_user_info(app.access_token, app.user_id)
            self.my_pos = int(me["position"])
            def _add_me():
                for header in list:
                    self.label = MDLabel(
                            text = str(me[header])
                            )
                    self.label.font_size = "12dp"
                    grid.add_widget(self.label)

            if me["position"] == 11:
                _add_me()
            elif me["position"] > 11:
                grid.add_widget(
                    MDLabel(
                    text = '...',
                    font_size = "12dp"
                    )
                )
                for j in range(4):
                    grid.add_widget(MDLabel())
                _add_me()
        except KeyError:
            pass
    
    def show_full(self):
        app = MDApp.get_running_app()

        if not self.table_dialog:

            self.box = GlobalTable()
            self.scroll_box = self.box.children[0].children[0]

            all_users = get_all_users(app.access_token)
            users = [v for v in sorted(all_users['users'], key = lambda item: item['position'])]



            for i, user in enumerate(users):
                colour = (0, 0, 1, 1)

                self.headers = {}

                self.headers["position"] = MDLabel(text = str(i + 1), size_hint_y = None, adaptive_height = True, theme_text_color = 'Custom', text_color = colour if self.my_pos == i + 1 else None)
                self.headers["username"] = MDLabel(text = user["username"], size_hint_y = None, adaptive_height = True, theme_text_color = 'Custom', text_color = colour if self.my_pos == i + 1 else None)
                self.headers["points"] = MDLabel(text = str(user["points"]), size_hint_y = None, adaptive_height = True, theme_text_color = 'Custom', text_color = colour if self.my_pos == i + 1 else None)
                self.headers["three_pointers"] = MDLabel(text = str(user["three_pointers"]), size_hint_y = None, adaptive_height = True, theme_text_color = 'Custom', text_color = colour if self.my_pos == i + 1 else None)
                self.headers["one_pointers"] = MDLabel(text = str(user["one_pointers"]), size_hint_y = None, adaptive_height = True, theme_text_color = 'Custom', text_color = colour if self.my_pos == i + 1 else None)

                for key in self.headers.keys():
                    self.headers[key].font_size = '12dp'
                    self.scroll_box.add_widget(self.headers[key])

            okay_button = MDFlatButton(
                        text="Back",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                    )
            
            self.table_dialog = MDDialog(
                title='',
                type='custom',
                content_cls = self.box,
                buttons=[
                    okay_button
                ]
            )
            okay_button.bind(on_release=self.exit_full_table)
            
        self.table_dialog.open()
    
    def exit_full_table(self, instance):

        self.table_dialog.dismiss()
            
    '''
    NavItem - 'Premier League Table'
    '''

    def pl_table(self):

        self.ids.boxlayout.clear_widgets()
        self.ids.boxlayout2.clear_widgets()

        headings = ["", "Club", "MP", "W", "D", "L", "Pts", "GF", "GA", "GD"]
        headings_layout = MDGridLayout(cols=2, md_bg_color = (1, 1, 1, 1))
        headings_layout2 = MDGridLayout(cols=8, md_bg_color = (1, 1, 1, 1))
        
        self.ids.boxlayout.add_widget(headings_layout)
        self.ids.boxlayout2.add_widget(headings_layout2)

        for i in headings:
            if i == "":
                headings_layout.add_widget(MDLabel(text=i))
            elif i == "Club":
                headings_layout.add_widget(MDLabel(text=i,
                                                size_hint_x = 2))
            elif i == "Pts":
                headings_layout2.add_widget(MDLabel(text=i,
                                                bold=True))
            else:
                headings_layout2.add_widget(MDLabel(text=i))

        position = 1
        for i in pl.positions.keys():
            # Holds position number and team name
            gridlayout = MDGridLayout(cols=2, md_bg_color = (1, 1, 1, 1))
            # Holds the games playes, points, etc. (all the numerical stats)
            gridlayout2 = MDGridLayout(cols=8, md_bg_color = (1, 1, 1, 1))

            self.ids.boxlayout.add_widget(gridlayout)
            self.ids.boxlayout2.add_widget(gridlayout2)

            gridlayout.add_widget(MDLabel(text=str(position)))
            gridlayout.add_widget(MDLabel(text=str(pl.positions[i]["name"]),
                                          size_hint_x = 2))
            for i2 in pl.positions[i].keys():
                if i2 == "points":
                    gridlayout2.add_widget(MDLabel(text=str(pl.positions[i][i2]),
                                                  bold=True))
                elif i2 != "id" and i2 != "name": 
                    # We do not need the team id when displaying premier league table.
                    # Name column is already included.
                    gridlayout2.add_widget(MDLabel(text=str(pl.positions[i][i2])))
            position += 1

        self.ids.boxlayout.md_bg_color = (1, 1, 1, 1)#'#212121' # app.theme_cls.primary_color
    
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

        # header = MDLabel(
        #     text = f'Gameweek {self.gameweek}',
        #     halign = 'center'
        # )
        # self.ids.header.add_widget(header)
        self.ids.header_label.text = f'Gameweek {self.gameweek}'

        # Main gridlayout that will hold three other gridlayouts 
        grid = MDGridLayout(
            cols = 3,
            size_hint_y = None,
            adaptive_height = True
        )
        layout.add_widget(grid)

        # Leaving space below widgets to make
        # keyboard management easier (on a mobile)
        layout.add_widget(
            MDBoxLayout(
                size_hint_y = None,
                height = app.root.height / 2
            )
        )
        
        # For team1 and goal1
        grid_layout1 = MDGridLayout(
            size_hint_y = None,
            adaptive_height = True,
            cols = 2,
            spacing = 10
            )

        # For prediction1 and prediction2
        self.grid_layout2 = MDGridLayout(
            size_hint_y = None,
            adaptive_height = True,
            cols = 2,
            spacing = 10,
            padding = [60, 0, 60, 0]
            )

        # For team2 and goal2
        grid_layout3 = MDGridLayout(
            size_hint_y = None,
            adaptive_height = True,
            cols = 2,
            spacing = 10
            )

        for game in self.codes_list:

            self.team1 = MyLabel(
                text = str(pl.teams[pl.matches[self.gameweek][game]["team1"]]["name"]), # team name
                size_hint = (0.3, None),
                height = layout_height / 10,
                valign = "bottom",
                halign = "center"
                )
            grid_layout1.add_widget(self.team1)

            self.goal1 = MyLabel(
                text = str(pl.matches[self.gameweek][game]["goals1"]), # goals scored by team1
                size_hint = (0.1, None),
                height = layout_height / 10,
                valign = "middle",
                halign = "center"
                )
            grid_layout1.add_widget(self.goal1)

            # Putting textfields in a grid layout so that it 
            # is easier to align with other widgets
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
            
            # Putting textfields in a grid layout so that it 
            # is easier to align with other widgets
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
                text = str(pl.matches[self.gameweek][game]["goals2"]), # goals scored by team2
                size_hint = (0.1, None),
                height = layout_height / 10,
                valign = "middle",
                halign = "center"
                )
            grid_layout3.add_widget(self.goal2)

            self.team2 = MyLabel(
                text=str(pl.teams[pl.matches[self.gameweek][game]["team2"]]["name"]), # team2 name
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
                guess1 = 0
            if guess2 == "":
                self.codes[code]["guess2"].text = "0"
                guess2 = 0
            matches.append(code)
            list_guess1.append(guess1)
            list_guess2.append(guess2)

        update_bets = update_multiple_bets(str(app.access_token), matches, list_guess1, list_guess2)
        print(update_bets)

        if update_bets["status_code"] == 200:
            self.open_dialog("Your predictions were submitted successfully!", "Submitted")
        elif update_bets["status_code"] == 405:
            self.open_dialog("Cannot create/update predictions once the gameweek has started.", "Failed")
    
    def open_dialog(self, message, title):

        app = MDApp.get_running_app()
        if not self.dialog:
            okay_button = MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                    )
            self.dialog = MDDialog(
                title='',
                type='custom',
                content_cls = BetDialog(),
                buttons=[
                    okay_button
                ]
            )
            okay_button.bind(on_release=self.exit_dialog)
        
        self.dialog.title = title
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
        pass
        # app = MDApp.get_running_app()
        # delete_account(app.access_token, app.user_id)
        # self.manager.current = "CreateUser"
