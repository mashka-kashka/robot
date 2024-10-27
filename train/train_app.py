import numpy
from PyQt6.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QImage
from PyQt6.QtWidgets import QApplication
from train.train_window import TrainWindow
from train.robocamera import RoboCamera
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import hands as mp_hand_detector
import toml
import sys


class TrainApp(QApplication):
    get_next_frame = pyqtSignal()
    connection = None
    current_frame = None
    hand_results = None

    def __init__(self, argv):
        super().__init__(argv)

    def start(self, window):
        self.window = window
        self.log_info(f"Начало работы")

        # Модуль распознавания ладони на изображении
        self.hand_detector = hand_detector = mp_hand_detector.Hands(
            static_image_mode=False,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=1)

        with open('config.toml', 'r') as f:
            self.config = toml.load(f)

        # Камера
        self.camera_thread = QThread()
        self.camera = RoboCamera(self.config)
        self.camera.moveToThread(self.camera_thread)
        self.camera.started_signal.connect(self.camera_started)
        self.camera.failed_signal.connect(self.camera_failed)
        self.camera.frame_captured_signal.connect(self.frame_captured)
        self.get_next_frame.connect(self.camera.get_frame)
        self.camera_thread.started.connect(self.camera.start)
        self.camera_thread.start()

    def stop(self):
        if self.camera_thread.isRunning():
            self.camera.stop()
            self.camera_thread.quit()
            self.camera_thread.wait()

    @pyqtSlot()
    def camera_started(self):
        self.log_info("Успешное подключение камеры")

    @pyqtSlot()
    def camera_failed(self):
        self.log_error("Не удалось подключить камеру")

    @pyqtSlot(object)
    def frame_captured(self, frame):
        self.hand_results = self.hand_detector.process(frame)
        if self.hand_results.multi_hand_landmarks:
            for handLandmark in self.hand_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, handLandmark,
                                          mp_hand_detector.HAND_CONNECTIONS)
        image = QImage(
            frame.data,
            frame.shape[1],
            frame.shape[0],
            QImage.Format.Format_BGR888,
        )

        self.window.show_palm(image, self.hand_results)
        self.get_next_frame.emit()

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
    app = TrainApp(sys.argv)
    _main_window = TrainWindow(app)
    _main_window.show()
    app.start(_main_window)
    app.exec()
    app.stop()
