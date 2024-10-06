from PyQt6.QtCore import QObject, pyqtSignal
import cv2
import time

class Camera(QObject):
    frameCaptured = pyqtSignal(object)

    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.running = False

    def run(self):
        self.running = True
        cap = cv2.VideoCapture(self.camera_index)
        while self.running:
            ret, frame = cap.read()
            if ret:
                self.frameCaptured.emit(frame)
                time.sleep(0.033)  # Limit to ~30 FPS
            else:
                break
        cap.release()

    def stop(self):
        self.running = False