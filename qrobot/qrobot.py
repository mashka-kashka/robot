#!/usr/bin/python3


from time import time, localtime, strftime
from PyQt6.QtGui import QTextFormat, QColor, QTextCursor, QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGridLayout
from PyQt6.QtCore import QObject, QThread, Qt
from camera import Camera
from main import Ui_MainWindow
from messagetype import MessageType

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np
import sys
import cv2
import platform

class QRobot(QObject):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.logger = ui.teLog

        self.thread = QThread()
        self.camera = Camera()
        self.camera.moveToThread(self.thread)
        self.camera.frameCaptured.connect(self.processCameraFrame)
        self.camera.log.connect(self.log)
        self.thread.started.connect(self.camera.run)
        self.thread.start()

        self.graphicsView = QGraphicsView()
        self.graphicsView.show()

        self.cameraLayout = QGridLayout()
        self.cameraLayout.addWidget(self.graphicsView, 0, 0, 1, 1)
        ui.tabCamera.setLayout(self.cameraLayout)

        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.scenePixmapItem = None

        base_options = python.BaseOptions(model_asset_path='models/face_landmarker.task')
        options = vision.FaceLandmarkerOptions(base_options=base_options,
                                              output_face_blendshapes=True,
                                              output_facial_transformation_matrixes=True,
                                              num_faces=1)
        self.faceDetector = vision.FaceLandmarker.create_from_options(options)

    def run(self):
        self.log(f"Начало работы на {platform.uname().system}")
        self.log(f"Версия OpenCV: {cv2.__version__}")

    def draw_landmarks_on_image(self, rgb_image, detection_result):
        face_landmarks_list = detection_result.face_landmarks
        annotated_image = np.copy(rgb_image)

        # Loop through the detected faces to visualize.
        for idx in range(len(face_landmarks_list)):
            face_landmarks = face_landmarks_list[idx]

            # Draw the face landmarks.
            face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            face_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
            ])

            solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles
                .get_default_face_mesh_tesselation_style())
            solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles
                .get_default_face_mesh_contours_style())
            solutions.drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks_proto,
                connections=mp.solutions.face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles
                .get_default_face_mesh_iris_connections_style())

        return annotated_image

    def processCameraFrame(self, frame):
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        detection_result = self.faceDetector.detect(mp_image)

        frame = self.draw_landmarks_on_image(mp_image.numpy_view(), detection_result)
        #cv2_imshow(cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

        image = QImage(
            frame.data,
            frame.shape[1],
            frame.shape[0],
            QImage.Format.Format_BGR888,
        )
        pixmap = QPixmap.fromImage(image)

        if self.scenePixmapItem is None:
            self.scenePixmapItem = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.scenePixmapItem)
            self.scenePixmapItem.setZValue(0)
        else:
            self.scenePixmapItem.setPixmap(pixmap)

        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def stopCamera(self):
        self.camera.stop()
        self.thread.quit()
        self.thread.wait()

    def log(self, message, type = MessageType.STATUS):
        fmt = QTextFormat()
        self.logger.setTextColor(QColor(0, 0, 0))
        self.logger.moveCursor(QTextCursor.MoveOperation.End)
        self.logger.append(strftime("%H:%M:%S : ", localtime()))
        if type == MessageType.ERROR:
            self.logger.setTextColor(QColor(255, 0, 0))
        elif type == MessageType.WARNING:
            self.logger.setTextColor(QColor(255, 255, 0))
        self.logger.moveCursor(QTextCursor.MoveOperation.End)
        self.logger.insertPlainText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    robot = QRobot(ui)
    robot.run()
    MainWindow.show()
    app.exec()
    robot.stopCamera()
