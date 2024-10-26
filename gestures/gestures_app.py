import numpy
from PyQt6.QtCore import pyqtSlot, QThread, pyqtSignal, QPoint
from PyQt6.QtGui import QColor, QImage, QPainter, QFont
from PyQt6.QtWidgets import QApplication
from google.protobuf.json_format import MessageToDict

from gestures.gestures_model import GesturesNet
from gestures.gestures_window import GesturesWindow
from gestures.robocamera import RoboCamera
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import hands as mp_hand_detector
import torch
import toml
import sys


class GesturesApp(QApplication):
    get_next_frame = pyqtSignal()
    connection = None
    current_frame = None
    label_font = QFont("Times", 20)
    emoji_font = QFont("Noto Color Emoji", 64)
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

        # Нейронная сеть для распознавания жестов
        device = (
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )
        self.log_info(f"Создание нейронной сети с использованием {device}")
        self.gesture_net = GesturesNet().to(device)
        print(self.gesture_net)

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
                min_x = None
                min_y = None
                min_z = None
                max_x = None
                max_y = None
                max_z = None
                for lm in handLandmark.landmark:
                    if not min_x or lm.x < min_x:
                        min_x = lm.x
                    if not min_y or lm.y < min_y:
                        min_y = lm.y
                    if not min_z or lm.z < min_z:
                        min_z = lm.y
                    if not max_x or lm.x > max_x:
                        max_x = lm.x
                    if not max_y or lm.y > max_y:
                        max_y = lm.y
                    if not max_z or lm.z > max_z:
                        max_z = lm.y

        image = QImage(
            frame.data,
            frame.shape[1],
            frame.shape[0],
            QImage.Format.Format_BGR888,
        )

        if self.hand_results.multi_handedness:
            handedness_dict = MessageToDict(self.hand_results.multi_handedness[0])
            classification = handedness_dict['classification'][0]
            painter = QPainter(image)
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(self.label_font)
            painter.drawText(QPoint(5, 25), f"Уверенность: {classification['score']}")
            hand = classification['label']
            if hand == "Left":
                hand = "Правая" # Зеркальное искажение
            else:
                hand = "Левая"
            painter.drawText(QPoint(5, 55), hand)
            painter.drawText(QPoint(5, 85), f"X: {min_x:.2f} {max_x:.2f}")
            painter.drawText(QPoint(5, 115), f"Y: {min_y:.2f} {max_y:.2f}")
            painter.drawText(QPoint(5, 145), f"Z: {min_z:.2f} {max_z:.2f}")

            #painter.setFont(self.emoji_font)
            #painter.drawText(QPoint(5, 140), "👍")

            painter.end()

        self.window.show_palm(image)
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
    app = GesturesApp(sys.argv)
    _main_window = GesturesWindow(app)
    _main_window.show()
    app.start(_main_window)
    app.exec()
    app.stop()
