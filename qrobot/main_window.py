from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow
from message_type import MessageType
import netifaces as ni

class MainWindow(QMainWindow):
    on_start_stop = pyqtSignal(bool)
    log = pyqtSignal(object, object)

    def __init__(self):
        super().__init__()

    def init(self, robot, ui):
        self.robot = robot
        self.log.connect(self.robot.log)

        self.ui = ui

    def on_start_stop(self, start):
        _translate = QtCore.QCoreApplication.translate
        if start:
            self.ui.actionStartStop.setStatusTip(_translate("MainWindow", "Остановить передачу данных"))
            self.ui.actionStartStop.setText(_translate("MainWindow", "Остановка"))
            self.ui.actionStartStop.setIconText(_translate("MainWindow", "Остановка"))
            address = ni.ifaddresses('wlp15s0')[ni.AF_INET][0]['addr']
            self.log.emit(f"Запуск сервера на {address}", MessageType.STATUS)
        else:
            self.ui.actionStartStop.setStatusTip(_translate("MainWindow", "Запустить сервер для передачи данных"))
            self.ui.actionStartStop.setText(_translate("MainWindow", "Запуск"))
            self.ui.actionStartStop.setIconText(_translate("MainWindow", "Запуск"))
            self.log.emit("Сервер остановлен", MessageType.STATUS)
