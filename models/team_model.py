import numpy as np
import pandas as pd
import math
import os
import sys
from datetime import datetime

sys.path.append('/Users/jonat/OneDrive - University of Southern California/Documents/USC/Quant/Sports Betting/Sports-Betting')

from basketball_ref_scraper.constants import TEAM_TO_TEAM_ABBR
from basketball_ref_scraper.constants import PLAYER_METRICS

class TeamStatistics:
    def __init__(self, team_name, year, num_relevant = 7, metrics = None):
        if team_name not in TEAM_TO_TEAM_ABBR.values():
            team_name = TEAM_TO_TEAM_ABBR[team_name.upper()]
        self.team_name = team_name
        self.data_path = 'data/NBA_{}/{}_{}'.format(year, self.team_name, year)
        self.roster = pd.read_csv(self.data_path + '/roster.csv').drop("Unnamed: 0", axis = 1)
        self.team_logs = (pd.read_csv(self.data_path + '/team_logs.csv')).drop("Unnamed: 0", axis = 1)
        
        # dictionary of player -> dataframe of player gamelogs, preprocessing
        self.players = self.get_players(self.roster, self.data_path)
        
        # extract relevant players
        relevant_names = self.compute_relevant(self.players, num_relevant)[0]
        self.relevant_players = {key : v for key, v in self.players.items() if key in relevant_names}
        
        # sort players by metrics
        if metrics is None:
            metrics = PLAYER_METRICS
        self.player_metrics = self.select_metrics(self.relevant_players, metrics)

        # dictionary of games -> relevant players
        self.game_players = self.player_of_games(self.team_logs, self.player_metrics)
        print(self.game_players)

    # extract players with data from roster list
    def get_players(self, roster, data_path):
        player_data = []
        player_names = []
        for i in range(len(roster["PLAYER"])):
            player_path = data_path + '/{}.csv'.format(roster["PLAYER"][i])
            if os.path.exists(player_path):
                player_df = pd.read_csv(player_path)
                if not player_df.empty:
                    player_data.append(pd.read_csv(player_path))
                    player_names.append(roster["PLAYER"][i]) 
        # drop extra columns, time conversion
        def time_to_decimal(time_str):
            minutes, seconds = time_str.split(':')
            return int(minutes) + int(seconds)/60
        for i in range(len(player_data)):
            player_data[i] = player_data[i].drop("Unnamed: 0", axis = 1)
            player_data[i]["MP"] = player_data[i]["MP"].apply(time_to_decimal)
        players = dict(zip(player_names, player_data))
        return players 
    
    # find relevant players, remove others by game participation
    def compute_relevant(self, players, num_relevant = 7):
        player_name = list(players.keys())
        player_relevance = []
        if len(players) <= num_relevant:
            return players    
        for i in range(len(players)):
            games_played = len(players[player_name[i]])
            minutes_played = sum(players[player_name[i]]["MP"])
            # games_started = sum(players[player_name[i]]["GS"])
            # print(games_played, minutes_played)
            player_relevance.append(minutes_played)
        combined = sorted(zip(player_name, player_relevance), key=lambda x: x[1], reverse=True)
        player_name, player_relevance = zip(*combined)
        return player_name[:num_relevant], player_relevance[:num_relevant]
    
    # select a particular set of metrics 
    def select_metrics(self, players, metrics):
        player_name = list(players.keys())
        for i in range(len(players)):
            players[player_name[i]] = players[player_name[i]][metrics]
        return players
    
    # get players for each game the team played in the regular season
    def player_of_games(self, team_logs, players):
        num_games = len(team_logs)
        player_name = list(players.keys())
        game_players = {}
        for i in range(num_games):
            date = "{}-{}-{}".format(team_logs["YEAR"][i], team_logs["MONTH"][i], team_logs["DAY"][i])
            date = datetime.strptime(date, '%Y-%m-%d')
            date = date.strftime('%Y-%m-%d')  
            team_logs["DATE"][i] = date
            relevant_players = []
            for j in range(len(players)):
                if date in players[player_name[j]]["DATE"].values:
                    relevant_players.append(player_name[j])
            game_players[date] = relevant_players
        return game_players
        
        
team = TeamStatistics("Golden State Warriors", 2022)