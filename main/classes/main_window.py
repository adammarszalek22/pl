from api.pl_api import *
from api.db_api import *

from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout

class MyLabel(MDLabel):
    pass

class MainWindow(Screen):
    def scroll1(self):
        self.ids.scrolltwo.scroll_y = self.ids.scrollone.scroll_y
    def scroll2(self):
        self.ids.scrollone.scroll_y = self.ids.scrolltwo.scroll_y
    def table2(self):
        position = 1
        for i in pl.positions.keys():
            gridlayout = MDGridLayout(cols=2, adaptive_height=True)
            gridlayout2 = MDGridLayout(cols=8, adaptive_height=True)
            gridlayout.add_widget(MDLabel(text=str(position), adaptive_height=False))
            gridlayout.add_widget(MDLabel(text=str(pl.positions[i]["name"]),
                                          adaptive_height=False,
                                          size_hint_x = 2))
            for i2 in pl.positions[i].keys():
                if i2 == "points":
                    gridlayout2.add_widget(MDLabel(text=str(pl.positions[i][i2]),
                                                  adaptive_height=False,
                                                  bold=True))
                elif i2 != "id" and i2 != "name": 
                    # We do not need the team id when displaying premier league table.
                    # Name column is already included.
                    gridlayout2.add_widget(MDLabel(text=str(pl.positions[i][i2]),
                                                  adaptive_height=False))
            self.ids.boxlayout3.add_widget(gridlayout)
            self.ids.boxlayout4.add_widget(gridlayout2)
            position += 1
    def table1(self):
        position = 1
        for i in pl.positions.keys():
            gridlayout = MDGridLayout(cols=2, adaptive_height=True)
            gridlayout2 = MDGridLayout(cols=8, adaptive_height=True)
            gridlayout.add_widget(MDLabel(text=str(position), adaptive_height=False))
            gridlayout.add_widget(MDLabel(text=str(pl.positions[i]["name"]),
                                          adaptive_height=False,
                                          size_hint_x = 2))
            for i2 in pl.positions[i].keys():
                if i2 == "points":
                    gridlayout2.add_widget(MDLabel(text=str(pl.positions[i][i2]),
                                                  adaptive_height=False,
                                                  bold=True))
                elif i2 != "id" and i2 != "name": 
                    # We do not need the team id when displaying premier league table.
                    # Name column is already included.
                    gridlayout2.add_widget(MDLabel(text=str(pl.positions[i][i2]),
                                                  adaptive_height=False))
            self.ids.boxlayout.add_widget(gridlayout)
            self.ids.boxlayout2.add_widget(gridlayout2)
            position += 1

    def table(self):
        name = ''
        matches_played = ''
        wins = ''
        draws = ''
        losses = ''
        goals_scored = ''
        goals_conceded = ''
        goals_balance = ''
        points = ''
        for i in pl.positions.keys():
            name += pl.positions[i]["name"] + '\n'
            matches_played += str(pl.positions[i]["matches_played"]) + '\n'
            wins += str(pl.positions[i]["wins"]) + '\n'
            draws += str(pl.positions[i]["draws"]) + '\n'
            losses += str(pl.positions[i]["losses"]) + '\n'
            goals_scored += str(pl.positions[i]["goals_scored"]) + '\n'
            goals_conceded += str(pl.positions[i]["goals_conceded"]) + '\n'
            goals_balance += str(pl.positions[i]["goals_balance"]) + '\n'
            points += str(pl.positions[i]["points"]) + '\n'
        self.ids.name.text = name
        self.ids.matches_played.text = matches_played
        self.ids.wins.text = wins 
        self.ids.draws.text = draws
        self.ids.losses.text = losses
        self.ids.goals_scored.text = goals_scored
        self.ids.goals_conceded.text = goals_conceded
        self.ids.goals_balance.text = goals_balance
        self.ids.points.text = points

    def bets(self):
        b = 0
        for i in pl.matches.keys():
            for i2 in pl.matches[i].keys():
                if pl.matches[i][i2]["started"] == False:
                    a = i
                    b = 1
                    break
            if b == 1:
                break

        list1 = []
        self.codes = {}

        for i in pl.matches[a].keys():
            list1.append(i)

        app = MDApp.get_running_app()
        layout = self.ids.mylayout
        layout.clear_widgets()
        layout_height = app.root.height / (len(list1) - 2)

        self.entries = []
        self.codes["Gameweek"] = a
        self.codes["codes"] = {}

        for i in list1:
            gridlayout = MDGridLayout(size_hint_y = None,
                                      height = layout_height,
                                      cols = 6,
                                      spacing = 10)
            self.team1 = MyLabel(text = str(pl.teams[pl.matches[a][i]["team1"]]["name"]),
                                 size_hint = (0.3, 1),
                                 valign = "bottom",
                                 halign = "center")
            gridlayout.add_widget(self.team1)
            self.goal1 = MyLabel(text = str(pl.matches[a][i]["goals1"]),
                                 size_hint = (0.1, 1),
                                 valign = "middle",
                                 halign = "center")
            gridlayout.add_widget(self.goal1)
            self.guess1 = MDTextField(size_hint = (0.05, 1),
                                      multiline = False,
                                      input_type = 'number')
            gridlayout.add_widget(self.guess1)
            self.entries.append(self.guess1)
            self.guess2 = MDTextField(size_hint = (0.05, 1),
                                      multiline = False,
                                      input_type = 'number')
            gridlayout.add_widget(self.guess2)
            self.entries.append(self.guess2)
            self.goal2 = MyLabel(text = str(pl.matches[a][i]["goals2"]),
                                 size_hint = (0.1, 1),
                                 valign = "middle",
                                 halign = "center")
            gridlayout.add_widget(self.goal2)
            self.team2 = MyLabel(text=str(pl.teams[pl.matches[a][i]["team2"]]["name"]),
                                 size_hint = (0.3, 1),
                                 valign = "middle",
                                 halign = "center")
            gridlayout.add_widget(self.team2)

            
            self.codes["codes"][i] = {}
            self.codes["codes"][i]["guess1"] = self.guess1
            self.codes["codes"][i]["guess2"] = self.guess2

            layout.add_widget(gridlayout)
        
        user = my_user_info(app.access_token, app.user_id)
        t = False
        for i in user["bets"]:
            if i["match_id"] in list1:
                t = True
        if t == True:
            for i in user["bets"]:
                self.codes["codes"][i["match_id"]]["guess1"].text = str(i["goal1"])
                self.codes["codes"][i["match_id"]]["guess2"].text = str(i["goal2"])

    
    def do_bets(self):
        #Sending input to the server
        for i in self.entries:
            if i.text == '':
                i.text = '0'
        app = MDApp.get_running_app()
        for i in self.codes["codes"].keys():
            guess1 = int(self.codes["codes"][i]["guess1"].text)
            guess2 = int(self.codes["codes"][i]["guess2"].text)
            #This adds a bet or updates it if it already exists
            update_bet(str(app.access_token), str(i), guess1, guess2, int(app.user_id))
    
    def scores(self):
        app = MDApp.get_running_app()
        user_info = my_user_info(app.access_token, app.user_id)
        self.ids.username.text = str(user_info["username"])
        self.ids.position.text = str(user_info["position"])
        self.ids.points2.text = str(user_info["points"])
        self.ids.three_pointers.text = str(user_info["three_pointers"])
        self.ids.one_pointers.text = str(user_info["one_pointers"])