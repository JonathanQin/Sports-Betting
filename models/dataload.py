from tqdm import tqdm
import numpy as np
import json
import os
import datetime
import pandas as pd
import sys
sys.path.append('/Users/jonat/OneDrive - University of Southern California/Documents/USC/Quant/Sports Betting/Sports-Betting')
from basketball_ref_scraper.constants import TEAM_TO_TEAM_ABBR
from basketball_ref_scraper.constants import CURR_NBA_TEAMS
from team_model import TeamStatistics



class DataLoad:
    def __init__(self, year, metrics, game_metrics = None):
        self.data_path = 'data/NBA_{}'.format(year)
        self.team_sequence = {}
        self.num_teams = len(CURR_NBA_TEAMS)
        self.metrics = metrics
        self.game_metrics = game_metrics
        if self.game_metrics == None:
            self.game_metrics = ["HOME", "STREAK", "POINTS_SCORED", "OPPONENT_POINTS", "OUTCOME"]
        self.obs_len = 10
        self.load(year)
        
    def load(self, year):
        for i in range(self.num_teams):
            team_abbr = TEAM_TO_TEAM_ABBR[CURR_NBA_TEAMS[i].upper()]
            team = TeamStatistics(team_abbr, year, num_relevant=7, metrics = self.metrics)
            self.team_sequence[team_abbr] = self.get_team(team)
        
    def get_team(self, team_obj):
        data = []
        for i in range(len(team_obj.game_metrics)):
            selected_player_data = team_obj.game_metrics.loc[i, self.metrics].tolist()
            selected_game_row = team_obj.team_logs[team_obj.team_logs["DATE"] == team_obj.game_metrics.loc[i, "DATE"]]
            selected_game_data = list(selected_game_row[self.game_metrics])
            # spread = [team_obj.team_logs.loc[i, "POINTS_SCORED"] - team_obj.team_logs.loc[i, "OPPONENT_POINTS"]]
            # total = [team_obj.team_logs.loc[i, "POINTS_SCORED"] + team_obj.team_logs.loc[i, "OPPONENT_POINTS"]]
            # data.append(selected_player_data + selected_game_data + spread + total) 
            data.append(selected_player_data + selected_game_data) 
        print(len(data))
        return data

player_metrics = ['DATE', 'MP', 'USG%', 'ORtg', 'DRtg', 'GAME_SCORE', 'BPM']
game_metrics = ["HOME", "STREAK", "POINTS_SCORED", "OPPONENT_POINTS", "OUTCOME"]
data = DataLoad(2022, player_metrics, game_metrics)
    
