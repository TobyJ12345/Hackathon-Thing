import sys
import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from getData import SingleLap, getSession, pickQualiLaps, getFastest

NANOFACTOR = 10 ** 9

def formatTime(time):
    totalSeconds = time.total_seconds()
    minutes = int(totalSeconds // 60)
    seconds = totalSeconds % 60

    return f"{minutes}:{seconds:06.3f}"

class Car():
    def __init__(self, name, colour, lap : SingleLap):
        self.name = name
        self.colour = colour
        self.lap = lap
        self.pos = self.getPos(0)
        self.plotItem = None
        self.laptime = lap.lap["LapTime"]

    def getPos(self, time):
        return self.lap.getTimeData(time)

    def drawSelf(self, plot):
        if self.plotItem == None:
            self.plotItem = pg.ScatterPlotItem(
                x=[self.pos[0]],
                y=[self.pos[1]],
                size=8,
                brush=[pg.mkBrush(self.colour)],
                pen=pg.mkPen("white", width=1)
            )
        self.plotItem.setData(
            x=[self.pos[0]],
            y=[self.pos[1]],
            size=8,
            brush=[pg.mkBrush(self.colour)],
            pen=pg.mkPen("white", width=1))


    def getFilteredData(self, relDistMax):
            mask = (self.lap.telem["RelativeDistance"] <= relDistMax)
            filteredData = self.lap.telem.slice_by_mask(mask)
    
            return filteredData

class RaceOverview():
    def __init__(self, cars, app):
        self.cars = cars
        self.app = app
        self.plot = pg.PlotWidget()
        self.plot.setWindowTitle("Track Overview")
        self.time = 0

        self.timeTexts = {}

        for car in self.cars:
            self.timeTexts[car.name] = pg.TextItem(
                f"{car.name}: {formatTime(car.laptime)}",
                color=car.colour
            )
            self.plot.addItem(self.timeTexts[car.name])
        

    def getMaxTime(self):
        return max(max(self.cars, key= lambda x: max(x.lap.telem["Time"])).lap.telem["Time"])

    def drawTrack(self):
        lap = self.cars[0].lap 

        track_x, track_y = lap.createTrackData()

        self.plot.plot(
            track_x,
            track_y,
            pen=pg.mkPen("#dddddd", width=4)
        )

        x = min(track_x)
        y = max(track_y)

        for i, car in enumerate(self.cars):
            self.timeTexts[car.name].setPos(
                x,
                y - i * 350
            )

        self.plot.show()


    def updateTrack(self, time):
        self.time = time * NANOFACTOR

        self.updateCars()

        self.drawCars()


    def drawCars(self):
        for car in self.cars:
            car.drawSelf(self.plot)

    def updateCars(self):
        for car in self.cars:
            car.pos = car.getPos(self.time)