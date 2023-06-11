import requests
import json


def get(url):
    response = requests.get(url)
    return json.loads(response.content)

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

url_1 = 'https://fantasy.premierleague.com/api/fixtures/'

class premier_league:
    def __init__(self, teams, matches, positions, connection):
        self.teams = teams
        self.matches = matches
        self.positions = positions
        self.connection = connection
    def get_data(self):
        try:
            response = get(url)
            response_1 = get(url_1)
            self.teams = {}
            for i in response["teams"]:
                self.teams[i['id']] = {}
                self.teams[i['id']]['id'] = i['id']
                self.teams[i['id']]['name'] = i['name']
                self.teams[i['id']]['matches_played'] = 0
                self.teams[i['id']]['wins'] = 0
                self.teams[i['id']]['draws'] = 0
                self.teams[i['id']]['losses'] = 0
                self.teams[i['id']]['points'] = 0
                self.teams[i['id']]['goals_scored'] = 0
                self.teams[i['id']]['goals_conceded'] = 0
                self.teams[i['id']]['goals_balance'] = 0
                self.matches = {}
            for i in range(1, 39):
                self.matches['Gameweek ' + str(i)] = {}

            for i in response_1:
                self.matches['Gameweek ' + str(i['event'])][str(i['code'])] = {}
                self.matches['Gameweek ' + str(i['event'])][str(i['code'])]['team1'] = i['team_h']
                self.matches['Gameweek ' + str(i['event'])][str(i['code'])]['team2'] = i['team_a']
                self.matches['Gameweek ' + str(i['event'])][str(i['code'])]['goals1'] = i['team_h_score']
                self.matches['Gameweek ' + str(i['event'])][str(i['code'])]['goals2'] = i['team_a_score']
                self.matches['Gameweek ' + str(i['event'])][str(i['code'])]['kickoff_date'] = i['kickoff_time'][0:10]
                self.matches['Gameweek ' + str(i['event'])][str(i['code'])]['kickoff_time'] = i['kickoff_time'][11:19]
                self.matches['Gameweek ' + str(i['event'])][str(i['code'])]['finished'] = i['finished']

                self.matches['Gameweek ' + str(i['event'])][str(i['code'])]['started'] = i['started']

                if i['team_h_score'] != None:

                    if i['team_h_score'] > i['team_a_score']:
                        self.teams[i['team_h']]['points'] += 3
                        self.teams[i['team_h']]['wins'] += 1
                        self.teams[i['team_a']]['losses'] += 1
                    elif i['team_h_score'] < i['team_a_score']:
                        self.teams[i['team_a']]['points'] += 3
                        self.teams[i['team_a']]['wins'] += 1
                        self.teams[i['team_h']]['losses'] += 1
                    else:
                        self.teams[i['team_h']]['points'] += 1
                        self.teams[i['team_a']]['points'] += 1
                        self.teams[i['team_h']]['draws'] += 1
                        self.teams[i['team_a']]['draws'] += 1

                    self.teams[i['team_h']]['matches_played'] += 1
                    self.teams[i['team_a']]['matches_played'] += 1

                    self.teams[i['team_h']]['goals_scored'] += i['team_h_score']
                    self.teams[i['team_a']]['goals_scored'] += i['team_a_score']

                    self.teams[i['team_h']]['goals_conceded'] += i['team_a_score']
                    self.teams[i['team_a']]['goals_conceded'] += i['team_h_score']

                    self.teams[i['team_h']]['goals_balance'] += i['team_h_score'] - i['team_a_score']
                    self.teams[i['team_a']]['goals_balance'] += i['team_a_score'] - i['team_h_score']
                
            self.positions = {k: v for k, v in sorted(self.teams.items(),
                                                    key=lambda item: (item[1]['points'],
                                                                        item[1]['goals_balance'],
                                                                        item[1]['goals_scored']),
                                                                        reverse=True)}
            pl.connection = True # user login will only be successful when the get_data() runs successfully
        except requests.exceptions.ConnectionError:  
            pl.connection = False


pl = premier_league({}, {}, {}, False)
pl.get_data()




