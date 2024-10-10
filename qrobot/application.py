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
        self.camera.activate_robot_signal.connect(self.window.activate_robot)
        self.camera.activate_computer_signal.connect(self.window.activate_computer)
        self.camera.frame_captured_signal.connect(self.robot.process_image)
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
        self.stop_server()

    def start_server(self):
        with open('config.toml', 'r') as f:
            self.config = toml.load(f)
            _video_port = self.config["network"]["video_port"]
            _data_port = self.config["network"]["data_port"]
            _host = self.config["network"]["host"]

            self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.video_socket.bind((_host, int(_video_port)))
            self.video_socket.listen(1)
            self.log_signal.emit(f"Ожидается подключение к {_host}:{_video_port} для передачи видео", LogMessageType.STATUS)

            #self.video_thread = QThread()
            #self.camera = Camera()
            #self.camera.moveToThread(self.video_thread)
            #self.camera.frame_captured_signal.connect(self.robot.process_image)
            #self.camera.log_signal.connect(self.window.log_signal)
            #self.video_thread.started.connect(self.camera.run)
            #self.video_thread.start()

            self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.data_socket.bind((_host, int(_data_port)))
            self.data_socket.listen(1)
            self.log_signal.emit(f"Ожидается подключение к {_host}:{_data_port} для передачи данных", LogMessageType.STATUS)

    def stop_server(self):
        try:
            self.video_connection.close()
            self.video_thread.quit()
            self.video_thread.wait()

            self.data_connection.close()
            self.data_thread.quit()
            self.data_thread.wait()
        except Exception as e:
            self.log_signal.emit("Нет активных подключений", LogMessageType.STATUS)

    def reset_server(self):
        self.stop_server()
        self.start_server()


        #self.send_video = Thread(target=self.send_video)
        #self.read_data = Thread(target=self.read_data)
        #self.send_video.start()
        #self.read_data.start()



if __name__ == "__main__":
    app = QRobotApplication(sys.argv)
    _main_window = QRobotMainWindow(app)
    _main_window.show()
    app.start(_main_window)
    app.exec()
    app.stop()