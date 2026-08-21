import sys
import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from getData import SingleLap, getSession, pickQualiLaps, getFastest
from graphs import F1Graph
from dashboard import Car, RaceOverview



DT = 0.01
NANOFACTOR = 10 ** 9



class Utils():
    def __init__(self, race, graphs, timer):
        self.race = race
        self.graphs = graphs
        self.timer = timer
        self.time = 0

        self.maxTime = race.getMaxTime()
        self.paused = False
        self.speed = 4 * NANOFACTOR

    def createAll(self):
        self.race.drawTrack()
        for graph in self.graphs:
            graph.plotGraph()

        self.timer.timeout.connect(self.updateLoop)
        self.timer.start(int(DT * 1000))

    def updateLoop(self):
        if not self.paused:
            self.time += DT * self.speed
        self.race.updateTrack(self.time)
        for graph in self.graphs:
            graph.updateGraph((self.time) / float(self.maxTime.total_seconds() * NANOFACTOR))

if __name__ == "__main__":

    app = QApplication(sys.argv)


    qualiLaps = pickQualiLaps(getSession(2025, "China"), 3)
    fastestV = getFastest(qualiLaps, "PIA")
    fastestL = getFastest(qualiLaps, "NOR")

    car1 = Car("PIA", "orange", SingleLap(fastestV))
    car2 = Car("NOR", "green", SingleLap(fastestL))

    race = RaceOverview([car1, car2], app)

    speedGraph = F1Graph(app, "Speed", [car1, car2])

    RPMGraph = F1Graph(app, "RPM", [car1, car2])

    timer = QTimer()

    util = Utils(race, [RPMGraph, speedGraph], timer)

    util.createAll()

    sys.exit(app.exec())
