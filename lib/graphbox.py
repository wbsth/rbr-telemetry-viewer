import sys

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox

from lib.SimpleGraph import SimpleGraph
from lib.AdvGraphs import *

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as navigationToolbar


class GraphBox(QWidget):
    """Class represents single graph"""
    def __init__(self, data):
        super().__init__()
        self._data = data

        # building list of possible graphs choices
        self.proper_graphs = ['MapView', 'SuspHistogram.LF', 'SuspHistogram.RF', 'SuspHistogram.LB', 'SuspHistogram.RB', 'TireTemps']
        self.direct_values = list(self._data.columns)[2:-1]
        self.possible_graphs = ['-']
        self.possible_graphs.extend(self.proper_graphs)
        self.possible_graphs.extend('-')
        self.possible_graphs.extend(self.direct_values)

        # setting layout
        self.lay = QVBoxLayout()
        self.setLayout(self.lay)
        self.lay.setAlignment(Qt.AlignTop)
        self._createComboBox()
        self._createPlaceholder()

    def _createComboBox(self):
        """Create combo box and adds to layout"""
        self.comboBox = QComboBox(self)
        for option in self.possible_graphs:
            self.comboBox.addItem(option)
        self.comboBox.activated[str].connect(self._createGraph)
        self.lay.addWidget(self.comboBox)

    def _createGraph(self, option):
        """Create graph"""
        self._option = option
        # delete previous widget
        for widget in self.widgets:
            widget.deleteLater()

        if self._option != "-":
            if self._option in self.direct_values:
                # direct value graph
                self.graph = SimpleGraph(self._data, self._option)
            elif self._option in self.proper_graphs:
                # advanced graphs, ex map view
                # check if its
                self._split_option = self._option.split(".")
                if len(self._option) == 1:
                    self.graph = eval(f"{self._split_option}(self._data, self._split_option)")
                else:
                    self.graph = eval(f"{self._split_option[0]}(self._data, self._split_option)")
            else:
                sys.exit()

            toolbar = navigationToolbar(self.graph, self)
            self.lay.addWidget(self.graph)
            self.lay.addWidget(toolbar)
            self.widgets = [self.graph, toolbar]

        else:
            self._createPlaceholder()

    def _createPlaceholder(self):
        """Create placeholder if def value is selected in combo box"""
        placeholder = QWidget(self)
        self.lay.addWidget(placeholder)
        self.widgets = [placeholder]
