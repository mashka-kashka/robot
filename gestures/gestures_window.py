from time import time, localtime, strftime
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QTextFormat, QColor, QTextCursor, QPixmap, QImage, QIcon
from PyQt6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGridLayout
from PyQt6.QtCore import pyqtSignal, Qt, pyqtSlot
from gestures_window_ui import Ui_GesturesWindow


class GesturesWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_GesturesWindow()
        self.ui.setupUi(self)

        self.logger = self.ui.teLog

        #self.scene = QGraphicsScene()
        #self.ui.gv_camera.setScene(self.scene)
        #self.scenePixmapItem = None

    @pyqtSlot(object)
    def show_frame(self, frame):
        _image = QImage(
            frame.data,
            frame.shape[1],
            frame.shape[0],
            QImage.Format.Format_BGR888,
        )

        _pixmap = QPixmap.fromImage(_image)

        # if self.scenePixmapItem is None:
        #     self.scenePixmapItem = QGraphicsPixmapItem(_pixmap)
        #     self.scene.addItem(self.scenePixmapItem)
        #     self.scenePixmapItem.setZValue(0)
        # else:
        #     self.scenePixmapItem.setPixmap(_pixmap)

        # self.ui.gv_camera.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        # self.ui.gv_camera.show()

    def log(self, message, color):
        fmt = QTextFormat()
        self.logger.moveCursor(QTextCursor.MoveOperation.End)
        self.logger.setTextColor(color)
        self.logger.append(strftime("%H:%M:%S : ", localtime()))
        self.logger.insertPlainText(message)