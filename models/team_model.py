import numpy as np
import pandas as pd
import math
import os
import sys
from player_model import Player
from datetime import datetime

sys.path.append('/Users/jonat/OneDrive - University of Southern California/Documents/USC/Quant/Sports Betting/Sports-Betting')

from basketball_ref_scraper.constants import TEAM_TO_TEAM_ABBR
from basketball_ref_scraper.constants import PLAYER_METRICS

class TeamStatistics:
    def __init__(self, team_name, year, num_relevant = 7, metrics = PLAYER_METRICS):
        if team_name not in TEAM_TO_TEAM_ABBR.values():
            team_name = TEAM_TO_TEAM_ABBR[team_name.upper()]
        self.team_name = team_name
        self.year = year
        self.data_path = 'data/NBA_{}/{}_{}'.format(year, self.team_name, year)
        self.roster = pd.read_csv(self.data_path + '/roster.csv').drop("Unnamed: 0", axis = 1)
        self.team_logs = (pd.read_csv(self.data_path + '/team_logs.csv')).drop("Unnamed: 0", axis = 1)
        self.process_team_logs()
        
        # list / dictionary of player objects
        self.players = self.get_players(self.roster, self.data_path)
        
        # extract relevant players, data
        self.relevant_players, player_weights = self.compute_relevant(self.players, num_relevant)
        self.player_weights = [weight / sum(player_weights) for weight in player_weights]

        self.relevant_player_names = [player.name for player in self.relevant_players]
        
        # get specific player metrics
        self.select_metrics(self.relevant_players, metrics)

        # dictionary of games (date) -> relevant players
        self.game_players = self.player_of_games(self.team_logs, self.relevant_players, self.relevant_player_names)
        
        self.game_metrics = self.game_data(self.game_players, self.relevant_players, self.relevant_player_names, self.player_weights)

    # extract players with data from roster list
    def get_players(self, roster, data_path):
        players = []
        for i in range(len(roster["PLAYER"])):
            player_path = data_path + '/{}.csv'.format(roster["PLAYER"][i])
            if os.path.exists(player_path):
                player_df = pd.read_csv(player_path)
                if not player_df.empty:
                    players.append(Player(roster["PLAYER"][i], self.team_name, self.year))
        return players 
    
    # extract players as a dictionary
    def get_players_dict(self, roster, data_path):
        player_data = []
        player_names = []
        for i in range(len(roster["PLAYER"])):
            player_path = data_path + '/{}.csv'.format(roster["PLAYER"][i])
            if os.path.exists(player_path):
                player_df = pd.read_csv(player_path)
                if not player_df.empty:
                    player_data.append(Player(roster["PLAYER"][i], self.team_name, self.year))
                    player_names.append(roster["PLAYER"][i]) 
        players = dict(zip(player_names, player_data))
        return players 
    
    # find relevant players, remove others by game participation
    def compute_relevant(self, players, num_relevant = 7):
        player_relevance = []
        if len(players) <= num_relevant:
            return players    
        for i in range(len(players)):
            games_played = len(players[i].data)
            minutes_played = sum(players[i].data["MP"])
            player_relevance.append(minutes_played)
        combined = sorted(zip(players, player_relevance), key=lambda x: x[1], reverse=True)
        players, player_relevance = zip(*combined)
        return players[:num_relevant], player_relevance[:num_relevant]
    
    # select a particular set of metrics 
    def select_metrics(self, players, metrics):
        for i in range(len(players)):
            players[i].apply_metrics(metrics)
    
    # get players for each game the team played in the regular season
    def player_of_games(self, team_logs, players, player_names):
        num_games = len(team_logs)
        game_players = {}
        for i in range(num_games):
            relevant_players = []
            for j in range(len(players)):
                if team_logs.loc[i, "DATE"] in players[j].data["DATE"].values:
                    relevant_players.append(player_names[j])
            game_players[team_logs["DATE"][i]] = relevant_players
        return game_players
    
    def game_data(self, games, players, player_names, weights):
        for date in games.keys():
            # get player stats for each game
            # players_id = []
            player_stats = []
            player_weights = []
            for player in games[date]:
                for i in range(len(player_names)):
                    if player_names[i] == player:
                        # players_id.append(i)
                        player_stats.append(players[i].metrics_data[players[i].metrics_data["DATE"] == date])
                        player_weights.append(weights[i])
            game_weight = sum(player_weights)
            player_weights = [weight/game_weight for weight in player_weights]
                    
        
    
    # preprocess team_logs data
    def process_team_logs(self):
        def format_time(year, month, day):
            date = "{}-{}-{}".format(year, month, day)
            date = datetime.strptime(date, '%Y-%m-%d')
            return date.strftime('%Y-%m-%d')
        for i in range(len(self.team_logs)):
            date = format_time(self.team_logs["YEAR"][i], self.team_logs["MONTH"][i], self.team_logs["DAY"][i])
            self.team_logs.loc[i,"DATE"] = date
    
            
team = TeamStatistics("Golden State Warriors", 2022)

# old function implementations

    # # find relevant players, remove others by game participation
    # def compute_relevant(self, players, num_relevant = 7):
    #     player_name = list(players.keys())
    #     player_relevance = []
    #     if len(players) <= num_relevant:
    #         return players    
    #     for i in range(len(players)):
    #         games_played = len(players[player_name[i]])
    #         minutes_played = sum(players[player_name[i]]["MP"])
    #         # games_started = sum(players[player_name[i]]["GS"])
    #         # print(games_played, minutes_played)
    #         player_relevance.append(minutes_played)
    #     combined = sorted(zip(player_name, player_relevance), key=lambda x: x[1], reverse=True)
    #     player_name, player_relevance = zip(*combined)
    #     return player_name[:num_relevant], player_relevance[:num_relevant]
    
    # def compute_relevant_dict(self, players, num_relevant = 7):
    #     player_name = list(players.keys())
    #     player_relevance = []
    #     if len(players) <= num_relevant:
    #         return players    
    #     for i in range(len(players)):
    #         games_played = len(players[player_name[i]].data)
    #         minutes_played = sum(players[player_name[i]].data["MP"])
    #         player_relevance.append(minutes_played)
    #     combined = sorted(zip(player_name, player_relevance), key=lambda x: x[1], reverse=True)
    #     player_name, player_relevance = zip(*combined)
    #     return player_name[:num_relevant], player_relevance[:num_relevant]