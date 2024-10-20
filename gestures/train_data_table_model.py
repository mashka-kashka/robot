from operator import index
from venv import create

import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QModelIndex
import pandas as pd
from PyQt6.QtWidgets import QMessageBox
from google.protobuf.json_format import MessageToDict


class TrainDataTableModel(QtCore.QAbstractTableModel):
    modified = False
    file_name = ''

    def __init__(self):
        super(TrainDataTableModel, self).__init__()
        self.create()

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self.data.iloc[index.row(), index.column()]
            if value is np.nan:
                return ""
            else:
                return str(value)

    def rowCount(self, index):
        return self.data.shape[0]

    def columnCount(self, index):
        return self.data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self.data.columns[section])

    def is_modified(self):
        return self.modified

    def get_file_name(self):
        return  self.file_name

    def create(self):
        _landmarks = ['WRIST','THUMB_CMC','THUMB_MCP','THUMB_IP','THUMB_TIP','INDEX_FINGER_MCP','INDEX_FINGER_PIP',
                     'INDEX_FINGER_DIP','INDEX_FINGER_TIP','MIDDLE_FINGER_MCP','MIDDLE_FINGER_PIP','MIDDLE_FINGER_DIP',
                     'MIDDLE_FINGER_TIP','RING_FINGER_MCP','RING_FINGER_PIP','RING_FINGER_DIP','RING_FINGER_TIP',
                     'PINKY_MCP','PINKY_PIP','PINKY_DIP','PINKY_TIP']

        # TODO: Добавить учёт признака левой/правой руки (results.multi_handedness)
        _data = {
                "Жест": pd.Series([], dtype=np.dtype("int8")),
                "Уверенность": pd.Series([], dtype=np.dtype("float")), # confidence
               }

        for i,landmark in enumerate(_landmarks):
            for axis in ['X_', 'Y_', 'Z_']:
                _data[axis+landmark] = pd.Series([], dtype=np.dtype("float"))

        self.data = pd.DataFrame(_data)
        self.modified = False
        self.modelReset.emit()

    def add(self, sample_id, hand_results):
        if hand_results and hand_results.multi_hand_landmarks:
            score = MessageToDict(hand_results.multi_handedness[0])['classification'][0]['score']
            sample = [sample_id, score]
            for lm in hand_results.multi_hand_landmarks[0].landmark:
                sample.append(lm.x)
                sample.append(lm.y)
                sample.append(lm.z)

            self.data = pd.concat([self.data, pd.DataFrame([sample], columns=self.data.columns)], ignore_index=True)
            self.modified = True
            self.modelReset.emit()

    def open(self, filename):
        try:
            df = pd.read_csv(filename)
            if (df.columns == self.data.columns).all():
                self.data = df
                self.file_name = filename
                self.modified = False
                self.modelReset.emit()
        except Exception as e:
            dlg = QMessageBox()
            dlg.setWindowTitle("Невозможно загрузить данные!")
            dlg.setText(f"{e}")
            dlg.setStandardButtons(
                QMessageBox.StandardButton.Ok
            )
            dlg.setIcon(QMessageBox.Icon.Critical)
            button = dlg.exec()

    def save(self, filename):
        self.file_name = filename
        self.data.to_csv(filename, index=False)
        self.modified = False
        self.modelReset.emit()

