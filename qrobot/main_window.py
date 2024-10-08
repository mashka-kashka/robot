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
    reset_server_signal = pyqtSignal()
    start_client_signal = pyqtSignal()
    stop_client_signal = pyqtSignal()
    reset_client_signal = pyqtSignal()

    def __init__(self, app):
        super().__init__()

        self.app = app

        self.log_signal.connect(self.on_log)
        self.start_server_signal.connect(self.app.start_server)
        self.stop_server_signal.connect(self.app.stop_server)
        self.reset_server_signal.connect(self.app.reset_server)

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

            if self.ui.actionActivateComputer.isEnabled():
                self.reset_client_signal.emit()
            else:
                self.reset_server_signal.emit()

    def activate_robot(self):
        self.ui.actionActivateRobot.toggle()

    def on_activate_robot(self, start):
        _translate = QtCore.QCoreApplication.translate
        if start:
            self.ui.actionActivateRobot.setStatusTip(_translate("MainWindow", "Отключить робота"))
            self.ui.actionActivateRobot.setText(_translate("MainWindow", "Отключить робота"))
            self.ui.actionActivateRobot.setIconText(_translate("MainWindow", "Отключить робота"))
            self.ui.actionActivateComputer.setEnabled(False)
            self.start_server_signal.emit()
        else:
            self.ui.actionActivateRobot.setStatusTip(_translate("MainWindow", "Активировать робота"))
            self.ui.actionActivateRobot.setText(_translate("MainWindow", "Активировать робота"))
            self.ui.actionActivateRobot.setIconText(_translate("MainWindow", "Активация робота"))
            self.ui.actionActivateComputer.setEnabled(True)
            self.stop_server_signal.emit()

    def activate_computer(self):
        self.ui.actionActivateComputer.toggle()

    def on_activate_computer(self, start):
        _translate = QtCore.QCoreApplication.translate
        if start:
            self.ui.actionActivateComputer.setStatusTip(_translate("MainWindow", "Отключить компьютер"))
            self.ui.actionActivateComputer.setText(_translate("MainWindow", "Отключить компьютер"))
            self.ui.actionActivateComputer.setIconText(_translate("MainWindow", "Отключить компьютер"))
            self.ui.actionActivateRobot.setEnabled(False)
            self.start_client_signal.emit()
        else:
            self.ui.actionActivateComputer.setStatusTip(_translate("MainWindow", "Активировать компьютер"))
            self.ui.actionActivateComputer.setText(_translate("MainWindow", "Активировать компьютер"))
            self.ui.actionActivateComputer.setIconText(_translate("MainWindow", "Активация компьютера"))
            self.ui.actionActivateRobot.setEnabled(True)
            self.stop_client_signal.emit()
