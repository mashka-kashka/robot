from random import sample
from time import time, localtime, strftime
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QTextFormat, QColor, QTextCursor, QPixmap, QImage, QIcon
from PyQt6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGridLayout
from PyQt6.QtCore import pyqtSignal, Qt, pyqtSlot

from gestures.gestures_table_model import GesturesTableModel
from gestures_window_ui import Ui_GesturesWindow


class GesturesWindow(QMainWindow):

    def __init__(self, app):
        super().__init__()

        self.app = app

        self.ui = Ui_GesturesWindow()
        self.ui.setupUi(self)

        self.table_model = GesturesTableModel()
        self.ui.tv_gestures.setModel(self.table_model)

        self.ui.cb_gestures.setModel(self.table_model)
        self.ui.cb_gestures.setModelColumn(GesturesTableModel.UNICODE_COLUMN)

        self.scene = QGraphicsScene()
        self.ui.gv_palm.setScene(self.scene)
        self.scenePixmapItem = None

        self.logger = self.ui.teLog

        #self.scene = QGraphicsScene()
        #self.ui.gv_camera.setScene(self.scene)
        #self.scenePixmapItem = None

    def is_palm_visible(self):
        return not self.ui.gv_palm.visibleRegion().isEmpty()

    @pyqtSlot(object)
    def show_palm(self, frame):
        _image = QImage(
            frame.data,
            frame.shape[1],
            frame.shape[0],
            QImage.Format.Format_BGR888,
        )

        _pixmap = QPixmap.fromImage(_image)

        if self.scenePixmapItem is None:
            self.scenePixmapItem = QGraphicsPixmapItem(_pixmap)
            self.scene.addItem(self.scenePixmapItem)
            self.scenePixmapItem.setZValue(0)
        else:
            self.scenePixmapItem.setPixmap(_pixmap)

        self.ui.gv_palm.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.gv_palm.show()

    def log(self, message, color):
        fmt = QTextFormat()
        self.logger.moveCursor(QTextCursor.MoveOperation.End)
        self.logger.setTextColor(color)
        self.logger.append(strftime("%H:%M:%S : ", localtime()))
        self.logger.insertPlainText(message)

    @pyqtSlot()
    def on_add_sample(self):
        sample_index = self.ui.cb_gestures.currentIndex()
        self.app.add_sample(self.ui.cb_gestures.currentIndex())