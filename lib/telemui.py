from lib.telemetrywidget import TelemetryWidget

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMenu


class TelemUI(QMainWindow):
    """Class represents main UI"""
    def __init__(self):
        super().__init__()
        # setting window title
        self.setWindowTitle("RBR Telemetry Viewer")
        # setting minimum window size
        self.setMinimumSize(800, 600)
        # setting default grid type
        self.grid_type = (1, 1)
        # setting default view to intro screen
        self.telem_view = 0
        # creating menu
        self._createMenu()
        # setting main layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget()
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)
        self.initUI()

    def initUI(self, data=None):
        """setting proper view depending on telem_view"""
        if self.telem_view:
            # set telemetry screen, enable grid menu
            self.gridMenu.setDisabled(False)
            self._telem_screen(data)
        else:
            # set intro screen
            self._intro_screen()

    def reiniUI(self, data):
        """Cleans general layout, then make new one"""
        self.clear_layout(self.generalLayout)
        self.initUI(data)

    def _intro_screen(self):
        """Displays intro screen at main layout"""
        self.introWidget = QLabel('<center>Load telemetry data using file menu (or use Ctrl+O)</center>')
        self.generalLayout.addWidget(self.introWidget, alignment=Qt.AlignCenter)

    def _telem_screen(self, data):
        """Displays telemetry screen at main layout"""
        self.telem_widget = TelemetryWidget(self, self.generalLayout, self.grid_type, data)
        self.generalLayout.addWidget(self.telem_widget, alignment=Qt.AlignCenter)

    def _createMenu(self):
        """Creates menus for UI"""
        self.openAction = QAction('Open', self)
        self.openAction.setShortcut('Ctrl+O')
        self.exitAction = QAction('Exit', self)
        self.aboutAction = QAction('About', self)

        self.gridMenu = QMenu('Grid', self)
        self.gridMenu.setDisabled(True)
        self.grid1x1Action = QAction('1x1', self)
        self.grid2x2Action = QAction('2x2', self)
        self.gridMenu.addAction(self.grid1x1Action)
        self.gridMenu.addAction(self.grid2x2Action)

        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        file_menu.addAction(self.openAction)
        file_menu.addMenu(self.gridMenu)
        file_menu.addAction(self.exitAction)

        info_menu = menubar.addMenu('Info')
        info_menu.addAction(self.aboutAction)

    def clear_layout(self, layout):
        """Clears entirely given layout"""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())
