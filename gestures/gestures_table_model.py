from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QSize
import pandas as pd
from PyQt6.QtGui import QFont


class GesturesTableModel(QtCore.QAbstractTableModel):
    UNICODE_COLUMN = 1
    NAME_COLUMN = 2

    def __init__(self):
        super(GesturesTableModel, self).__init__()
        self.data = pd.read_csv('gestures.csv')
        self.noto_font = QFont("Noto Color Emoji", 20)
        self.unicode_column_size = QSize(100, 50)
        self.name_column_size = QSize(300, 50)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self.data.iloc[index.row(), index.column()]
            return str(value)
        elif role == Qt.ItemDataRole.FontRole and index.column() == self.UNICODE_COLUMN:
            return self.noto_font
        elif role == Qt.ItemDataRole.TextAlignmentRole and index.column() == self.UNICODE_COLUMN:
            return Qt.AlignmentFlag.AlignHCenter

    def rowCount(self, index):
        return self.data.shape[0]

    def columnCount(self, index):
        return self.data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self.data.columns[section])
