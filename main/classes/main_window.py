from api.pl_api import *
from api.db_api import *

from kivy.properties import NumericProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import mainthread

from functools import partial
from threading import Thread
from datetime import datetime

def convert_date(date):
    return f"{date[8:10]}/{date[5:7]}/{date[0:4]}"

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

    table_dialog = None
    bets = None

    colour = (0, 0, 1, 1)

    '''
    NavItem - 'Table'
    '''

    def _add_me(self, grid, me):
        for header in self.list:
            self.label = MDLabel(
                    text = str(me[header]),
                    theme_text_color = 'Custom',
                    text_color = self.colour
                    )
            self.label.font_size = "12dp"
            grid.add_widget(self.label)

    def users_table(self):

        app = MDApp.get_running_app()

        # getting the 10 best users
        first10 = first_ten(app.access_token)

        # headers/keys
        self.list = ["position", "username", "points", "three_pointers", "one_pointers"]

        # main container
        grid = self.ids.grid
        grid.clear_widgets()

        # getting the actual user and their position
        me = my_user_info(app.access_token, app.user_id)
        self.my_pos = int(me["position"])

        # adding the 10 users to the table
        for i in first10:
            t_t_c = 'Custom' if i["username"] == me["username"] else None
            t_c = self.colour if i["username"] == me["username"] else None
            for header in self.list:
                self.label = MDLabel(text = str(i[header]), theme_text_color = t_t_c, text_color = t_c)
                self.label.font_size = "12dp"
                grid.add_widget(self.label)
       
        # if the user is 11th in the table then we add him
        if me["position"] == 11:
            self._add_me(grid, me)
        # else we leave one row empty ('...') and add the user on next line
        elif me["position"] > 11:
            grid.add_widget(
                MDLabel(
                text = '...',
                font_size = "12dp"
                )
            )
            for j in range(4):
                grid.add_widget(MDLabel())
            self._add_me(grid, me)
    
    def show_full(self):
        app = MDApp.get_running_app()

        if not self.table_dialog:

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

    def pl_table(self):
        # add the widgets first and then use threading to add info

        if self.name_widgets:
            return
        
        # for holding the widgets
        self.name_widgets = {}
        self.stats_widgets = {}

        # dealing with headings
        self.ids.my_layout.ids.gridlayout.add_widget(MDLabel(text = 'Pos', size_hint_x = 0.3))
        self.ids.my_layout.ids.gridlayout.add_widget(MDLabel(text = 'Club', size_hint_x = 0.7))
        for heading in ['MP', 'W', 'D', 'L', 'Pts', 'GA', 'GF', 'GD']:
            self.ids.my_layout.ids.gridlayout2.add_widget(MDLabel(text = heading))


        self.headers = ["matches_played", "wins", "draws", "losses",
                 "points", "goals_scored", "goals_conceded", "goals_balance"]
        # creating widgets for position and name of club, then storing them in a dict
        for position in range(1, 21):
            self.name_widgets[position] = {}
            self.name_widgets[position]['POS'] = MDLabel(text = str(position), size_hint_x = 0.3)
            self.name_widgets[position]['CLUB'] = MDLabel(size_hint_x = 0.7)
            self.ids.my_layout.ids.gridlayout.add_widget(self.name_widgets[position]['POS'])
            self.ids.my_layout.ids.gridlayout.add_widget(self.name_widgets[position]['CLUB'])
        
        # creating widgets for the club stats, then storing them in a dict
        for position in range(1, 21):
            self.stats_widgets[position] = {}
            for header in self.headers:
                self.stats_widgets[position][header] = MDLabel()
                self.ids.my_layout.ids.gridlayout2.add_widget(self.stats_widgets[position][header])
        
        # adding the info in a separate thread for smoother experience
        thread = Thread(target = self.show_info)
        thread.start()
    
    def show_info(self):
        
        position = 1
        for club in pl.positions.values():

            # showing the club name
            self.name_widgets[position]['CLUB'].text = str(club["name"])

            # showing the stats info
            for header in self.headers:
                self.stats_widgets[position][header].text = str(club[header])
                self.stats_widgets[position][header].bold = True if header == "points" else False

            position += 1        
    
    '''
    NavItem - 'PostBet'
    '''

    def show_gameweek_games(self):

        thread = Thread(target = self.display)
        thread.start()

    def display(self):

        # find out what gameweek it is if the function is run for the first time
        if not self.gameweek:
            self.what_gameweek()
        
        # list with all match ids from current gameweek
        self.match_id_list = [match_id for match_id in pl.matches[self.gameweek].keys()]

        # # store widgets in a dict for easier access
        if not self.widgets:
            self.store_widgets()

        # display the gameweek header
        self.handle_header()
        
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
                        self.gameweek = week
                        raise Found
        except Found:
            pass
    
    def store_widgets(self):

        # storing all box_layouts in a dict for easier access
        self.widgets = {}

        i = 19
        for box_layout in self.ids.bet_layout.ids.main.children:
            self.widgets[i] = {}
            self.widgets[i]['box'] = box_layout
            self.widgets[i]['hour'] = box_layout.children[0]

            self.widgets[i]['team1'] = box_layout.children[1].children[5]
            self.widgets[i]['goals1'] = box_layout.children[1].children[4]
            self.widgets[i]['prediction1'] = box_layout.children[1].children[3]
            self.widgets[i]['prediction2'] = box_layout.children[1].children[2]
            self.widgets[i]['goals2'] = box_layout.children[1].children[1]
            self.widgets[i]['team2'] = box_layout.children[1].children[0]
            
            i -= 1
    
    def bind_textfields(self):

        for i in range(0, len(self.match_id_list)):
            self.widgets[i]['prediction1'].bind(on_text_validate=partial(self.store_text_input, i))
            self.widgets[i]['prediction2'].bind(on_text_validate=partial(self.store_text_input, i))

    def previous_gameweek(self):

        if self.gameweek == 1:
            pass
        else:
            self.gameweek -= 1


    def next_gameweek(self):

        if self.gameweek == 38:
            pass
        else:
            self.gameweek += 1
    
    def handle_header(self):
        self.ids.bet_layout.ids.header.text = f'Gameweek {self.gameweek}'
    
    def show_games(self):
        # show all games and their scores

        for i, match_id in enumerate(self.match_id_list):
            match = pl.matches[self.gameweek][match_id]

            self.widgets[i]['hour'].text = f"{match['kickoff_time'][0:-3]} {convert_date(match['kickoff_date'])}"
            self.widgets[i]['team1'].text = pl.teams[match['team1']]["name"]
            self.widgets[i]['goals1'].text = str(match['goals1'])
            self.widgets[i]['goals2'].text = str(match['goals2'])
            self.widgets[i]['team2'].text = pl.teams[match['team2']]["name"]
        
        # clearing the rest of the widgets
        for j in range(i + 1, 20):
            self.widgets[j]['hour'].text = ''
            self.widgets[j]['team1'].text = ''
            self.widgets[j]['goals1'].text = ''
            self.widgets[j]['goals2'].text = ''
            self.widgets[j]['team2'].text = ''

    # has to be on main thread to update Kivy graphics
    @mainthread
    def show_previous_predictions(self):
        
        app = MDApp.get_running_app()

        if not self.bets:
            self.bets = get_all_bets_by_user_id(app.access_token)

        if self.bets["status_code"] != 200:
            return
        
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
                    self.widgets[i]["prediction1"].text = str(bet['goal1'])
                    self.widgets[i]["prediction2"].text = str(bet['goal2'])
    
    def store_text_input(self, i, instance):
        
        if not self.bets or not self.match_id_list:
            return
    
        for bet in self.bets["list"]:
            if self.match_id_list[i] == bet['match_id']:
                if instance == self.widgets[i]['prediction1']:
                    bet["goal1"] = instance.text
                else:
                    bet["goal2"] = instance.text
                return
        
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

            for match in self.bets["list"]:
                if match["match_id"] == match_code:
                    match["goal1"] = prediction1
                    match["goal2"] = prediction2
                    continue
            
            # if the match code doesn't exist in self.bets yet then:
            self.bets["list"].append(
                {"match_id": match_code,
                 "goal1": prediction1,
                 "goal2": prediction2}
                )


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

        # These are different for different users so clearing them
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
