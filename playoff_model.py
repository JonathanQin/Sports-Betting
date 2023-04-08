import numpy as np
import pandas as pd
import math

class TeamStatistics:
    def __init__(self, team_name, year):
        pass

class Playoffs:
    def __init__(self, bracket, model):
        self.num_teams = 9
        self.bracket = bracket
        self.best_of = 7
        self.model = model
        
    # simulates a particular level of a bracket of 2^i teams playing a best of n
    def simulate_round(self, round_teams, model):
        num_games = math.log(len(round_teams), 2)
        results = []
        winners = []
        if not num_games.is_integer():
            raise ValueError("Teams in play must be a power of 2")
        for i in range(num_games):
            team_A = round_teams[i*2]
            team_B = round_teams[i*2 + 1]
            winner, win_probability, point_spread, over_under = model(team_A, team_B, self.best_of)
            winners.append(winner)
            results.append([winner, win_probability, point_spread, over_under])
        self.result_display(results)
        return winners
    
    # prints out / saves simulation results for analysis
    def result_display(self, results):
        pass
        
class Model:
    def __init__(self, team_A, team_B, best_of = 7):
        self.num_games = best_of
        self.team_A = team_A
        self.team_B = team_B
    