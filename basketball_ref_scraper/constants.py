PLAYER_METRICS = ['DATE', 'AGE', 'TEAM', 'HOME/AWAY', 'OPPONENT', 'RESULT', 'GS', 'MP',
       'TS%', 'eFG%', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%',
       'USG%', 'ORtg', 'DRtg', 'GAME_SCORE', 'BPM']

CURR_NBA_TEAMS = [
        'Atlanta Hawks', 
        'Boston Celtics', 
        'Brooklyn Nets', 
        'Charlotte Hornets', 
        'Chicago Bulls', 
        'Cleveland Cavaliers', 
        'Dallas Mavericks', 
        'Denver Nuggets', 
        'Detroit Pistons', 
        'Golden State Warriors', 
        'Houston Rockets', 
        'Indiana Pacers', 
        'Los Angeles Clippers', 
        'Los Angeles Lakers', 
        'Memphis Grizzlies', 
        'Miami Heat', 
        'Milwaukee Bucks', 
        'Minnesota Timberwolves', 
        'New Orleans Pelicans', 
        'New York Knicks', 
        'Oklahoma City Thunder', 
        'Orlando Magic', 
        'Philadelphia 76ers', 
        'Phoenix Suns', 
        'Portland Trail Blazers', 
        'Sacramento Kings', 
        'San Antonio Spurs', 
        'Toronto Raptors', 
        'Utah Jazz', 
        'Washington Wizards'
]


TEAM_TO_TEAM_ABBR = {
        'ATLANTA HAWKS': 'ATL',
        'ST. LOUIS HAWKS': 'SLH',
        'MILWAUKEE HAWKS': 'MIL',
        'TRI-CITIES BLACKHAWKS': 'TCB',
        'BOSTON CELTICS': 'BOS',
        'BROOKLYN NETS': 'BRK',
        'NEW JERSEY NETS' : 'NJN',
        'NEW YORK NETS' : 'NYN',
        'CHICAGO BULLS': 'CHI',
        'CHARLOTTE HORNETS': 'CHO',
        'CHARLOTTE BOBCATS' : 'CHA',
        'CLEVELAND CAVALIERS': 'CLE',
        'DALLAS MAVERICKS': 'DAL',
        'DENVER NUGGETS': 'DEN',
        'DETROIT PISTONS': 'DET',
        'FORT WAYNE PISTONS': 'FWP',
        'GOLDEN STATE WARRIORS': 'GSW',
        'SAN FRANCISCO WARRIORS': 'SFW',
        'PHILADELPHIA WARRIORS': 'PHI',
        'HOUSTON ROCKETS': 'HOU',
        'SAN DIEGO ROCKETS': 'HOU',
        'INDIANA PACERS': 'IND',
        'LOS ANGELES CLIPPERS': 'LAC',
        'SAN DIEGO CLIPPERS': 'SDC',
        'BUFFALO BRAVES': 'BUF',
        'LOS ANGELES LAKERS': 'LAL',
        'MINNEAPOLIS LAKERS': 'MIN',
        'MEMPHIS GRIZZLIES': 'MEM',
        'VANCOUVER GRIZZLIES' : 'VAN',
        'MIAMI HEAT': 'MIA',
        'MILWAUKEE BUCKS': 'MIL',
        'MINNESOTA TIMBERWOLVES': 'MIN',
        'NEW ORLEANS PELICANS' : 'NOP',
        'NEW ORLEANS/OKLAHOMA CITY HORNETS' : 'NOK',
        'NEW ORLEANS HORNETS' : 'NOH',
        'NEW YORK KNICKS' : 'NYK',
        'OKLAHOMA CITY THUNDER' : 'OKC',
        'SEATTLE SUPERSONICS' : 'SEA',
        'ORLANDO MAGIC' : 'ORL',
        'PHILADELPHIA 76ERS' : 'PHI',
        'SYRACUSE NATIONALS' : 'SYR',
        'PHOENIX SUNS' : 'PHO',
        'PORTLAND TRAIL BLAZERS' : 'POR',
        'SACRAMENTO KINGS' : 'SAC',
        'KANSAS CITY KINGS' : 'KCK',
        'KANSAS CITY-OMAHA KINGS' : 'KCK',
        'CINCINNATI ROYALS' : 'CIN',
        'ROCHESTER ROYALS': 'ROR',
        'SAN ANTONIO SPURS' : 'SAS',
        'TORONTO RAPTORS' : 'TOR',
        'UTAH JAZZ' : 'UTA',
        'NEW ORLEANS JAZZ' : 'NOJ',
        'WASHINGTON WIZARDS' : 'WAS',
        'WASHINGTON BULLETS' : 'WAS',
        'CAPITAL BULLETS' : 'CAP',
        'BALTIMORE BULLETS' : 'BAL',
        'CHICAGO ZEPHYRS' : 'CHI',
        'CHICAGO PACKERS' : 'CHI',

        # DEFUNCT FRANCHISES
        'ANDERSON PACKERS': 'AND',
        'CHICAGO STAGS': 'CHI',
        'INDIANAPOLIS OLYMPIANS': 'IND',
        'SHEBOYGAN RED SKINS': 'SRS',
        'ST. LOUIS BOMBERS': 'SLB',
        'WASHINGTON CAPITOLS' : 'WAS',
        'WATERLOO HAWKS': 'WAT',
        }
TEAM_SETS = [['STL', 'TRI', 'MLH', 'ATL'],
 ['BOS'],
 ['NJN', 'BRK', 'NYN', 'NJA', 'NYA'],
 ['CHO', 'CHA', 'CHH'],
 ['CHI'],
 ['CLE'],
 ['DAL'],
 ['DEN', 'DNR', 'DNA'],
 ['DET', 'FTW'],
 ['GSW', 'SFW', 'PHW'],
 ['SDR', 'HOU'],
 ['INA', 'IND'],
 ['SDC', 'LAC', 'BUF'],
 ['LAL', 'MNL'],
 ['MEM', 'VAN'],
 ['MIA'],
 ['MIL'],
 ['MIN'],
 ['NOP', 'NOH', 'NOK'],
 ['NYK'],
 ['SEA', 'OKC'],
 ['ORL'],
 ['PHI', 'SYR'],
 ['PHO'],
 ['POR'],
 ['CIN', 'SAC', 'KCO', 'KCK', 'ROC'],
 ['DLC', 'SAA', 'SAS', 'TEX'],
 ['TOR'],
 ['NOJ', 'UTA'],
 ['WSB', 'CHP', 'CAP', 'BAL', 'WAS', 'CHZ']]

MONTH_ABBR_TO_NUM = {
        'JAN': 1,
        'FEB': 2,
        'MAR': 3,
        'APR': 4,
        'MAY': 5,
        'JUN': 6,
        'JUL': 7,
        'AUG': 8,
        'SEP': 9,
        'OCT': 10,
        'NOV': 11,
        'DEC': 12
}