#!/usr/bin/python3
from PyQt6.QtCore import QThread, Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication

from log_message_type import LogMessageType
from main_window import QRobotMainWindow
from camera import Camera
from robot import QRobot

import platform
import socket
import toml
import sys
import cv2

from server import QRobotServer


class QRobotApplication(QApplication):
    log_signal = pyqtSignal(object, object)
    show_image_signal = pyqtSignal(object)

    def __init__(self, argv):
        super().__init__(argv)

    def start(self, window):
        # Главное окно
        self.window = window
        self.log_signal.connect(self.window.on_log)
        self.log_signal.emit(f"Начало работы на {platform.uname().system}", LogMessageType.STATUS)
        self.log_signal.emit(f"Версия OpenCV: {cv2.__version__}", LogMessageType.STATUS)

        # Робот
        self.robot = QRobot()
        self.robot.show_image_signal.connect(self.window.on_show_image)

        # Камера
        self.camera_thread = QThread()
        self.camera = Camera()
        self.camera.moveToThread(self.camera_thread)
        self.camera.activate_robot_signal.connect(self.window.activate_robot)
        self.camera.activate_computer_signal.connect(self.window.activate_computer)
        self.camera.frame_captured_signal.connect(self.robot.process_image)
        self.camera_thread.started.connect(self.camera.run)
        self.camera_thread.start()

        # Сервер
        self.server_thread = QThread()
        self.server = QRobotServer()
        self.server.moveToThread(self.server_thread)
        self.server.log_signal.connect(self.window.on_log)
        self.server.stop_signal.connect(self.stop_server)
        self.server_thread.started.connect(self.server.start)
        self.window.start_server_signal.connect(self.start_server)
        self.window.stop_server_signal.connect(self.stop_server)
        self.window.reset_server_signal.connect(self.reset_server)

        # Клиент
        self.client_thread = QThread()
        self.client = QRobotServer()
        self.client.moveToThread(self.client_thread)
        self.client.log_signal.connect(self.window.on_log)
        self.client.stop_signal.connect(self.stop_client)
        self.client_thread.started.connect(self.client.start)
        self.window.start_client_signal.connect(self.start_client)
        self.window.stop_client_signal.connect(self.stop_client)
        self.window.reset_client_signal.connect(self.reset_client)

    def stop(self):
        self.stop_camera()
        self.stop_server()
        self.stop_client()

    def stop_camera(self):
        if self.camera_thread.isRunning():
            self.camera.stop()
            self.camera_thread.quit()
            self.camera_thread.wait()

    def start_server(self):
        if not self.server_thread.isRunning():
            self.server_thread.start()

    def stop_server(self):
        if self.server_thread.isRunning():
            self.server.stop()
            self.server_thread.quit()
            self.server_thread.wait()
            if self.window.ui.actionActivateRobot.isChecked(): # При старте произошла ошибка
                self.window.activate_robot()

    def reset_server(self):
        if self.server_thread.isRunning():
            self.server.reset()

    def start_client(self):
        if not self.client_thread.isRunning():
            self.client_thread.start()

    def stop_client(self):
        if self.client_thread.isRunning():
            self.client.stop()
            self.client_thread.quit()
            self.client_thread.wait()
            if self.window.ui.actionActivateComputer.isChecked(): # При старте произошла ошибка
                self.window.activate_computer()

    def reset_client(self):
        if self.client_thread.isRunning():
            self.client.reset()

if __name__ == "__main__":
    app = QRobotApplication(sys.argv)
    _main_window = QRobotMainWindow(app)
    _main_window.show()
    app.start(_main_window)
    app.exec()
    app.stop()