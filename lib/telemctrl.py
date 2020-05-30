from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QWidget


class TelemCtrl:
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._data = self._model.data
        self._menuSignals()
        self._file_path = ''
        self._data_tick = 5

    def _menuSignals(self):
        """Connecting signals with menu actions"""
        self._view.openAction.triggered.connect(self.open_file)
        self._view.exitAction.triggered.connect(QApplication.quit)
        self._view.aboutAction.triggered.connect(self._model.display_about)
        self._view.grid1x1Action.triggered.connect(lambda: self.set_grid((1, 1)))
        self._view.grid2x2Action.triggered.connect(lambda: self.set_grid((2, 2)))

    def _telemViewSignals(self):
        """Connecting signals with view actions"""
        self._view.telem_widget.slider.valueChanged.connect(self.sliderChange)

    def sliderChange(self):
        """Update graphs when slider position changes"""
        slider_value = self.sanitize_slider(self._view.telem_widget.slider.value())
        for i in self._view.telem_widget.grid_elements:
            if type(i.widgets[0]) != QWidget:
                i.widgets[0].upd(slider_value)

    def sanitize_slider(self, slider_val):
        """Restrict slider values to match ticks"""
        sanitized_value = int(slider_val/self._data_tick) * self._data_tick
        return sanitized_value

    def open_file(self):
        """loads file path"""
        self._file_path = QFileDialog.getOpenFileName(self._view, 'Open', "", "TSV files (*.tsv)")[0]

        if self._file_path:
            self._data = self._model.process_data(self._file_path)
            self._view.data = self._data
            self._view.reiniUI()
            self._data_tick = list(self._data.index.values)[1] - list(self._data.index.values)[0]
            self._telemViewSignals()

    def set_grid(self, grid):
        """sets proper grid telemetry size"""
        if self._view.grid_type != grid:
            self._view.grid_type = grid
            self._view.reiniUI()
            self._telemViewSignals()
