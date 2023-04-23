import pandas as pd
from requests import get
from bs4 import BeautifulSoup

try:
    from constants import TEAM_TO_TEAM_ABBR, TEAM_SETS
    from utils import remove_accents
except:
    from basketball_ref_scraper.constants import TEAM_TO_TEAM_ABBR, TEAM_SETS
    from basketball_ref_scraper.utils import remove_accents

# edited get_roster function to resolve null player names
def get_roster(team, season_end_year):
    r = get(
        f'https://www.basketball-reference.com/teams/{team}/{season_end_year}.html')
    df = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        df.columns = ['NUMBER', 'PLAYER', 'POS', 'HEIGHT', 'WEIGHT', 'BIRTH_DATE',
                        'NATIONALITY', 'EXPERIENCE', 'COLLEGE']
        df['BIRTH_DATE'] = df['BIRTH_DATE'].apply(
            lambda x: pd.to_datetime(x) if pd.notna(x) else pd.NaT)
        df['NATIONALITY'] = df['NATIONALITY'].apply(
            lambda x: x.upper() if pd.notna(x) else '')
    return df
    
# original web-scraper code commented out

def get_roster_original(team, season_end_year):
    r = get(
        f'https://www.basketball-reference.com/teams/{team}/{season_end_year}.html')
    df = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        df.columns = ['NUMBER', 'PLAYER', 'POS', 'HEIGHT', 'WEIGHT', 'BIRTH_DATE',
                      'NATIONALITY', 'EXPERIENCE', 'COLLEGE']
        # remove rows with no player name (this was the issue above)
        df = df[df['PLAYER'].notna()]
        df['PLAYER'] = df['PLAYER'].apply(
            lambda name: remove_accents(name, team, season_end_year))
        # handle rows with empty fields but with a player name.
        df['BIRTH_DATE'] = df['BIRTH_DATE'].apply(
            lambda x: pd.to_datetime(x) if pd.notna(x) else pd.NaT)
        df['NATIONALITY'] = df['NATIONALITY'].apply(
            lambda x: x.upper() if pd.notna(x) else '')

    return df

def get_team_stats(season_end_year):
    r = get(
        f'https://www.basketball-reference.com/leagues/NBA_{season_end_year}.html')
    merged_df = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find_all('table')
        advanced_stats_df = pd.read_html(str(table))[-3]
        per_game_df_100 = pd.read_html(str(table))[8]
        opp_per_game_df_100 = pd.read_html(str(table))[9]

        advanced_stats_df.columns = advanced_stats_df.columns.droplevel(0)

        advanced_stats_df['Team'] = advanced_stats_df['Team'].str.replace("\*", '')
        per_game_df_100['Team'] = advanced_stats_df['Team'].str.replace('\*', '')
        opp_per_game_df_100['Team'] = advanced_stats_df['Team'].str.replace('\*', '')
        opp_per_game_df_100.columns = opp_per_game_df_100.columns.str.replace('Opp', '')
        opp_per_game_df_100 = opp_per_game_df_100.rename(columns=lambda x: 'opp_' + x)
        opp_per_game_df_100 = opp_per_game_df_100.rename(columns={'opp_Team': 'Team'})

        advanced_stats_df.drop(['Rk'], axis=1, inplace=True)
        advanced_stats_df.drop(['Arena'], axis=1, inplace=True)
        advanced_stats_df.drop(['Attend.'], axis=1, inplace=True)
        advanced_stats_df.drop(['Unnamed: 22_level_1'], axis=1, inplace=True)
        advanced_stats_df.drop(['Unnamed: 27_level_1'], axis=1, inplace=True)
        advanced_stats_df.drop(['Unnamed: 17_level_1'], axis=1, inplace=True)
        advanced_stats_df.drop(30)
        opp_per_game_df_100.drop(['opp_Rk'], axis=1, inplace=True)
        per_game_df_100.drop(['Rk'], axis=1, inplace=True)

        merged_df = pd.merge(advanced_stats_df, per_game_df_100, on='Team')
        merged_df = pd.merge(merged_df, opp_per_game_df_100, on='Team')
        merged_df = merged_df.rename(columns={'Team': 'TEAM'})
        merged_df['TEAM'] = merged_df['TEAM'].apply(lambda x: TEAM_TO_TEAM_ABBR[x.upper()] + "_" +str(season_end_year))

    return merged_df

def get_playoff_wins(season_end_year):
    r = get(
        f'https://www.basketball-reference.com/playoffs/NBA_{season_end_year}.html')
    df = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find_all('table')
        df = pd.read_html(str(table))[-1]
        df.columns = df.columns.droplevel(0)
        df = df[['Tm', 'W']]
        df.columns = ['TEAM', 'PLAYOFF_WINS']
        df = df.drop(16)
        df['TEAM'] = df['TEAM'].apply(lambda x: TEAM_TO_TEAM_ABBR[x.upper()] + "_" +str(season_end_year))
    return df
    

if __name__ == '__main__':
    print(get_playoff_wins(2022))
    print(get_team_stats(2022))