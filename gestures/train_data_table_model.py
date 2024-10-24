from operator import index
from venv import create

import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QModelIndex, QPoint
import pandas as pd
from PyQt6.QtGui import QColor, QPixmap, QPainter, QPen
from PyQt6.QtWidgets import QMessageBox
from google.protobuf.json_format import MessageToDict


class TrainDataTableModel(QtCore.QAbstractTableModel):
    modified = False
    file_name = ''
    size = 27
    white_color = QColor(255, 255, 255)
    landmarks = ['WRIST', 'THUMB_CMC', 'THUMB_MCP', 'THUMB_IP', 'THUMB_TIP', 'INDEX_FINGER_MCP', 'INDEX_FINGER_PIP',
                  'INDEX_FINGER_DIP', 'INDEX_FINGER_TIP', 'MIDDLE_FINGER_MCP', 'MIDDLE_FINGER_PIP', 'MIDDLE_FINGER_DIP',
                  'MIDDLE_FINGER_TIP', 'RING_FINGER_MCP', 'RING_FINGER_PIP', 'RING_FINGER_DIP', 'RING_FINGER_TIP',
                  'PINKY_MCP', 'PINKY_PIP', 'PINKY_DIP', 'PINKY_TIP']

    def __init__(self):
        super(TrainDataTableModel, self).__init__()
        self.create()
        self.red_pen = QPen()
        self.red_pen.setWidth(1)
        self.red_pen.setColor(QColor(200, 0, 0))
        self.green_pen = QPen()
        self.green_pen.setWidth(1)
        self.green_pen.setColor(QColor(0, 200, 0))

    def data(self, index, role):
        if role == Qt.ItemDataRole.DecorationRole:
            if index.column() == 0:
                return self.draw_palm(index.row())
        elif role == Qt.ItemDataRole.DisplayRole:
                value = self.data.iloc[index.row(), index.column()]
                if value is np.nan:
                    return ""
                else:
                    return str(value)

    def draw_palm(self, row_index):
        pixmap = QPixmap(self.size + 3, self.size + 3)
        pixmap.fill(self.white_color)
        try:
            row = self.data.loc[row_index,:]
            painter = QPainter(pixmap)
            painter.setPen(self.red_pen)
            points = []
            for i in range(len(self.landmarks)):
                x = int(row.iloc[i * 3 + 2] * self.size + 1)
                y = int(row.iloc[i * 3 + 3] * self.size + 1)
                points.append(QPoint(x, y))
                painter.drawEllipse(x - 1, y - 1, 2, 2)

            painter.setPen(self.green_pen)
            segments = [[0,1,2,3,4],[0,5,6,7,8],[0,17,18,19,20],[9,10,11,12],[13,14,15,16],[5,9,13,17]]
            for segment in segments:
                for i in range(1, len(segment)):
                    painter.drawLine(points[segment[i - 1]], points[segment[i]])
            painter.end()

        except Exception as e:
            pass
        return pixmap

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
        _data = {
                "Жест": pd.Series([], dtype=np.dtype("int8")),
                "Уверенность": pd.Series([], dtype=np.dtype("float")), # confidence
               }

        for i,landmark in enumerate(self.landmarks):
            for axis in ['X_', 'Y_', 'Z_']:
                _data[axis+landmark] = pd.Series([], dtype=np.dtype("float"))

        self.data = pd.DataFrame(_data)
        self.modified = False
        self.modelReset.emit()

    def add(self, sample_id, hand_results):
        if hand_results and hand_results.multi_hand_landmarks:
            try:
                score = MessageToDict(hand_results.multi_handedness[0])['classification'][0]['score']
                sample = [sample_id, score]

                min_x = None
                min_y = None
                min_z = None
                max_x = None
                max_y = None
                max_z = None
                for lm in hand_results.multi_hand_landmarks[0].landmark:
                    if not min_x or lm.x < min_x:
                        min_x = lm.x
                    if not min_y or lm.y < min_y:
                        min_y = lm.y
                    if not min_z or lm.z < min_z:
                        min_z = lm.y
                    if not max_x or lm.x > max_x:
                        max_x = lm.x
                    if not max_y or lm.y > max_y:
                        max_y = lm.y
                    if not max_z or lm.z > max_z:
                        max_z = lm.y

                dx = max_x - min_x
                dy = max_y - min_y
                dz = max_z - min_z
                scale = max(dx, dy, dz)

                for lm in hand_results.multi_hand_landmarks[0].landmark:
                    sample.append((lm.x - min_x) / scale)
                    sample.append((lm.y - min_y) / scale)
                    sample.append((lm.z - min_z) / scale)

                self.data = pd.concat([self.data, pd.DataFrame([sample], columns=self.data.columns)], ignore_index=True)
                self.modified = True
                self.modelReset.emit()
            except Exception as e:
                dlg = QMessageBox()
                dlg.setWindowTitle("Ошибка добавления данных!")
                dlg.setText(f"{e}")
                dlg.setStandardButtons(
                    QMessageBox.StandardButton.Ok
                )
                dlg.setIcon(QMessageBox.Icon.Critical)
                button = dlg.exec()

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

