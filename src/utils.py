import math


def box_score_generator(result, team):
    total_wins = 0
    tot_runs_scored = 0
    tot_runs_allowed = 0
    tot_at_bats = 0
    tot_hits = 0

    for baseball_data in result:
        visiting_team = baseball_data[0]
        visiting_score = baseball_data[1]
        home_team = baseball_data[2]
        home_score = baseball_data[3]
        visiting_score_line = baseball_data[4]
        home_score_line = baseball_data[5]
        visiting_at_bats = baseball_data[6]
        visiting_hits = baseball_data[7]
        home_at_bats = baseball_data[12]
        home_hits = baseball_data[13]
        visiting_array = [*visiting_score_line]
        home_array = [*home_score_line]

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
            tot_at_bats += visiting_at_bats
            tot_hits += visiting_hits
        else:
            if home_score > visiting_score:
                total_wins += 1
            tot_runs_scored += home_score
            tot_runs_allowed += visiting_score
            tot_at_bats += home_at_bats
            tot_hits += home_hits

    return total_wins, tot_runs_scored, tot_runs_allowed, tot_at_bats, tot_hits


def total_stat_printer(total_games, wins, runs_scored, runs_allowed, at_bats, hits):
    print("Record over " + str(total_games) + " games: " + str(wins) + " - " + str(total_games - wins))
    print()
    print("Total runs scored: " + str(runs_scored))
    print("Total runs allowed: " + str(runs_allowed))
    print()
    print("Average runs scored over " + str(total_games) + " games: " + str(
        round(runs_scored / total_games, 2)))
    print("Average runs scored against over " + str(total_games) + " games: " + str(
        round(runs_allowed / total_games, 2)))
    print()
    print("Batting average over " + str(total_games) + " : " + str(round(hits / at_bats, 3)))


def batter_stat_generator(result, player):
    walks = 0
    strikeouts = 0
    hits = 0
    hbp = 0
    errors = 0
    sf_flies = 0
    singles = 0
    doubles = 0
    triples = 0
    homeruns = 0

    # Total amount of times the player was at the plate. It is NOT the same as at bats
    plate_appearances = 0

    # Total at bats. These are plate appearances that do NOT end in:
    # Walk, HBP, Sac Fly/Bunt(Hit), Interference, or replaced
    at_bats = 0

    for play in result:
        # game_id = play[0]
        # pitching_seq = play[1]
        # batter = play[2]
        # event_text = play[3]
        event_type = play[4]
        # rbi_on_play = play[5]
        ab_flag = play[6]
        sf_flag = play[7]

        plate_appearances += 1

        # Generic Out
        if event_type == 2:
            if ab_flag == 'T':
                at_bats += 1
            if sf_flag == 'T':
                sf_flies += 1
        # Strikeout
        elif event_type == 3:
            at_bats += 1
            strikeouts += 1
        # Walk
        elif event_type == 14 or event_type == 15:
            walks += 1
        # HBP
        elif event_type == 16:
            hbp += 1
        # Error
        elif event_type == 18:
            at_bats += 1
            errors += 1
        # Fielder's Choice
        elif event_type == 19:
            at_bats += 1
        # Single
        elif event_type == 20:
            at_bats += 1
            hits += 1
            singles += 1
        # Double
        elif event_type == 21:
            at_bats += 1
            hits += 1
            doubles += 1
        # Triple
        elif event_type == 22:
            at_bats += 1
            hits += 1
            triples += 1
        # Home Run
        elif event_type == 23:
            at_bats += 1
            hits += 1
            homeruns += 1
        else:
            plate_appearances += 0

    # Total number of bases the player achieved in hits (1 for S, 2 for D, 3 for T, 4 for HR)
    total_bases = singles + (2 * doubles) + (3 * triples) + (4 * homeruns)

    # Shows how often a player's At bats ended in a hit (Hits / At Bats)
    batting_avg = round(hits / at_bats, 3)

    # Shows how often a player's PA ended in a walk (Walks / Plate Appearances)
    bb_avg = round(walks / plate_appearances, 3)

    # Shows how often a player ended up on base, no matter how it was done
    # (Hits + Walks + HBP / At Bats + Walks + HBP + Sac Fly)
    on_base_per = round((hits + walks + hbp) / (at_bats + walks + hbp + sf_flies), 3)

    # Shows batting average with weight for the number of bases the player gets in a hit
    # (Singles + 2*Doubles + 3*Triples + 4*HRs) / At Bats
    slugging_per = round(total_bases / at_bats, 3)

    # Percentage of times a player struck out (Strikeouts / At bats)
    strikeout_ratio = round(strikeouts / at_bats, 3)

    # On base + slugging. Good overall way to see a hitter's general performance
    on_base_plus_slugging = round(on_base_per + slugging_per, 3)

    batter_stat_printer(
        player,
        plate_appearances,
        at_bats,
        total_bases,
        batting_avg,
        bb_avg,
        on_base_per,
        slugging_per,
        strikeout_ratio,
        on_base_plus_slugging
    )


def batter_stat_printer(player, pa, ab, tb, ba, bb_avg, obp, slg, str_r, ops):
    player = player[0]
    last_name = player[0]
    first_name = player[1]
    print(f'2002 Stats for { first_name } { last_name }: ')
    print()
    print("Plate Appearances: " + str(pa))
    print("At Bats: " + str(ab))
    print("Total bases: " + str(tb))
    print("Batting Average: " + str(ba))
    print("Base on Balls Average: " + str(bb_avg))
    print("On Base Percentage: " + str(obp))
    print("Slugging Percentage: " + str(slg))
    print("Strikeout ratio: " + str(str_r))
    print("On Base Plus Slugging: " + str(ops))
    print()
    print()


def round_decimals_down(number: float, decimals: int = 2):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor
