import sys
import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from getData import SingleLap, getSession, pickQualiLaps, getFastest

DT = 0.05
NANOFACTOR = 10 ** 9


class Car():
    def __init__(self, name, colour, lap : SingleLap):
        self.name = name
        self.colour = colour
        self.lap = lap
        self.pos = self.getPos(0)

    def getPos(self, time):
        return self.lap.getTimeData(time)

    def drawSelf(self, plot):
        self.plotItem = pg.ScatterPlotItem(
            x=[self.pos[0]],
            y=[self.pos[1]],
            size=8,
            brush=[pg.mkBrush(self.colour)],
            pen=pg.mkPen("white", width=1)
        )

        plot.addItem(self.plotItem)


class RaceOverview():
    def __init__(self, cars, app):
        self.cars = cars
        self.app = app
        self.plot = pg.PlotWidget()
        self.plot.setWindowTitle("Track Overview")

        #State Variables
        self.time = 0
        self.maxTime = self.getMaxTime()
        self.paused = False
        self.speed = 1 * NANOFACTOR

    def getMaxTime(self):
        return max(self.cars, key= lambda x: max(x.lap.telem["Time"]))

    def drawTrack(self):
        lap = self.cars[0].lap 

        track_x, track_y = lap.createTrackData()

        self.plot.plot(
            track_x,
            track_y,
            pen=pg.mkPen("#dddddd", width=4)
        )

        self.plot.show()


    def updateTrack(self):
        if self.paused:
            return

        self.time += DT * self.speed

        self.updateCars()

        self.drawCars()

        self.plot.show

        
    def drawCars(self):
        for car in self.cars:
            car.pos = car.drawSelf(self.plot)

    def updateCars(self):
        for car in self.cars:
            car.pos = car.getPos(self.time)




app = QApplication(sys.argv)


qualiLaps = pickQualiLaps(getSession(2024, "Monaco"), 3)
fastestV = getFastest(qualiLaps, "VER")
fastestL = getFastest(qualiLaps, "LEC")

car1 = Car("VER", "blue", SingleLap(fastestV))
car2 = Car("LEC", "red", SingleLap(fastestL))

race = RaceOverview([car1, car2], app)
race.getMaxTime()
race.drawTrack()

timer = QTimer()
timer.timeout.connect(race.updateTrack)
timer.start(int(DT * 1000)) #DT is seconds

sys.exit(app.exec())
