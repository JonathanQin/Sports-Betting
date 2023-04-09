import numpy as np
import pandas as pd
import math
import os
import sys
from datetime import datetime

sys.path.append('/Users/jonat/OneDrive - University of Southern California/Documents/USC/Quant/Sports Betting/Sports-Betting')

from basketball_ref_scraper.constants import TEAM_TO_TEAM_ABBR
from basketball_ref_scraper.constants import PLAYER_METRICS

class Player:
    def __init__(self, player_name, team_name, year):
        self.name = player_name
        self.team = team_name
        self.year = year
        self.data_path = 'data/NBA_{}/{}_{}'.format(year, self.team, self.year)
        self.data = pd.read_csv(self.data_path + '/{}.csv'.format(self.name)).drop("Unnamed: 0", axis = 1)
        self.preprocess_data()
        self.metrics_data = self.data
    
    def preprocess_data(self):
        def time_to_decimal(time_str):
            minutes, seconds = time_str.split(':')
            return int(minutes) + int(seconds)/60
        self.data["MP"] = self.data["MP"].apply(time_to_decimal)

    def apply_metrics(self, metrics = PLAYER_METRICS):
        self.metrics_data = self.data[metrics]
        return self.metrics_data