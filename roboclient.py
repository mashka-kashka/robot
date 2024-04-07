from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow
from robogui import Ui_MainWindow
from robolog import RoboLog
import sys


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tabWidget.setTabIcon(0, QtGui.QIcon(r"img\gear.png"))
        self.tabWidget.setTabIcon(1, QtGui.QIcon(r"img\hands.png"))

        self.actionConnect.setIcon(QtGui.QIcon(r"img\connect.png"))
        self.actionConnect.triggered.connect(self.on_connect)

        self.actionExit.setIcon(QtGui.QIcon(r"img\exit.png"))
        self.actionExit.triggered.connect(self.close)

        # Перенаправление вывода в окно протокола работы
        sys.stdout = RoboLog(self.log_widget, sys.stdout)
        sys.stderr = RoboLog(self.log_widget, sys.stderr, QtGui.QColor(255, 0, 0))

    def on_connect(self):
        pass

app = QApplication(sys.argv)

win = MainWindow()
win.show()

app.exec()