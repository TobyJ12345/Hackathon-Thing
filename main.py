import fastf1

from dashboard import createVis
from getData import pickQualiLaps, getSession

STATS_LIST = ["Speed", "RPM", "nGear", "Throttle"]

def selectRace():
    year = int(input("Enter the year: "))

    schedule = fastf1.get_event_schedule(2023, include_testing=False)
    for i, event in enumerate(schedule["EventName"]):
        print(f"{i+1}: {event}")

    print("")

    num = int(input("Select an event (The number): "))

    eventName = list(schedule["EventName"])[num-1]

    sessionNum = int(input("Select the session (1-3 for Q1-3): "))

    sessionData = getSession(year, eventName)

    laps = pickQualiLaps(sessionData, sessionNum)

    drivers = list(set(laps["Driver"]))

    print(f"The drivers in the session are {" ".join(drivers)}")
    print("Enter any number of drivers seperated by a space (Eg PIA NOR LEC)")

    driversSelected = input("").split(" ")

    print("Enter the same number of colours seperated by a space (Eg Orange Green Red)")

    colours = input("").split(" ")

    stats = []
    print("For each of the following stats specifiy y or n for wether you want the graph displayed")
    for stat in STATS_LIST:
        if input(f"{stat} : ") == "y":
            stats.append(stat)

    return year, eventName, sessionNum, driversSelected, colours, stats

if __name__ == "__main__":
    createVis(*selectRace())
