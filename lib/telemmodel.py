import pandas as pd
from PyQt5.QtWidgets import QMessageBox


class TelemModel:
    def __init__(self, view):
        self._view = view
        self.data = pd.DataFrame()

    def process_data(self, file_path):
        """opens tsv file and store it content to data var, also sets
        view variable to telemetry view and reini UI"""
        temp_data = pd.read_csv(file_path, sep='\t', index_col=0)
        first_step = list(temp_data.index.values)[0]
        temp_data.index = temp_data.index - first_step
        return temp_data

    def display_about(self):
        """Display text about the program"""
        text = '<center>' \
               '<h1>RBR Telemetry Viewer</h1>' \
               '<p>Michal Ungeheuer 2020</p>' \
               '</center>'
        msgbox = QMessageBox.information(self._view, "About program", text)