import numpy as np
import pandas as pd
import math
import sys
sys.path.append('/Users/jonat/OneDrive - University of Southern California/Documents/USC/Quant/Sports Betting/Sports-Betting')
from basketball_ref_scraper.constants import TEAM_TO_TEAM_ABBR
from basketball_ref_scraper.constants import CURR_NBA_TEAMS
from team_model import TeamStatistics

# num series won, # games per series
PLAYOFFS_2022 = {
    'MIA' : 2,
    'ATL' : 0,
    'PHI' : 1,
    'TOR' : 0,
    'MIL' : 1,
    'CHI' : 0,
    'BOS' : 3,
    'BRK' : 0,
    'PHO' : 1,
    'NOP' : 0,
    'DAL' : 2,
    'UTA' : 0,
    'GSW' : 4,
    'DEN' : 0,
    'MEM' : 1,
    'MIN' : 0,
}

# margin of victory
# num of games margin of victory
# team strength and seeding
# depth of run

class Playoffs:
    def __init__(self, bracket):
        self.num_teams = 16
        self.bracket = bracket
        self.data_path = 'data\NBA_playoffs_2022'
        self.teams = self.load()
        
    # simulates a particular level of a bracket of 2^i teams playing a best of n
    def load(self):
        playoff_log = {}
        teams = self.bracket.keys()
        series = self.bracket.values()
        for i in range(self.num_teams):
            for j in range(series[i] + 1):
                
            
        
playoffs_2022 = Playoffs(PLAYOFFS_2022)