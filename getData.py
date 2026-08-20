import fastf1
import numpy as np


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

def lerp(x1, x2, t):
    return t*x1 + (1-t)*x2

class SingleLap:
    def __init__(self, lap):
        self.lap = lap

        self.telem = lap.get_telemetry()

    def createTrackData(self, interp=10):
        x = np.array(self.telem["X"])
        y = np.array(self.telem["Y"])

        #Interpolating between points to create more complete track data

        new_indices = np.linspace(0, len(x) - 1, interp * len(x))
        interpX = np.interp(new_indices, np.linspace(0, len(x) - 1, len(x)), x)
        interpY = np.interp(new_indices, np.linspace(0, len(x) - 1, len(x)), y)
        
        return interpX, interpY

    def getTimeData(self, time):
        times = np.array(self.telem["Time"])
        times = times.astype("int64") 
        xs = np.array(self.telem["X"])
        ys = np.array(self.telem["Y"])

        x = np.interp(time, times, xs)
        y = np.interp(time, times, ys)

        return float(x), float(y)

    def getDriverData(self):
        speed = self.telem["Speed"]
        rpm = self.telem["RPM"]
        throttle = self.telem["Throttle"]
        brake = self.telem["Break"]
        drs = self.telem["DRS"]

        return speed, rpm, throttle, brake, drs
   

qualiLaps = pickQualiLaps(getSession(2024, "Monaco"), 3)
fastest = getFastest(qualiLaps, "VER")

fastLap = SingleLap(fastest)

print(fastLap.createTrackData())
