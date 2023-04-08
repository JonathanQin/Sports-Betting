import numpy as np
import pandas as pd
import math
import os
import sys

sys.path.append('/Users/jonat/OneDrive - University of Southern California/Documents/USC/Quant/Sports Betting/Sports-Betting')

from basketball_ref_scraper.constants import TEAM_TO_TEAM_ABBR

class TeamStatistics:
    def __init__(self, team_name, year):
        if team_name not in TEAM_TO_TEAM_ABBR.values():
            team_name = TEAM_TO_TEAM_ABBR[team_name.upper()]
        self.team_name = team_name
        self.data_path = 'data/NBA_{}/{}_{}'.format(year, self.team_name, year)
        self.roster = pd.read_csv(self.data_path + '/roster.csv')
        self.team_logs = pd.read_csv(self.data_path + '/team_logs.csv')
        self.players = self.get_players(self.roster)
        print(self.players.keys())

        
    def get_players(self, roster):
        player_data = []
        player_names = []
        for i in range(len(roster["PLAYER"])):
            player_path = self.data_path + '/{}.csv'.format(roster["PLAYER"][i])
            if os.path.exists(player_path):
                player_df = pd.read_csv(player_path)
                if not player_df.empty:
                    player_data.append(pd.read_csv(player_path))
                    player_names.append(roster["PLAYER"][i])
        for i in range(len(player_data)):
            player_data[i] = player_data[i].drop("Unnamed: 0", axis = 1)
        players = dict(zip(player_names, player_data))
        return players 
        
team = TeamStatistics("Golden State Warriors", 2022)