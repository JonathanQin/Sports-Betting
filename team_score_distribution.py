import numpy as np
import pandas as pd
import random
import math
from basketball_ref_scraper import teams
from basketball_ref_scraper import games
from basketball_ref_scraper import players


class TeamDistribtuion:
    def __init__(self, team, year):
        self.team = team
        self.year = year
        self.roster = teams.get_roster(team, year)
        self.roster_size = len(self.roster.index)
        self.player_logs = {}
        for player in self.roster["PLAYER"]:
            self.player_logs[player] = players.get_game_logs(player, year)
        # self.player_logs = pd.DataFrame.from_dict(self.player_logs)
        # self.player_logs.head()
        print(self.player_logs)

        
team = TeamDistribtuion("ATL", 2022)
