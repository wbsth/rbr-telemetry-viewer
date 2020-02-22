from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QSlider
from lib.graphbox import GraphBox


class TelemetryWidget(QWidget):
    def __init__(self, parent, layout, grid_type, data):
        super().__init__()
        self._layout = layout
        self._grid_type = grid_type
        self._data = data
        self.grid_elements = []
        self.grid_layout = QGridLayout()
        self.createGraphGrid()
        self._createSlider()

    def createGraphGrid(self):
        """Creates telemetry grid at provided layout"""
        # creating grid layout
        grid = QWidget()
        grid.setLayout(self.grid_layout)
        self._layout.addWidget(grid)
        # filling grid layout with GraphBoxes
        for i in range(self._grid_type[0]):
            for j in range(self._grid_type[1]):
                box = GraphBox(self._data)
                self.grid_elements.append(box)
                self.grid_layout.addWidget(self.grid_elements[-1], i, j)
                self.grid_layout.setColumnStretch(i, 5)
                self.grid_layout.setRowStretch(j, 5)

    def _createSlider(self):
        """Creates slider to provided layout"""
        self.slider = QSlider(Qt.Horizontal, self)
        steps_list = [list(self._data.index.values)[i] for i in (0, -1)]
        self.slider.setMinimum(steps_list[0])
        self.slider.setMaximum(steps_list[-1])
        self.grid_layout.addWidget(self.slider, self._grid_type[0], 0, 1, self._grid_type[1])