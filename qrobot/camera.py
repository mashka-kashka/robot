from PyQt6.QtCore import QObject, pyqtSignal
from message_type import MessageType
import time
import cv2
import platform
import toml

class Camera(QObject):
    frame_captured = pyqtSignal(object)
    log = pyqtSignal(object, object)

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
            self.log.emit(f"Камера запущена", MessageType.STATUS)
            while self.running:
                frame = picam2.capture_array()
                self.frame_captured.emit(frame)
                time.sleep(self.config["camera"]["sleep"])
            picam2.stop()
        else:
            cap = cv2.VideoCapture(self.camera_index)
            while self.running:
                ret, frame = cap.read()
                if ret:
                    self.frame_captured.emit(frame)
                    time.sleep(self.config["camera"]["sleep"])
                else:
                    self.log.emit(f"Ошибка камеры", MessageType.ERROR)
                    self.running = False
                    break
            cap.release()

    def stop(self):
        self.running = False
