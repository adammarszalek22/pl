from api.pl_api import *
from api.db_api import *
from db import *

from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout

class MyLabel(MDLabel):
    pass

class MainWindow(Screen):
    padding = NumericProperty(40)
    def table(self):
        app = MDApp.get_running_app()

        size_num = 21
        widget_height = app.root.height / size_num  - (self.padding * 2) / size_num - 5

        self.ids.boxlayout.clear_widgets()
        self.ids.boxlayout2.clear_widgets()

        headings = ["", "Club", "MP", "W", "D", "L", "Pts", "GF", "GA", "GD"]
        headings_layout = MDGridLayout(cols=2, adaptive_height=True, md_bg_color = (1, 1, 1, 1))
        headings_layout2 = MDGridLayout(cols=8, adaptive_height=True, md_bg_color = (1, 1, 1, 1))
        position = 1

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

    def bets(self, gameweek=0):
        # When no gameweek entered this statement will find out what gameweek we are currently in
        if gameweek == 0:
            b = 0
            for i in pl.matches.keys():
                for i2 in pl.matches[i].keys():
                    if pl.matches[i][i2]["started"] == False:
                        gameweek = i
                        self.current_gameweek = i
                        b = 1
                        break
                if b == 1:
                    break
        if gameweek == 0:
            self.gameweek = 38
            self.current_gameweek = 38
        else:
            self.gameweek = gameweek
        
        gameweek_string = 'Gameweek ' + str(self.gameweek)

        self.codes_list = []
        self.codes = {}

        # A list of all match codes in the current gameweek
        for i in pl.matches[gameweek_string].keys():
            self.codes_list.append(i)

        app = MDApp.get_running_app()
        layout = self.ids.mylayout
        layout.clear_widgets()
        layout_height = app.root.height / 8

        for i in self.codes_list:
            gridlayout = MDGridLayout(size_hint_y = None,
                                      height = layout_height,
                                      cols = 6,
                                      spacing = 10)
            self.team1 = MyLabel(text = str(pl.teams[pl.matches[gameweek_string][i]["team1"]]["name"]),
                                 size_hint = (0.3, 1),
                                 valign = "bottom",
                                 halign = "center")
            gridlayout.add_widget(self.team1)
            self.goal1 = MyLabel(text = str(pl.matches[gameweek_string][i]["goals1"]),
                                 size_hint = (0.1, 1),
                                 valign = "middle",
                                 halign = "center")
            gridlayout.add_widget(self.goal1)
            self.guess1 = MDTextField(size_hint = (0.05, 1),
                                      multiline = False,
                                      input_type = 'number')
            gridlayout.add_widget(self.guess1)
            self.guess2 = MDTextField(size_hint = (0.05, 1),
                                      multiline = False,
                                      input_type = 'number')
            gridlayout.add_widget(self.guess2)
            self.goal2 = MyLabel(text = str(pl.matches[gameweek_string][i]["goals2"]),
                                 size_hint = (0.1, 1),
                                 valign = "middle",
                                 halign = "center")
            gridlayout.add_widget(self.goal2)
            self.team2 = MyLabel(text=str(pl.teams[pl.matches[gameweek_string][i]["team2"]]["name"]),
                                 size_hint = (0.3, 1),
                                 valign = "middle",
                                 halign = "center")
            gridlayout.add_widget(self.team2)

            # Assigning the textfield widgets to a match code in a dictionary
            # so I can access it when submitting the score guesses
            self.codes[i] = {}
            self.codes[i]["guess1"] = self.guess1
            self.codes[i]["guess2"] = self.guess2

            layout.add_widget(gridlayout)
        self.display_previous_guesses()
    
    def display_previous_guesses(self):
        does_exist = False
        bets = get_all_guesses()
        for bet in bets:
            code = bet[0]
            if code in self.codes_list:
                does_exist = True
        if does_exist == True:
            for bet in bets:
                try:
                    code = bet[0]
                    guess1 = bet[1]
                    guess2 = bet[2]
                    self.codes[code]["guess1"].text = str(guess1)
                    self.codes[code]["guess2"].text = str(guess2)
                except KeyError:
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
        for code in self.codes.keys():
            if self.codes[code]["guess1"].text == "":
                self.codes[code]["guess1"].text = "0"
            if self.codes[code]["guess2"].text == "":
                self.codes[code]["guess2"].text = "0"
            guess1 = self.codes[code]["guess1"].text
            guess2 = self.codes[code]["guess2"].text
            #This adds a bet or updates it if it already exists
            bet = get_guess(code)
            if bet:
                update_guess(guess1, guess2, code)
            else:
                add_guess(code, guess1, guess2)
            update_bet(str(app.access_token), str(code), guess1, guess2, int(app.user_id))
    
    # def scores(self):
    #     app = MDApp.get_running_app()
    #     user_info = my_user_info(app.access_token, app.user_id)
    #     self.ids.username.text = str(user_info["username"])
    #     self.ids.position.text = str(user_info["position"])
    #     self.ids.points2.text = str(user_info["points"])
    #     self.ids.three_pointers.text = str(user_info["three_pointers"])
    #     self.ids.one_pointers.text = str(user_info["one_pointers"])
    
    def logout(self):
        self.manager.current = "LoginWindow"
        app = MDApp.get_running_app()
        revoke_jwt(app.access_token)
    
    def delete_account(self):
        app = MDApp.get_running_app()
        delete_account(app.access_token, app.user_id)
        delete_all_guesses()
        self.manager.current = "CreateUser"
