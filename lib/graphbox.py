from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox
from lib.mplcanvas import MplCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as navigationToolbar


class GraphBox(QWidget):
    """Class represents single graph"""
    def __init__(self, data):
        super().__init__()
        self._data = data

        # building list of possible graphs choices
        self.possible_graphs = ['-']
        test = list(self._data.columns)[2:-1]
        self.possible_graphs.extend(test)

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
            self.graph = MplCanvas(self, width=10, height=10, dpi=75)
            self.graph.axes.plot(self._data[self._option], color='k', linewidth=1)
            self.graph.axes.axvline(list(self._data.index.values)[0], color='r', label='-')
            self.graph.axes.legend(loc='upper right')
            self.graph.fig.set_tight_layout(True)
            toolbar = navigationToolbar(self.graph, self)
            self.lay.addWidget(self.graph)
            self.lay.addWidget(toolbar)
            self.widgets = [self.graph, toolbar]
        else:
            self._createPlaceholder()

    def update_graph(self, slider_value):
        """Updates graph based on slider position"""
        if type(self.widgets[0]) == MplCanvas:
            # remove old vertical line
            self.graph.axes.lines.remove(self.graph.axes.lines[-1])
            # add new vertical line
            value = self._data[self._option][slider_value]
            if isinstance(value, float):
                str_value = "{:.2f}".format(value)
            else:
                str_value = str(value)
            self.graph.axes.axvline(slider_value, color='r', label=str_value)
            self.graph.axes.legend(loc='upper right')
            self.graph.draw()

    def _createPlaceholder(self):
        """Create placeholder if def value is selected in combo box"""
        placeholder = QWidget(self)
        self.lay.addWidget(placeholder)
        self.widgets = [placeholder]