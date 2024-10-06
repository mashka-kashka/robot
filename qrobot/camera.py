from PyQt6.QtCore import QObject, pyqtSignal
from messagetype import MessageType
from picamera2 import Picamera2
import time
import cv2
import os


# Параметры кадра
FRAME_WIDTH = 1024  
FRAME_HEIGHT = 768
SLEEP_TIME = 0.033

class Camera(QObject):
    frameCaptured = pyqtSignal(object)
    log = pyqtSignal(object, object)

    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.running = False

    def run(self):
        self.running = True
        if os.uname().nodename == "raspberrypi":
            picam2 = Picamera2()
            picam2.configure(picam2.create_preview_configuration(
                main={"format": 'RGB888', "size": (FRAME_WIDTH, FRAME_HEIGHT)}))
            picam2.start() # запускаем камеру
            self.log.emit(f"camera started", MessageType.ERROR)
            while self.running:
                frame = picam2.capture_array()
                self.frameCaptured.emit(frame)
                time.sleep(SLEEP_TIME)
            picam2.stop()
        else:
            cap = cv2.VideoCapture(self.camera_index)
            while self.running:
                ret, frame = cap.read()
                if ret:
                    self.frameCaptured.emit(frame)
                    time.sleep(SLEEP_TIME)
                else:
                    self.log.emit(f"camera error", MessageType.ERROR)
                    self.running = False
                    break
            cap.release()

    def stop(self):
        self.running = False
