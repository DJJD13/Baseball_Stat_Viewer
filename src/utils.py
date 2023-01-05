def box_score_generator(result, team):
    total_wins = 0
    tot_runs_scored = 0
    tot_runs_allowed = 0

    for baseball_data in result:
        visiting_team = baseball_data[0]
        visiting_score = baseball_data[1]
        home_team = baseball_data[2]
        home_score = baseball_data[3]
        visiting_score_line = baseball_data[4]
        home_score_line = baseball_data[5]
        visiting_at_bats = baseball_data[6]
        visiting_hits = baseball_data[7]
        home_at_bats = baseball_data[8]
        home_hits = baseball_data[9]
        visiting_array = [*visiting_score_line]
        home_array = [*home_score_line]

        stat_returner = []

        print(visiting_team + " |", end=" ")
        for score in visiting_array:
            print(score, end=" ")
        print("| FINAL: " + str(visiting_score))

        print(home_team + " |", end=" ")
        for score in home_array:
            print(score, end=" ")
        print("| FINAL: " + str(home_score))
        print()
        print(visiting_team + " At Bats: " + str(visiting_at_bats))
        print(visiting_team + " Hits: " + str(visiting_hits))
        print()
        print(home_team + " At Bats: " + str(home_at_bats))
        print(home_team + " Hits: " + str(home_hits))
        print()
        print()

        if visiting_team == team:
            if visiting_score > home_score:
                total_wins += 1
            tot_runs_scored += visiting_score
            tot_runs_allowed += home_score
        else:
            if home_score > visiting_score:
                total_wins += 1
            tot_runs_scored += home_score
            tot_runs_allowed += visiting_score

    return total_wins, tot_runs_scored, tot_runs_allowed


def total_stat_printer(total_games, wins, runs_scored, runs_allowed):
    print("Record over " + str(total_games) + " games: " + str(wins) + " - " + str(total_games - wins))
    print()
    print("Total runs scored: " + str(runs_scored))
    print("Total runs allowed: " + str(runs_allowed))
    print()
    print("Average runs scored over " + str(total_games) + " games: " + str(
        round(runs_scored / total_games, 2)))
    print("Average runs scored against over " + str(total_games) + " games: " + str(
        round(runs_allowed / total_games, 2)))
    print("Done")
