import sys
import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from getData import SingleLap, getSession, pickQualiLaps, getFastest
from dashboard import Car

class Graph():
    def __init__(self, app, dataType, cars : Car):
        self.app = app
        self.dataType = dataType
        self.cars = cars

    def plotGraph(self):
        self.plot = pg.PlotWidget()

        self.plot.setWindowTitle(f"Comparison of {self.dataType}")

        for car in self.cars:
            car.line = self.plot.plot(
            pen=pg.mkPen(car.colour, width=2),
            name= f"{car.name} {self.dataType}"
            )

        self.plot.show()

    def updateGraph(self, timeFloat : float):
        for car in self.cars:
            filteredData = car.getFilteredData(timeFloat)

            x = np.array(filteredData["RelativeDistance"])
            y = np.array(filteredData[self.dataType])

            car.line.setData(x,y)

        self.plot.show()



app = QApplication(sys.argv)

qualiLaps = pickQualiLaps(getSession(2025, "China"), 3)
fastestV = getFastest(qualiLaps, "PIA")
fastestL = getFastest(qualiLaps, "NOR")

car1 = Car("PIA", "orange", SingleLap(fastestV))
car2 = Car("NOR", "green", SingleLap(fastestL))

speedGraph = Graph(app, "Speed", [car1, car2])

speedGraph.plotGraph()
speedGraph.updateGraph(1)

RPMGraph = Graph(app, "RPM", [car1, car2])

RPMGraph.plotGraph()
RPMGraph.updateGraph(1)

sys.exit(app.exec())

