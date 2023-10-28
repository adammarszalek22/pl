from api.pl_api import pl
from api.db_api import first_ten, my_user_info, get_all_users, get_all_bets_by_user_id, revoke_jwt, update_multiple_bets

from kivy.properties import NumericProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import mainthread
from kivy.animation import Animation

from functools import partial
from threading import Thread
from datetime import datetime

import copy
import time

def convert_date(date):
    months = {
        1 : 'January',
        2 : 'February',
        3 : 'March',
        4 : 'April',
        5 : 'May',
        6 : 'June',
        7 : 'July',
        8 : 'August',
        9 : 'September',
        10 : 'October',
        11 : 'November',
        12 : 'December'
    }
    return f"{date[8:10]} {months[int(date[5:7])]} {date[0:4]}"

def has_passed(start_time):
    return start_time < datetime.now()

class Submission_Dialog(MDBoxLayout):
    pass

class GlobalTable(MDBoxLayout):
    pass

class MainWindow(Screen):

    padding = ListProperty([20, 100, 20, 100])
    spacing = NumericProperty(20)

    dialog = None
    widgets = None
    gameweek = None
    name_widgets = None
    first10 = None

    table_dialog = None
    bets = None

    colour = (0, 0, 1, 1)

    def enter(self):

        thread1 = Thread(target = self.display_pl_table)
        thread1.start()

        thread2 = Thread(target = self.display_gameweek_games)
        thread2.start()

        thread3 = Thread(target = self.display_users_table)
        thread3.start()

    '''
    NavItem - 'Table'
    '''

    def __add_me(self, num):
        # used in users_table function
        j = 4
        for header in self.list:
            self.main_grid[num].children[j].text = str(self.me[header])
            # self.label = MDLabel(text = str(i[header]), theme_text_color = t_t_c, text_color = t_c)
            j -= 1

    def display_users_table(self):

        if self.first10:
            return
        
        app = MDApp.get_running_app()

        self.main_grid = list(reversed(self.ids.main.ids.grid.children))

        # getting the 10 best users
        self.first10 = first_ten(app.access_token)

        # headers/keys
        self.list = ["position", "username", "points", "three_pointers", "one_pointers"]

        # getting the actual user and their position
        self.me = my_user_info(app.access_token, app.user_id)
        self.my_pos = int(self.me["position"])

        # adding the 10 users to the table
        for i, user in enumerate(self.first10):
            # t_t_c = 'Custom' if i["username"] == me["username"] else None
            # t_c = self.colour if i["username"] == me["username"] else None
            j = 4
            for header in self.list:
                self.main_grid[i].children[j].text = str(user[header])
                # self.label = MDLabel(text = str(i[header]), theme_text_color = t_t_c, text_color = t_c)
                j -= 1
        
        # if the user is 11th in the table then we add them
        if self.me["position"] == 11:
            self.__add_me(10)
        # else we leave one row empty ('...') and add the user on next line
        elif self.me["position"] > 11:
            self.main_grid[10].children[4].text = '...'
            self.__add_me(11)      
    
    def show_full(self):

        if not self.table_dialog:

            app = MDApp.get_running_app()

            self.box = GlobalTable()
            self.scroll_box = self.box.children[0].children[0]

            all_users = get_all_users(app.access_token)
            users = [v for v in sorted(all_users['users'], key = lambda item: item['position'])]

            for i, user in enumerate(users):
                
                t_t_c = 'Custom' if self.my_pos == i + 1 else None
                t_c = self.colour if self.my_pos == i + 1 else None

                self.headers = {}

                self.headers["position"] = MDLabel(text = str(i + 1), size_hint_y = None, adaptive_height = True, theme_text_color = t_t_c, text_color = t_c)
                self.headers["username"] = MDLabel(text = user["username"], size_hint_y = None, adaptive_height = True, theme_text_color = t_t_c, text_color = t_c)
                self.headers["points"] = MDLabel(text = str(user["points"]), size_hint_y = None, adaptive_height = True, theme_text_color = t_t_c, text_color = t_c)
                self.headers["three_pointers"] = MDLabel(text = str(user["three_pointers"]), size_hint_y = None, adaptive_height = True, theme_text_color = t_t_c, text_color = t_c)
                self.headers["one_pointers"] = MDLabel(text = str(user["one_pointers"]), size_hint_y = None, adaptive_height = True, theme_text_color = t_t_c, text_color = t_c)

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

    def display_pl_table(self):

        self.first_grid = list(reversed(self.ids.my_layout.ids.left_layout.children))
        self.main_grid = list(reversed(self.ids.my_layout.ids.main_layout.children))


        self.first_grid[0].children[1].text = 'Pos'
        self.first_grid[0].children[0].text = 'Club'
        i = 7
        for heading in ['MP', 'W', 'D', 'L', 'Pts', 'GA', 'GF', 'GD']:
            self.main_grid[0].children[i].text = heading
            i -= 1
        self.main_grid[0].children[3].bold = True #pos

        self.headers = ["matches_played", "wins", "draws", "losses",
                 "points", "goals_scored", "goals_conceded", "goals_balance"]
        
        for pos, club in enumerate(pl.positions.values(), start = 1):

            self.first_grid[pos].children[1].text = str(pos)

            # showing the club name
            self.first_grid[pos].children[0].text = str(club["name"])

            # showing the stats info
            for i, header in enumerate(self.headers):
                list(reversed(self.main_grid[pos].children))[i].text = str(club[header])
                list(reversed(self.main_grid[pos].children))[i].bold = True if header == "points" else False

    
    
    '''
    NavItem - 'PostBet'
    '''

    def display_gameweek_games(self):

        # find out what gameweek it is if the function is run for the first time
        if not self.gameweek:
            self.what_gameweek()
        
        # list with all match ids from current gameweek
        self.match_id_list = [match_id for match_id in pl.matches[self.gameweek].keys()]

        # # store widgets in a dict for easier access
        if not self.widgets:
            self.store_widgets()

        # display the gameweek header
        self.display_header()
        
        # show matches, scores and times from the particular gameweek
        self.show_games()

        # if predictions were already made, display them
        self.show_previous_predictions()

        # bind 'on_text' function to each textfield
        self.bind_textfields()

    def what_gameweek(self):

        class Found(Exception):
            pass
        try:
            for week in pl.matches.keys():
                for match_id in pl.matches[week].keys():
                    if pl.matches[week][match_id]["started"] == False:
                        # the first gameweek that has a match which has not yet started is the current gameweek
                        self.gameweek = week
                        self.current_gameweek = week
                        raise Found
        except Found:
            pass
    
    def previous_gameweek(self):
        if self.gameweek != 1:
            self.gameweek -= 1

    def next_gameweek(self):
        if self.gameweek != 38:
            self.gameweek += 1
    
    def store_widgets(self):

        # storing all box_layouts in a dict for easier access
        self.widgets = {}

        i = 19 # last widget index
        for box_layout in self.ids.bet_layout.ids.main.children: # the loop starts with the last widget for some reason
            self.widgets[i] = {}
            self.widgets[i]['box'] = box_layout
            self.widgets[i]['time'] = box_layout.children[0]

            self.widgets[i]['team1'] = box_layout.children[1].children[5]
            self.widgets[i]['goals1'] = box_layout.children[1].children[4]
            self.widgets[i]['prediction1'] = box_layout.children[1].children[3]
            self.widgets[i]['prediction2'] = box_layout.children[1].children[2]
            self.widgets[i]['goals2'] = box_layout.children[1].children[1]
            self.widgets[i]['team2'] = box_layout.children[1].children[0]
            
            i -= 1
    
    def display_header(self):
        self.ids.bet_layout.ids.header.text = f'Gameweek {self.gameweek}'
        if self.gameweek == self.current_gameweek:
            self.ids.bet_layout.ids.header.bold = True
        else:
            self.ids.bet_layout.ids.header.bold = False

    def show_games(self):
        # show all games and their scores

        for i, match_id in enumerate(self.match_id_list):
            match = pl.matches[self.gameweek][match_id]

            self.widgets[i]['time'].text = f"{match['kickoff_time'][0:-3]}, {convert_date(match['kickoff_date'])}"
            self.widgets[i]['team1'].text = pl.teams[match['team1']]["name"]
            self.widgets[i]['goals1'].text = str(match['goals1'])
            self.widgets[i]['goals2'].text = str(match['goals2'])
            self.widgets[i]['team2'].text = pl.teams[match['team2']]["name"]
        
        # clearing the rest of the widgets
        for j in range(i + 1, 20):
            self.widgets[j]['time'].text = ''
            self.widgets[j]['team1'].text = ''
            self.widgets[j]['goals1'].text = ''
            self.widgets[j]['goals2'].text = ''
            self.widgets[j]['team2'].text = ''

    # has to be on main thread to update Kivy graphics
    @mainthread
    def show_previous_predictions(self):
        # if predicted scores were already submitted by user, show them
        app = MDApp.get_running_app()

        if not self.bets:

            # this dict holds users predictions and will be updated 
            # every time the user makes a change
            self.bets = get_all_bets_by_user_id(app.access_token)

            # this is the original that the bets dict will be compared to
            # when choosing what colour the textfield should be
            # (green if the text has been changed, black otherwise)
            self.original = copy.deepcopy(self.bets)

        if self.bets["status_code"] != 200:
            return # TODO create a popup
        
        # clearing the textfields
        for i in range(20):
            self.widgets[i]["prediction1"].text = ''
            self.widgets[i]["prediction2"].text = ''
        
        # displaying the previous predictions
        for i, match_id in enumerate(self.match_id_list):
            self.widgets[i]["prediction1"].disabled = False
            self.widgets[i]["prediction2"].disabled = False
            
            for bet in self.bets["list"]:
                
                if match_id == bet['match_id']:

                    index = self.bets["list"].index(bet)
                    guess = self.original["list"][index]

                    self.widgets[i]["prediction1"].text = str(bet['goal1'])
                    self.widgets[i]["prediction2"].text = str(bet['goal2'])

                    # if the score has been amended then display it as green
                    self.widgets[i]["prediction1"].text_color_normal = [0, 1, 0, 0.7] if str(bet['goal1']) != str(guess['goal1']) else [0, 0, 0, 1]
                    self.widgets[i]["prediction2"].text_color_normal = [0, 1, 0, 0.7] if str(bet['goal2']) != str(guess['goal2']) else [0, 0, 0, 1]
    
    def bind_textfields(self):

        for i in range(0, len(self.match_id_list)):
            self.widgets[i]['prediction1'].bind(on_text_validate=partial(self.store_text_input, i))
            self.widgets[i]['prediction2'].bind(on_text_validate=partial(self.store_text_input, i))

            self.widgets[i]['prediction1'].bind(focus=partial(self.store_text_input, i))
            self.widgets[i]['prediction2'].bind(focus=partial(self.store_text_input, i))
    
    def store_text_input(self, i, instance, focus = False):

        if instance.focus == True:
            return
        
        if not self.bets or not self.match_id_list:
            return
    
        for bet in self.bets["list"]:
            
            # if the prediction already exists
            if self.match_id_list[i] == bet['match_id']:

                index = self.bets["list"].index(bet)
                guess = self.original["list"][index]
                
                if instance == self.widgets[i]['prediction1']:
                    # update to new prediction
                    bet["goal1"] = instance.text
                else:
                    # update to new prediction
                    bet["goal2"] = instance.text

                # update colours
                self.widgets[i]["prediction1"].text_color_normal = [0, 1, 0, 0.7] if str(bet['goal1']) != str(guess['goal1']) else [0, 0, 0, 1]
                self.widgets[i]["prediction2"].text_color_normal = [0, 1, 0, 0.7] if str(bet['goal2']) != str(guess['goal2']) else [0, 0, 0, 1]

                return
        
        # if it's a new prediction then add it to self.bets
        if instance == self.widgets[i]['prediction1']:
            self.bets["list"].append({"match_id": self.match_id_list[i], "goal1": instance.text})
        else:
            self.bets["list"].append({"match_id": self.match_id_list[i], "goal1": instance.text})

    def submit(self):

        app = MDApp.get_running_app()

        matches = []
        list_guess1 = []
        list_guess2 = []

        for i, match_code in enumerate(self.match_id_list):

            prediction1 = self.widgets[i]["prediction1"].text
            prediction2 = self.widgets[i]["prediction2"].text
            if prediction1 == "":
                self.widgets[i]["prediction1"].text = "0"
                prediction1 = 0
            if prediction2 == "":
                self.widgets[i]["prediction2"].text = "0"
                prediction2 = 0

            matches.append(match_code)
            list_guess1.append(prediction1)
            list_guess2.append(prediction2)

            found = False
            for match in self.original["list"]:
                if match["match_id"] == match_code:
                    match["goal1"] = prediction1
                    match["goal2"] = prediction2
                    self.widgets[i]["prediction1"].text_color_normal = [0, 0, 0, 1]
                    self.widgets[i]["prediction2"].text_color_normal = [0, 0, 0, 1]
                    found = True
            
            if found:
                continue

            # if the match code doesn't exist in self.original then add it on
            self.original["list"].append(
                {"match_id": match_code,
                 "goal1": prediction1,
                 "goal2": prediction2}
                )

        print(self.original)
        update_bets = update_multiple_bets(app.access_token, matches, list_guess1, list_guess2)

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
                content_cls = Submission_Dialog(),
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

        # these are different for different users so clearing them
        self.table_dialog = None
        self.bets = None

        # change screen and revoke the access token
        self.manager.current = "LoginWindow"
        app = MDApp.get_running_app()
        revoke_jwt(app.access_token)
    
    def delete_account(self):
        pass
        # app = MDApp.get_running_app()
        # delete_account(app.access_token, app.user_id)
        # self.manager.current = "CreateUser"
