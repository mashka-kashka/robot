from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow
from net_config_dialog import NetConfigDialog
import netifaces as ni
import toml


class MainWindow(QMainWindow):
    log_signal = pyqtSignal(object, object)
    start_server_signal = pyqtSignal()
    stop_server_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

    def init(self, robot, ui):
        self.robot = robot
        self.log_signal.connect(self.robot.log)
        self.start_server_signal.connect(self.robot.start_server)
        self.stop_server_signal.connect(self.robot.stop_server)
        self.ui = ui

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
