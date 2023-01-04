import mysql.connector

baseballStatsDb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="OrangeBlue4",
    database="baseball_stats",
)

baseballCursor = baseballStatsDb.cursor()

print(" Welcome to JD's BaseBall Stats Generator and Game Log Finder!")
print(" Please type the year you want to find below (in YYYY format):")

while True:
    year = input(" Enter the year you want to find: ")
    if not year.isnumeric():
        print("Please enter a valid year.")
        continue
    yearBegin = year + "-01-01"
    yearEnd = year + "-12-31"

    team = input(" Enter the home team name: ")

    amountOfGames = int(input(" Enter the amount of games you want to find: "))
    print()

    query = f'SELECT visitingTeam, visitingScore, homeTeam, homeScore, visitingLineScore, homeLineScore ' \
            f'FROM game_logs ' \
            f'WHERE (homeTeam = \'{team}\' OR visitingTeam = \'{team}\') AND ' \
            f'(gameDate >= \'{yearBegin}\' AND gameDate <= \'{yearEnd}\') ORDER BY gameDate LIMIT {amountOfGames}'

    baseballCursor.execute(query)

    result = baseballCursor.fetchall()

    teamWins = 0
    totalRunsScored = 0
    totalRunsAllowed = 0

    for x in result:
        visitingTeam = x[0]
        visitingScore = x[1]
        homeTeam = x[2]
        homeScore = x[3]
        visitingScoreLine = x[4]
        homeScoreLine = x[5]
        visitingArray = [*visitingScoreLine]
        homeArray = [*homeScoreLine]

        print(visitingTeam + " |", end=" ")
        for score in visitingArray:
            print(score, end=" ")
        print("| FINAL: " + str(visitingScore))

        print(homeTeam + " |", end=" ")
        for score in homeArray:
            print(score, end=" ")
        print("| FINAL: " + str(homeScore))
        print()

        if visitingTeam == team:
            if visitingScore > homeScore:
                teamWins += 1
            totalRunsScored += visitingScore
            totalRunsAllowed += homeScore
        else:
            if homeScore > visitingScore:
                teamWins += 1
            totalRunsScored += homeScore
            totalRunsAllowed += visitingScore

    print("Record over " + str(amountOfGames) + " games: " + str(teamWins) + " - " + str(amountOfGames - teamWins))
    print()
    print("Total runs scored: " + str(totalRunsScored))
    print("Total runs allowed: " + str(totalRunsAllowed))
    print()
    print("Average score over " + str(amountOfGames) + " games: " + str(round(totalRunsScored / amountOfGames, 2)))
    print("Average score against over " + str(amountOfGames) + " games: " + str(round(totalRunsAllowed / amountOfGames, 2)))
    break

#
# if year.isnumeric():
#     year = int(year)
#     print(year)
# else:
#     print(" Please enter a valid year (YYYY format)")
