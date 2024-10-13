from PyQt6.QtCore import QObject, pyqtSignal
from log_message_type import LogMessageType
import time
import cv2
import platform
import toml

class Camera(QObject):
    activate_robot_signal = pyqtSignal(bool)
    activate_computer_signal = pyqtSignal(bool)
    frame_captured_signal = pyqtSignal(object)

    def __init__(self, camera_index=0):
        super().__init__()
        with open('config.toml', 'r') as f:
            self.config = toml.load(f)
        self.camera_index = camera_index
        self.running = False

    def run(self):
        self.running = True
        if platform.uname().system == "raspberrypi":
            from picamera2 import Picamera2
            picam2 = Picamera2()
            picam2.configure(picam2.create_preview_configuration(
                main={"format": 'RGB888', "size": (self.config["camera"]["width"], self.config["camera"]["height"])}))
            picam2.start() # запускаем камеру
            self.activate_robot_signal.emit(False)
            while self.running:
                frame = picam2.capture_array()
                self.frame_captured_signal.emit(frame)
                time.sleep(self.config["camera"]["sleep"])
            picam2.stop()
        else:
            cap = cv2.VideoCapture(self.camera_index)
            if cap.isOpened():
                while self.running:
                    ret, frame = cap.read()
                    if ret:
                        self.frame_captured_signal.emit(frame)
                        time.sleep(self.config["camera"]["sleep"])
                    else:
                        self.running = False
                        break
            else:
                self.running = False
                self.activate_computer_signal.emit(False)
            cap.release()

    def stop(self):
        self.running = False
