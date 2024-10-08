from time import time, localtime, strftime
from PyQt6 import QtCore
from PyQt6.QtGui import QTextFormat, QColor, QTextCursor, QPixmap, QImage, QIcon
from PyQt6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGridLayout
from PyQt6.QtCore import pyqtSignal, Qt
from main_window_ui import Ui_MainWindow
from log_message_type import LogMessageType
from net_config_dialog import NetConfigDialog
import toml


class QRobotMainWindow(QMainWindow):
    log_signal = pyqtSignal(object, object)
    start_server_signal = pyqtSignal()
    stop_server_signal = pyqtSignal()

    def __init__(self, app):
        super().__init__()

        self.app = app

        self.log_signal.connect(self.on_log)
        self.start_server_signal.connect(self.app.start_server)
        self.stop_server_signal.connect(self.app.stop_server)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.logger = self.ui.teLog

        self.graphicsView = QGraphicsView()
        self.graphicsView.show()

        self.cameraLayout = QGridLayout()
        self.cameraLayout.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.ui.tabCamera.setLayout(self.cameraLayout)

        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.scenePixmapItem = None

    def on_show_image(self, image):
        _image = QImage(
            image.data,
            image.shape[1],
            image.shape[0],
            QImage.Format.Format_BGR888,
        )

        _pixmap = QPixmap.fromImage(_image)

        if self.scenePixmapItem is None:
            self.scenePixmapItem = QGraphicsPixmapItem(_pixmap)
            self.scene.addItem(self.scenePixmapItem)
            self.scenePixmapItem.setZValue(0)
        else:
            self.scenePixmapItem.setPixmap(_pixmap)

        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def on_log(self, message, type=LogMessageType.STATUS):
        fmt = QTextFormat()
        self.logger.setTextColor(QColor(0, 0, 0))
        self.logger.moveCursor(QTextCursor.MoveOperation.End)
        self.logger.append(strftime("%H:%M:%S : ", localtime()))
        if type == LogMessageType.ERROR:
            self.logger.setTextColor(QColor(255, 0, 0))
        elif type == LogMessageType.WARNING:
            self.logger.setTextColor(QColor(255, 255, 0))
        self.logger.moveCursor(QTextCursor.MoveOperation.End)
        self.logger.insertPlainText(message)

    def on_config(self):
        _dialog = NetConfigDialog()
        with open('config.toml', 'r') as f:
            self.config = toml.load(f)
            _dialog.set_video_port(self.config["network"]["video_port"])
            _dialog.set_data_port(self.config["network"]["data_port"])
            _dialog.set_host(self.config["network"]["host"])
        if _dialog.exec():
            self.config["network"]["video_port"] = _dialog.get_video_port()
            self.config["network"]["data_port"] = _dialog.get_data_port()
            self.config["network"]["host"] =_dialog.get_host()
            with open('config.toml', 'w') as f:
                toml.dump(self.config, f)
        else:
            self.ui.actionStartStop.setChecked(False)

    def on_start_stop(self, start):
        _translate = QtCore.QCoreApplication.translate
        if start:
            self.ui.actionStartStop.setStatusTip(_translate("MainWindow", "Остановить передачу данных"))
            self.ui.actionStartStop.setText(_translate("MainWindow", "Остановка"))
            self.ui.actionStartStop.setIconText(_translate("MainWindow", "Остановка"))
            self.start_server_signal.emit()
        else:
            self.ui.actionStartStop.setStatusTip(_translate("MainWindow", "Запустить сервер для передачи данных"))
            self.ui.actionStartStop.setText(_translate("MainWindow", "Запуск"))
            self.ui.actionStartStop.setIconText(_translate("MainWindow", "Запуск"))
            self.stop_server_signal.emit()
