from PyQt6.QtWidgets import QApplication, QMainWindow
import robogui
import sys


class MainWindow(QMainWindow, robogui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.actionExit.triggered.connect(self.close)

app = QApplication(sys.argv)

win = MainWindow()
win.show()

app.exec()