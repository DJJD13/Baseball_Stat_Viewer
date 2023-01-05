import mysql.connector
import re
import utils

baseball_stats_db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="OrangeBlue4",
    database="baseball_stats",
)

baseball_cursor = baseball_stats_db.cursor()
date_check = re.compile(r"^\d{4}-\d{2}-\d{2} - \d{4}-\d{2}-\d{2}")

team_dict = {
    'ANA': {'city': 'Anaheim', 'name': 'Angels'},
    'ARI': {'city': 'Arizona', 'name': 'Diamondbacks'},
    'ATL': {'city': 'Atlanta', 'name': 'Braves'},
    'BAL': {'city': 'Baltimore', 'name': 'Orioles'},
    'BOS': {'city': 'Boston', 'name': 'Red Sox'},
    'CHA': {'city': 'Chicago', 'name': 'White Sox'},
    'CHN': {'city': 'Chicago', 'name': 'Cubs'},
    'CIN': {'city': 'Cincinnati', 'name': 'Reds'},
    'CLE': {'city': 'Cleveland', 'name': 'Guardians'},
    'COL': {'city': 'Colorado', 'name': 'Rockies'},
    'DET': {'city': 'Detroit', 'name': 'Tigers'},
    'HOU': {'city': 'Houston', 'name': 'Astros'},
    'KCA': {'city': 'Kansas City', 'name': 'Royals'},
    'LAN': {'city': 'Los Angeles', 'name': 'Dodgers'},
    'MIA': {'city': 'Miami', 'name': 'Marlins'},
    'MIN': {'city': 'Minnesota', 'name': 'Twins'},
    'MIL': {'city': 'Milwaukee', 'name': 'Brewers'},
    'NYA': {'city': 'New York', 'name': 'Yankees'},
    'NYN': {'city': 'New York', 'name': 'Mets'},
    'PHI': {'city': 'Philadelphia', 'name': 'Phillies'},
    'PIT': {'city': 'Pittsburgh', 'name': 'Pirates'},
    'OAK': {'city': 'Oakland', 'name': 'Athletics'},
    'SDN': {'city': 'San Diego', 'name': 'Padres'},
    'SEA': {'city': 'Seattle', 'name': 'Mariners'},
    'SFN': {'city': 'San Fransisco', 'name': 'Giants'},
    'SLN': {'city': 'St. Louis', 'name': 'Cardinals'},
    'TBA': {'city': 'Tampa Bay', 'name': 'Rays'},
    'TEX': {'city': 'Texas', 'name': 'Rangers'},
    'TOR': {'city': 'Toronto', 'name': 'Blue Jays'},
    'WAS': {'city': 'Washington', 'name': 'Nationals'}
}

print(" Welcome to JD's BaseBall Stats Generator and Game Log Finder!")
print(" Type --help for more information about formatting and options.")

while True:
    year = input(" Enter the year you want to find, or a specific game date/range of dates: ")
    if not year.isnumeric():
        if date_check.match(year):
            year_begin = year[0: year.index(" ")]
            year_end = year[year.index(" ") + 3:]
        elif year == "--help":
            print(" Enter a single year in the format YYYY (ex: 2013)")
            print(" Enter a range of dates in the format 'YYYY-MM-DD - YYYY-MM-DD' (ex: 2013-03-31 - 2013-06-31)")
            print(" Enter an abbreviation for the team you wish to find. Type '--teams' to see a list of acceptable"
                  " abbreviations")
            continue
        elif year == "--teams":
            for team in team_dict:
                print(" " + team + ": " + team_dict[team]['city'] + " " + team_dict[team]['name'])
            continue
        else:
            print("Please enter a valid year or range of years.")
            continue
    else:
        year_begin = year + "-01-01"
        year_end = year + "-12-31"

    team = input(" Enter the home team name: ")
    team_city = team_dict[team]['city']
    team_name = team_dict[team]['name']

    amount_of_games = int(input(" Enter the amount of games you want to find: "))
    print()

    queryGame = f'SELECT visitingTeam, visitingScore, homeTeam, homeScore, visitingLineScore, homeLineScore, vAtBats, ' \
                f'vHits, vDoubles, vTriples, vHomeRuns, vRBI,  hAtBats, hHits, hDoubles, hTriples, hHomeRuns, hRBI ' \
                f'FROM game_logs ' \
                f'WHERE (homeTeam = \'{team}\' OR visitingTeam = \'{team}\') AND ' \
                f'(gameDate >= \'{year_begin}\' AND gameDate <= \'{year_end}\') ORDER BY gameDate ' \
                f'LIMIT {amount_of_games}'

    baseball_cursor.execute(queryGame)

    result = baseball_cursor.fetchall()

    team_wins, total_runs_scored, total_runs_allowed = utils.box_score_generator(result, team)

    utils.total_stat_printer(amount_of_games, team_wins, total_runs_scored, total_runs_allowed)

    break
