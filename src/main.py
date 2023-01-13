import mysql.connector
# import pymysql
# import os
# import boto3
import re
import utils


# ENDPOINT = "baseballstats-mysql-aws.co5amxrfxw6w.us-east-1.rds.amazonaws.com"
# PORT = 3306
# USER = "mike_ohtani"
# REGION = "us-east-1"
# DBNAME = "baseball_stats"
# os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'


def main():
    # gets the credentials from .aws/credentials
    # session = boto3.Session(profile_name='default')
    # client = session.client('rds')
    #
    # token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)
    #
    # try:
    #     conn = pymysql.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME,
    #                            ssl_ca='us-east-1-bundle.pem')
    #     baseball_cursor = conn.cursor()
    #     print("Connection Successfully established")
    # except Exception as e:
    #     print("Database Connection failed due to {}".format(e))

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

    event_type_dict = {
        0: "Unkown Event",
        1: "No event",
        2: "Generic Out",
        3: "Strikeout",
        4: "Stolen Base",
        5: "Defensive Indifference",
        6: "Caught Stealing",
        7: "Pickoff error",
        8: "Pickoff",
        9: "Wild Pitch",
        10: "Passed ball",
        11: "Balk",
        12: "Other advance",
        13: "Foul Error",
        14: "Walk",
        15: "Intentional Walk",
        16: "Hit by pitch",
        17: "Interference",
        18: "Error",
        19: "Fielder's Choice",
        20: "Single",
        21: "Double",
        22: "Triple",
        23: "Home Run",
        24: "Missing Play"
    }

    print(" Welcome to JD's BaseBall Stats Generator and Game Log Finder!")
    print(" Type --help for more information about formatting and options.")

    while True:
        stat_choice = input("Select which mode you want: Game Log or 2002 Season > ")
        print()

        if stat_choice == "Game Log":
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

            team = input(" Enter the team abbreviation: ")
            team_city = team_dict[team]['city']
            team_name = team_dict[team]['name']

            print(" " + team_city + " " + team_name)

            amount_of_games = int(input(" Enter the amount of games you want to find: "))
            print()

            query_game = f'SELECT visitingTeam, visitingScore, homeTeam, homeScore, visitingLineScore, homeLineScore, ' \
                         f'vAtBats, vHits, vDoubles, vTriples, vHomeRuns, vRBI, ' \
                         f'hAtBats, hHits, hDoubles, hTriples, hHomeRuns, hRBI ' \
                         f'FROM game_logs ' \
                         f'WHERE (homeTeam = \'{team}\' OR visitingTeam = \'{team}\') AND ' \
                         f'(gameDate >= \'{year_begin}\' AND gameDate <= \'{year_end}\') ORDER BY gameDate ' \
                         f'LIMIT {amount_of_games}'

            query_season = f'SELECT visitingTeam, visitingScore, homeTeam, homeScore, visitingLineScore, homeLineScore, ' \
                           f'vAtBats, vHits, vDoubles, vTriples, vHomeRuns, vRBI, ' \
                           f'hAtBats, hHits, hDoubles, hTriples, hHomeRuns, hRBI ' \
                           f'FROM game_logs ' \
                           f'WHERE (homeTeam = \'{team}\' OR visitingTeam = \'{team}\') AND ' \
                           f'(gameDate >= \'{year_begin}\' AND gameDate <= \'{year_end}\') ORDER BY gameDate '

            baseball_cursor.execute(query_game)

            result = baseball_cursor.fetchall()

            team_wins, \
                total_runs_scored, \
                total_runs_allowed, \
                total_at_bats, \
                total_hits = utils.box_score_generator(result, team)

            utils.total_stat_printer(
                amount_of_games,
                team_wins,
                total_runs_scored,
                total_runs_allowed,
                total_at_bats,
                total_hits
            )

        elif stat_choice == "2002 Season":
            player_code = input("Enter the player you wish to find: ")
            print()

            query_2002_season_batters = f'SELECT game_id, pitching_sequence, res_batter, event_text, event_type, ' \
                                        f'rbi_on_play, ab_flag, sf_flag ' \
                                        f'FROM regular_season_2002 ' \
                                        f'WHERE res_batter = \'{ player_code }\' ' \

            query_player_name = f'SELECT last_name, first_name, team, field_position ' \
                                f'FROM roster_2002 ' \
                                f'WHERE player_id = \'{ player_code }\' '

            baseball_cursor.execute(query_2002_season_batters)
            result = baseball_cursor.fetchall()

            baseball_cursor.execute(query_player_name)
            player_name = baseball_cursor.fetchall()

            utils.batter_stat_generator(result, player_name)

        else:
            print("Please type a valid mode to set")
            continue

        break


if __name__ == '__main__':
    main()
