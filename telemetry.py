import sys
import pandas as pd

# helpers imports
from lib.telemmodel import TelemModel
from lib.telemctrl import TelemCtrl
from lib.telemui import TelemUI

# PyQt imports
from PyQt5.QtWidgets import QApplication

# matplotlib imports
import matplotlib
matplotlib.use('Qt5Agg')


data = pd.DataFrame()


def main():
    # initialize application
    rbrtelem = QApplication(sys.argv)

    # initialize view, and display it
    view = TelemUI()
    view.show()

    # initialize model
    model = TelemModel(view)

    # initialize controller
    ctrl = TelemCtrl(model, view)

    # execute app
    sys.exit(rbrtelem.exec())


if __name__ == '__main__':
    main()