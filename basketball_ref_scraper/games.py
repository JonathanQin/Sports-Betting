import pandas as pd
from requests import get
from bs4 import BeautifulSoup

try:
    from constants import TEAM_TO_TEAM_ABBR, TEAM_SETS, MONTH_ABBR_TO_NUM
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
        df = df[df['DATE'] != "Date"]

        df['HOME'] = df['HOME'].apply(
            lambda x: False if pd.notna(x) else True)
        df['OPPONENT'] = df['OPPONENT'].apply(
            lambda x: TEAM_TO_TEAM_ABBR.get(x.upper()))
        df['OVERTIME'] = df['OVERTIME'].apply(
            lambda x: True if pd.notna(x) else False)

        # parse date into year, month, day
        df.insert(1,'YEAR', 0)
        df['YEAR'] = df.apply(
            lambda row: row.DATE[-4:], axis=1)
        df.insert(2,'MONTH',0)
        df['MONTH'] = df.apply(
            lambda row: row.DATE[5:8], axis=1)
        df['MONTH'] = df['MONTH'].apply(
            lambda x: MONTH_ABBR_TO_NUM.get(x.upper()))
        df.insert(3,'DAY',0)
        df['DAY'] = df.apply(
            lambda row: row.DATE.split()[2][:-1], axis=1)
    return df