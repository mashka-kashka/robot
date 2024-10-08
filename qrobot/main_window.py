from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow
from message_type import MessageType

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
