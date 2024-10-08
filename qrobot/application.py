#!/usr/bin/python3
from PyQt6.QtCore import QThread, Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication

from log_message_type import LogMessageType
from main_window import QRobotMainWindow
from camera import Camera
from robot import QRobot

import platform
import toml
import sys
import cv2


class QRobotApplication(QApplication):
    log_signal = pyqtSignal(object, object)
    show_image_signal = pyqtSignal(object)

    def __init__(self, argv):
        super().__init__(argv)

    def start(self, window):
        self.window = window
        self.robot = QRobot()

        # Камера
        self.camera_thread = QThread()
        self.camera = Camera()
        self.camera.moveToThread(self.camera_thread)
        self.camera.frame_captured_signal.connect(self.robot.process_image)
        self.camera.log_signal.connect(self.window.log_signal)
        self.camera_thread.started.connect(self.camera.run)
        self.camera_thread.start()

        # Робот
        self.robot.show_image_signal.connect(self.window.on_show_image)

        self.log_signal.connect(self.window.on_log)
        self.log_signal.emit(f"Начало работы на {platform.uname().system}", LogMessageType.STATUS)
        self.log_signal.emit(f"Версия OpenCV: {cv2.__version__}", LogMessageType.STATUS)

    def stop(self):
        self.camera.stop()
        self.camera_thread.quit()
        self.camera_thread.wait()

    def start_server(self):
        self.server_started = True
        self.log_signal.emit("Сервер запущен", LogMessageType.STATUS)

    def stop_server(self):
        if self.server_started:
            self.server_started = False
            self.log_signal.emit("Сервер остановлен", LogMessageType.STATUS)

if __name__ == "__main__":
    app = QRobotApplication(sys.argv)
    _main_window = QRobotMainWindow(app)
    _main_window.show()
    app.start(_main_window)
    app.exec()
    app.stop()