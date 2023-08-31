import requests
import json

'''
Perhaps create a database later?
And can create a db on the server that does the calculation every few minutes? 
This might make the startup faster
'''


def get(url):
    response = requests.get(url)
    return json.loads(response.content)

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

url_1 = 'https://fantasy.premierleague.com/api/fixtures/'

class PremierLeague:

    def __init__(self, teams, matches, positions, connection):
        self.teams = teams
        self.matches = matches
        self.positions = positions
        self.connection = connection

    def get_data(self):

        try:
            response = get(url)
            response_1 = get(url_1)
        except requests.exceptions.ConnectionError:  
            pl.connection = False
            return 0

        self.teams = {}
        stats = ["matches_played", "wins", "draws", "losses",
                 "points", "goals_scored", "goals_conceded", "goals_balance"]
        for team in response["teams"]:
            self.teams[team['id']] = {}
            self.teams[team['id']]['id'] = team['id']
            self.teams[team['id']]['name'] = team['name']
            for stat in stats:
                self.teams[team['id']][stat] = 0
        
        self.matches = {}
        for gmwk in range(1, 39):
            self.matches[gmwk] = {}

        for match in response_1:
            try:
                gameweek = match["event"]
                match_code = str(match["code"])

                self.matches[gameweek][match_code] = {}
                match_stats = self.matches[gameweek][match_code]

                match_stats['team1'] = match['team_h']
                match_stats['team2'] = match['team_a']
                match_stats['goals1'] = match['team_h_score'] or 0 if match["started"] == True else ''
                match_stats['goals2'] = match['team_a_score'] or 0 if match["started"] == True else ''
                match_stats['kickoff_date'] = match['kickoff_time'][0:10]
                match_stats['kickoff_time'] = match['kickoff_time'][11:19]
                match_stats['finished'] = match['finished']
                match_stats['started'] = match['started']

                if match['team_h_score']:

                    if match['team_h_score'] > match['team_a_score']:
                        self.teams[match['team_h']]['points'] += 3
                        self.teams[match['team_h']]['wins'] += 1
                        self.teams[match['team_a']]['losses'] += 1
                    elif match['team_h_score'] < match['team_a_score']:
                        self.teams[match['team_a']]['points'] += 3
                        self.teams[match['team_a']]['wins'] += 1
                        self.teams[match['team_h']]['losses'] += 1
                    else:
                        self.teams[match['team_h']]['points'] += 1
                        self.teams[match['team_a']]['points'] += 1
                        self.teams[match['team_h']]['draws'] += 1
                        self.teams[match['team_a']]['draws'] += 1

                    self.teams[match['team_h']]['matches_played'] += 1
                    self.teams[match['team_a']]['matches_played'] += 1

                    self.teams[match['team_h']]['goals_scored'] += match['team_h_score']
                    self.teams[match['team_a']]['goals_scored'] += match['team_a_score']

                    self.teams[match['team_h']]['goals_conceded'] += match['team_a_score']
                    self.teams[match['team_a']]['goals_conceded'] += match['team_h_score']

                    self.teams[match['team_h']]['goals_balance'] += match['team_h_score'] - match['team_a_score']
                    self.teams[match['team_a']]['goals_balance'] += match['team_a_score'] - match['team_h_score']
            except KeyError:
                pass

        self.positions = {k: v for k, v in sorted(self.teams.items(),
                                                key=lambda item: (item[1]['points'],
                                                                    item[1]['goals_balance'],
                                                                    item[1]['goals_scored']),
                                                                    reverse=True)}
        pl.connection = True # user login will only be successful when the get_data() runs successfully



pl = PremierLeague({}, {}, {}, False)
pl.get_data()




