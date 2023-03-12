import pandas as pd
from requests import get
from bs4 import BeautifulSoup

try:
    from utils import get_player_suffix
    from lookup import lookup
except:
    from basketball_ref_scraper.utils import get_player_suffix
    from basketball_ref_scraper.lookup import lookup


def get_game_logs(_name, year, playoffs=False, ask_matches=True):
    name = lookup(_name, ask_matches)
    if name == "":
        print("No matches found")
        return ""
    # suffix = get_player_suffix(name).replace('/', '%2F').replace('.html', '')
    alpha_code = name.split(" ")[-1][0]
    if len(name.split(" ")[-1]) < 5:
        name_code = name.split(" ")[-1] + name[0:2]
    else:
        name_code = name.split(" ")[-1][0:5] + name[0:2]
    r = get(f'https://www.basketball-reference.com/players/{alpha_code}/{name_code}01/gamelog-advanced/{year}')
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        if table:
            df = pd.read_html(str(table))[0]
            df.rename(columns = {'Date': 'DATE', 'Age': 'AGE', 'Tm': 'TEAM', 'Unnamed: 5': 'HOME/AWAY', 'Opp': 'OPPONENT',
                'Unnamed: 7': 'RESULT', 'GmSc': 'GAME_SCORE'}, inplace=True)
            df['HOME/AWAY'] = df['HOME/AWAY'].apply(lambda x: 'AWAY' if x=='@' else 'HOME')
            df = df[df['Rk']!='Rk']
            df = df.drop(['Rk', 'G'], axis=1)
            df['DATE'] = pd.to_datetime(df['DATE'])
            df = df[df['GS'] == '1'].reset_index(drop=True)          
            return df