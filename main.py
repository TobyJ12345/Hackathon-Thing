import sys
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel
from PyQt6.QtCore import Qt, QTimer, QElapsedTimer

from getData import SingleLap, getSession, pickQualiLaps, getFastest
from graphs import F1Graph
from dashboard import Car, RaceOverview


class Controls(QWidget):
    def __init__(self, utils):
        super().__init__()
        self.utils = utils

        self.playButton = QPushButton("▶")
        self.slowButton = QPushButton("0.5×")
        self.normalButton = QPushButton("1×")
        self.fastButton = QPushButton("2×")
        self.fasterButton = QPushButton("4×")

        self.currentLabel = QLabel("00:00.000")
        self.durationLabel = QLabel(self.formatTime(utils.duration))

        self.timeline = QSlider(Qt.Orientation.Horizontal)
        self.timeline.setMinimum(0)
        self.timeline.setMaximum(int(utils.duration * 1000))
        self.timeline.setValue(0)

        layout = QVBoxLayout()
        controls = QHBoxLayout()

        controls.addWidget(self.playButton)
        controls.addWidget(self.slowButton)
        controls.addWidget(self.normalButton)
        controls.addWidget(self.fastButton)
        controls.addWidget(self.fasterButton)

        timelineLayout = QHBoxLayout()
        timelineLayout.addWidget(self.currentLabel)
        timelineLayout.addWidget(self.timeline)
        timelineLayout.addWidget(self.durationLabel)

        layout.addLayout(controls)
        layout.addLayout(timelineLayout)
        self.setLayout(layout)

        self.playButton.clicked.connect(self.togglePlayback)
        self.slowButton.clicked.connect(lambda: self.utils.setSpeed(0.5))
        self.normalButton.clicked.connect(lambda: self.utils.setSpeed(1.0))
        self.fastButton.clicked.connect(lambda: self.utils.setSpeed(2.0))
        self.fasterButton.clicked.connect(lambda: self.utils.setSpeed(4.0))
        self.timeline.valueChanged.connect(self.seek)

        self.utils.addCallback(self.updateTimeline)

    def togglePlayback(self):
        self.utils.toggle()

        if self.utils.paused:
            self.playButton.setText("▶")
        else:
            self.playButton.setText("⏸")

    def seek(self, value):
        self.utils.seek(value / 1000.0)

    def updateTimeline(self, time):
        self.timeline.blockSignals(True)
        self.timeline.setValue(int(time * 1000))
        self.timeline.blockSignals(False)
        self.currentLabel.setText(self.formatTime(time))

    def formatTime(self, seconds):
        minutes = int(seconds // 60)
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:06.3f}"


class Utils:
    def __init__(self, race, graphs, duration):
        self.race = race
        self.graphs = graphs
        self.time = 0.0
        self.duration = duration
        self.paused = True
        self.speed = 1.0

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateLoop)

        self.clock = QElapsedTimer()
        self.callbacks = []

    def createAll(self):
        self.race.drawTrack()

        for graph in self.graphs:
            graph.plotGraph()

        self.timer.start(16)
        self.updateObjects()

    def updateLoop(self):
        if not self.paused:
            dt = self.clock.restart() / 1000.0
            self.time += dt * self.speed

            if self.time >= self.duration:
                self.time = self.duration
                self.pause()

        self.updateObjects()

    def updateObjects(self):
        self.race.updateTrack(self.time)

        normalizedTime = self.time / self.duration if self.duration > 0 else 0

        for graph in self.graphs:
            graph.updateGraph(normalizedTime)

        for callback in self.callbacks:
            callback(self.time)

    def play(self):
        if self.time >= self.duration:
            self.time = 0.0

        self.paused = False
        self.clock.start()

    def pause(self):
        self.paused = True

    def toggle(self):
        if self.paused:
            self.play()
        else:
            self.pause()

    def setSpeed(self, speed):
        self.speed = speed

    def seek(self, time):
        self.time = max(0.0, min(time, self.duration))
        self.updateObjects()

    def addCallback(self, callback):
        self.callbacks.append(callback)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    qualiLaps = pickQualiLaps(getSession(2025, "China"), 3)
    fastestV = getFastest(qualiLaps, "PIA")
    fastestL = getFastest(qualiLaps, "NOR")

    car1 = Car("PIA", "orange", SingleLap(fastestV))
    car2 = Car("NOR", "green", SingleLap(fastestL))

    cars = [car1, car2]

    race = RaceOverview(cars, app)

    speedGraph = F1Graph(app, "Speed", cars)
    rpmGraph = F1Graph(app, "RPM", cars)

    graphs = [speedGraph, rpmGraph]

    duration = race.getMaxTime().total_seconds()

    utils = Utils(race, graphs, duration)

    controls = Controls(utils)
    controls.setWindowTitle("F1 Replay Controls")
    controls.resize(700, 120)
    controls.show()

    utils.createAll()

    sys.exit(app.exec())