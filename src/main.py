print(" Welcome to JD's BaseBall Stats Generator and Game Log Finder!")
print(" Please type the year you want to find below (in YYYY format):")

year = input(" Enter the year you want to find: ")

if year.isnumeric():
    year = int(year)
    print(year)
else:
    print(" Please enter a valid year (YYYY format)")


