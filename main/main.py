from login import *
from pl_api import *
from db_api import *
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRect, MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
from kivy.clock import Clock
from datetime import datetime

class MyLabel(MDLabel):
    pass

class LoginWindow(Screen):

    def log_in(self):
        username = self.ids.login.text
        password = self.ids.password.text
        if check_password(username, password) == True:
            self.manager.transition = NoTransition()
            self.manager.current = 'PLTable'
            app = MDApp.get_running_app()
            app.access_token, app.refresh_token, app.user_id = login(username, password)
        else:
            print('Wrong password')
    def password(self):
        if self.ids.password.password == True:
            self.ids.password.password = False
            self.ids.password.icon_left = "eye"
            Clock.schedule_once(self.focus, 0.05)
        else:
            self.ids.password.password = True
            self.ids.password.icon_left = "eye-off"
            Clock.schedule_once(self.focus, 0.05)
    
    def focus(self, dt):
        self.ids.password.focus = True
'''
class LoginWindow1(Screen):
    pass

    def log_in(self):
        username = self.ids.login.text
        password = self.ids.password.text
        if check_password(username, password) == True:
            self.manager.transition = NoTransition()
            self.manager.current = 'PLTable'
        else:
            pass
            #self.ids.my_label.text = 'Failed to log in'
            #self.ids.my_label.height = self.ids.my_label.texture_size[1]
'''
class CreateUser(Screen):
    pass

    def create_user_app(self):
        username = self.ids.login.text
        password = self.ids.password.text
        if check_password(username, password):
            create_user(username, password)
            login(username, password)
            #add_player(username)
            self.manager.current = 'PLTable'
        else:
            self.ids.my_label.text = 'User already exists'
            self.ids.my_label.height = self.ids.my_label.texture_size[1]

class PLTable(Screen):
    pass

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
        for i in positions.keys():
            name += positions[i]["name"] + '\n'
            matches_played += str(positions[i]["matches_played"]) + '\n'
            wins += str(positions[i]["wins"]) + '\n'
            draws += str(positions[i]["draws"]) + '\n'
            losses += str(positions[i]["losses"]) + '\n'
            goals_scored += str(positions[i]["goals_scored"]) + '\n'
            goals_conceded += str(positions[i]["goals_conceded"]) + '\n'
            goals_balance += str(positions[i]["goals_balance"]) + '\n'
            points += str(positions[i]["points"]) + '\n'
        self.ids.name.text = name
        self.ids.matches_played.text = matches_played
        self.ids.wins.text = wins 
        self.ids.draws.text = draws
        self.ids.losses.text = losses
        self.ids.goals_scored.text = goals_scored
        self.ids.goals_conceded.text = goals_conceded
        self.ids.goals_balance.text = goals_balance
        self.ids.points.text = points

class Bet(Screen):
    def bets(self):
        b = 0
        for i in matches.keys():
            for i2 in matches[i].keys():
                if matches[i][i2]["started"] == False:
                    a = i
                    b = 1
                    break
            if b == 1:
                break

        list1 = []
        self.codes = {}

        for i in matches[a].keys():
            list1.append(i)

        app = MDApp.get_running_app()
        layout = self.ids.mylayout
        layout_height = app.root.height / (len(list1) - 2)

        self.entries = []
        self.codes["Gameweek"] = a
        self.codes["codes"] = {}

        for i in list1:
            gridlayout = MDGridLayout(size_hint_y = None,
                                      height = layout_height,
                                      cols = 6,
                                      spacing = 10)
            self.team1 = MyLabel(text = str(teams[matches[a][i]["team1"]]["name"]),
                                 valign = "middle",
                                 halign = "center")
            gridlayout.add_widget(self.team1)
            self.goal1 = MyLabel(text = str(matches[a][i]["goals1"]),
                                 valign = "middle",
                                 halign = "center")
            gridlayout.add_widget(self.goal1)
            self.guess1 = MDTextField(size_hint = [0.5, 1],
                                      multiline = False,
                                      input_type = 'number')
            gridlayout.add_widget(self.guess1)
            self.entries.append(self.guess1)
            self.guess2 = MDTextField(size_hint = [0.5, 1],
                                      multiline = False,
                                      input_type = 'number')
            gridlayout.add_widget(self.guess2)
            self.entries.append(self.guess2)
            self.goal2 = MyLabel(text = str(matches[a][i]["goals2"]),
                                 valign = "middle",
                                 halign = "center")
            gridlayout.add_widget(self.goal2)
            self.team2 = MyLabel(text=str(teams[matches[a][i]["team2"]]["name"]),
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
        for i in self.entries:
            if i.text == '':
                i.text = '0'
        app = MDApp.get_running_app()
        for i in self.codes["codes"].keys():
            guess1 = int(self.codes["codes"][i]["guess1"].text)
            guess2 = int(self.codes["codes"][i]["guess2"].text)
            post_bet(str(app.access_token), str(i), guess1, guess2, int(app.user_id))

        


class MainWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass

class AwesomeApp(MDApp):
    def build(self):
        kv = Builder.load_file('user.kv')
        #Window.clearcolor = (1, 1, 1, 1)
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Teal'
        #self.theme_cls.accent_palette = ''
        return kv

if __name__ == '__main__':
    AwesomeApp().run()