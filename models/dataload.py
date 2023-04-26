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
from models.team_model import TeamStatistics



class DataLoad:
    def __init__(self, year, metrics, game_metrics, target_metrics):
        self.data_path = 'data/NBA_{}'.format(year)
        self.year = year
        self.team_sequence = {}
        self.cumulative_sequence = {}
        self.combined_team_sequence = {}
        self.target_sequence = {}
        self.num_teams = len(CURR_NBA_TEAMS)
        self.metrics = metrics
        self.game_metrics = game_metrics
        self.target_metrics = target_metrics
        self.obs_len = 10
        self.load(year) 
        
    
    def load(self, year):
        for i in range(self.num_teams):
            team_abbr = TEAM_TO_TEAM_ABBR[CURR_NBA_TEAMS[i].upper()]
            print("Getting data for {}".format(team_abbr))
            team = TeamStatistics(team_abbr, year, num_relevant=7, metrics = self.metrics)
            self.team_sequence[team_abbr], self.target_sequence[team_abbr], self.cumulative_sequence[team_abbr] = self.get_team(team)
        for i in range(self.num_teams):
            team_abbr = TEAM_TO_TEAM_ABBR[CURR_NBA_TEAMS[i].upper()]
            print("Combining data for {}".format(team_abbr))
            team = TeamStatistics(team_abbr, year, num_relevant=7, metrics = self.metrics)
            self.combined_team_sequence[team_abbr] = self.get_combined(team_abbr)
        
    def get_team(self, team_obj):
        data = []
        target = []
        cumulative = []
        for i in range(len(team_obj.game_metrics)):
            selected_player_data = team_obj.game_metrics.loc[i, self.metrics].tolist()
            selected_game_row = team_obj.team_logs[team_obj.team_logs["DATE"] == team_obj.game_metrics.loc[i, "DATE"]]
            selected_game_data = selected_game_row[self.game_metrics].values.ravel()
            selected_target_data = selected_game_row[self.target_metrics].values.ravel()
            # game_weight = team_obj.game_weights[i]

            # spread = [team_obj.team_logs.loc[i, "POINTS_SCORED"] - team_obj.team_logs.loc[i, "OPPONENT_POINTS"]]
            # total = [team_obj.team_logs.loc[i, "POINTS_SCORED"] + team_obj.team_logs.loc[i, "OPPONENT_POINTS"]]
            # data.append(selected_player_data + selected_game_data + spread + total) 
            
            # target.append(selected_target_data)
            if i == 0:
                data.append(list(selected_game_data) + selected_player_data) 
                cumulative.append(selected_player_data)
            elif i == len(team_obj.game_metrics)-1:
                target.append(selected_target_data)
            else:
                data.append(list(selected_game_data) + selected_player_data) 
                sum_list = []
                for j in range(len(selected_player_data)):
                    if j == 0:
                        sum_list.append(selected_player_data[j])
                    else:
                        sum_list.append((selected_player_data[j] + cumulative[i-1][j]*i)/i+1)
                cumulative.append(sum_list)
                target.append(selected_target_data)
        return data, target, cumulative
    
    def get_combined(self, team_abbr):
        combined = []
        game_sequence = self.team_sequence[team_abbr]
        for i in range(len(game_sequence)):
            opponent = game_sequence[i][0]
            date = game_sequence[i][3]
            target = list(self.target_sequence[team_abbr][i])
            target_diff = [target[0]-target[1], target[0]+target[1]]
            opponent_stats = [data for data in self.cumulative_sequence[opponent] if data[0] == date]
            our_stats = [data for data in self.cumulative_sequence[team_abbr] if data[0] == date]
            if(len(our_stats) == 0 or len(opponent_stats) == 0):
                continue          
            stat_diff = []
            for j in range(len(our_stats[0])):
                if j == 0:
                    stat_diff.append(our_stats[0][j])
                if j != 0:
                    stat_diff.append(our_stats[0][j] - opponent_stats[0][j])
            combined.append(list(game_sequence[i][1:3]) + stat_diff + target + target_diff)
        for i in range(len(combined)):
            for j in range(len(combined[i])):
                if j == 0:
                    if(combined[i][j] == True):
                        combined[i][j] = 1
                    else:
                        combined[i][j] = 0
                if j == 1:
                    if combined[i][j][0] == "W":
                        combined[i][j] = int(combined[i][j][2:])
                    else:
                        combined[i][j] = -int(combined[i][j][2:])
                if j == (len(combined[i])-3):
                    if combined[i][j] == "W":
                        combined[i][j] = 1
                    else:
                        combined[i][j] = 0
        return combined
            

player_metrics = ['DATE', 'MP', 'USG%', 'ORtg', 'DRtg', 'GAME_SCORE', 'BPM']
player_metrics = ['DATE','MP','TS%','eFG%','ORB%','DRB%','TRB%','AST%','STL%','BLK%','TOV%','USG%','ORtg','DRtg','GAME_SCORE','BPM']
game_metrics = ["OPPONENT", "HOME", "STREAK"]
target_metrics =  ["POINTS_SCORED", "OPPONENT_POINTS", "OUTCOME"]
data = DataLoad(2023, player_metrics, game_metrics, target_metrics)

# for i in range(len(data.team_sequence["GSW"])):
#     # print(data.team_sequence["GSW"][i], data.target_sequence["GSW"][i], data.cumulative_sequence["GSW"][i], data.combined_team_sequence["GSW"][i])
#     print(data.combined_team_sequence["GSW"][i])



    
