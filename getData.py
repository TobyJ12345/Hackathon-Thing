import fastf1

#Setup cache
fastf1.Cache.enable_cache('./cacheFolder')

def getSession(year, race):
    session = fastf1.get_session(year, race, "Q")
    session.load()

    return session

def pickQualiLaps(session, qualifyingSession=3):
    laps = session.laps

    return laps.split_qualifying_sessions()[qualifyingSession-1]

def getFastest(laps, driver):
    driverLaps = laps.pick_drivers(driver)
    fastest = driverLaps.pick_fastest()

    return fastest

class SingleLap:
    def __init__(self, lap):
        self.lap = lap

        self.telem = lap.get_telemetry()

    def createTrackData(self):
        x = self.telem["X"]
        y = self.telem["Y"]

        return x, y

    def getDriverData(self):
        speed = self.telem["Speed"]
        rpm = self.telem["RPM"]
        throttle = self.telem["Throttle"]
        brake = self.telem["Break"]
        drs = self.telem["DRS"]

        return speed, rpm, throttle, brake, drs
   

qualiLaps = pickQualiLaps(getSession(2024, "Monaco"), 3)
fastest = getFastest(qualiLaps, "VER")
telem = fastest.get_telemetry()
print(telem.columns.tolist())