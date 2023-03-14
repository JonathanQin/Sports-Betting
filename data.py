from basketball_ref_scraper.constants import TEAM_TO_TEAM_ABBR
from basketball_ref_scraper.constants import CURR_NBA_TEAMS

from basketball_ref_scraper.teams import get_roster
from basketball_ref_scraper.games import get_games
from basketball_ref_scraper.players import get_game_logs

import numpy as np
import pandas as pd
import os

class Dataset:
    def __init__(self, team, year):
        self.team = team
        self.year = year
        self.roster = get_roster(team, year)
        self.team_logs = get_games(team, year)
        self.player_logs = {}
        for player in self.roster["PLAYER"]:
            self.player_logs[player] = get_game_logs(player, year)
        self.save_data()
        
    def save_data(self):
        save_path = 'data/{}_{}'.format(self.team, self.year)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        self.team_logs.to_csv(save_path + '/team_logs.csv')
        self.roster.to_csv(save_path + '/roster.csv')
        for player in self.roster["PLAYER"]:
            if self.player_logs[player] is not None:
                if not isinstance(self.player_logs[player], str):
                    self.player_logs[player].to_csv(save_path + '/{}.csv'.format(player))
        
if __name__ == "__main__":
    year = 2022
    for team in CURR_NBA_TEAMS:
        team_abbr = TEAM_TO_TEAM_ABBR[team.upper()]
        Dataset(team_abbr, year)
                


    # def save(input_sequence, input_user, output, extra, social_dict, save_path):
    # if not os.path.exists(save_path):
    #     os.mkdir(save_path)
    # np.save(os.path.join(save_path, "input_seq.npy"), input_sequence)
    # np.save(os.path.join(save_path, "input_user.npy"), input_user)
    # np.save(os.path.join(save_path, "output.npy"), output)
    # np.save(os.path.join(save_path, "extra.npy"), extra)
    # with open(os.path.join(save_path, "social.json"), "w") as f:
    #     json.dump(social_dict, f, indent=1)
        