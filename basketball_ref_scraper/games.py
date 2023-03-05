import pandas as pd
from requests import get
from bs4 import BeautifulSoup

try:
    from constants import TEAM_TO_TEAM_ABBR, TEAM_SETS
    from utils import remove_accents
except:
    from basketball_ref_scraper.constants import TEAM_TO_TEAM_ABBR, TEAM_SETS
    from basketball_ref_scraper.utils import remove_accents


def get_games(team, season_end_year):
    r = get(f'https://www.basketball-reference.com/teams/{team}/{season_end_year}_games.html')
    df = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        df = df.drop(columns=['G', 'Unnamed: 3', 'Unnamed: 4', 'Notes'])
        df.columns = ['DATE', 'START_ET', 'HOME', 'OPPONENT', 'OUTCOME',
        'OVERTIME', 'POINTS_SCORED', 'OPPONENT_POINTS',
        'CUMULATIVE_W', 'CUMULATIVE_L', 'STREAK']
        df['HOME'] = df['HOME'].apply(
            lambda x: False if pd.notna(x) else True)
        df['OPPONENT'] = df['OPPONENT'].apply(
            lambda x: TEAM_TO_TEAM_ABBR.get(x.upper()))
        df['OVERTIME'] = df['OVERTIME'].apply(
            lambda x: True if pd.notna(x) else False)
    return df