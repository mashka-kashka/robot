from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication
from gestures.gestures_window import GesturesWindow
import robocamera
import sys


class GesturesApp(QApplication):
    connection = None

    def __init__(self, argv):
        super().__init__(argv)

    def start(self, window):
        self.window = window
        self.log_info(f"Начало работы")

        # # Камера
        # self.camera_thread = QThread()
        # self.camera = Camera()
        # self.camera.moveToThread(self.camera_thread)
        # self.camera.activate_robot_signal.connect(self.window.activate_robot)
        # self.camera.activate_computer_signal.connect(self.window.activate_computer)
        # self.camera.frame_captured_signal.connect(self.on_frame_captured)
        # self.get_frame_signal.connect(self.camera.get_frame)
        # self.camera_thread.started.connect(self.camera.start)
        # self.camera_thread.start()

    def stop(self):
        self.stop_camera()

    @pyqtSlot(object)
    def log_info(self, message):
        self.window.log(message, QColor(0, 0, 0))

    @pyqtSlot(object)
    def log_warning(self, message):
        self.window.log(message, QColor(0, 0, 255))

    @pyqtSlot(object)
    def log_error(self, message):
        self.window.log(message, QColor(255, 0, 0))

if __name__ == "__main__":
    app = GesturesApp(sys.argv)
    _main_window = GesturesWindow()
    _main_window.show()
    app.start(_main_window)
    app.exec()
    app.stop()
