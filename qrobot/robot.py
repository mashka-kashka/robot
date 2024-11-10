import math

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QPoint
from PyQt6.QtGui import QFont, QImage, QPainter, QPen, QColor
import mediapipe as mp
from mediapipe import solutions
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions import hands as mp_hand_detector
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np


class QRobot(QObject):
    emoji_font = QFont("Noto Color Emoji", 64)

    POSE_LANDMARKS = list(range(11, 17))
    POSE_LANDMARKS += list(range(23, 33))
    POSE_SEGMENTS = [[4, 2, 0, 1, 3, 5], [0, 6, 8, 10, 12, 14, 10], [1, 7, 9, 11, 13, 15, 11], [6, 7]]

    def __init__(self):
        super().__init__()

        self.red_pen = QPen()
        self.red_pen.setWidth(2)
        self.red_pen.setColor(QColor(200, 0, 0))
        self.green_pen = QPen()
        self.green_pen.setWidth(2)
        self.green_pen.setColor(QColor(0, 200, 0))

        # Модуль распознавания ладони на изображении
        self.hand_detector = mp_hand_detector.Hands(
            static_image_mode=False,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=6)

        # Модуль распознавания поз на изображении
        base_options = python.BaseOptions(model_asset_path='../models/pose_landmarker_full.task')
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=True,
            num_poses=3)
        self.pose_detector = vision.PoseLandmarker.create_from_options(options)

        # Модуль распознавания лиц на изображении
        base_options = python.BaseOptions(model_asset_path='../models/face_landmarker.task')
        options = vision.FaceLandmarkerOptions(base_options=base_options,
                                              output_face_blendshapes=True,
                                              output_facial_transformation_matrixes=True,
                                              num_faces=3)
        self.face_detector = vision.FaceLandmarker.create_from_options(options)

    # Обработка кадра
    def process_frame(self, image):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

        # Распознавание лиц
        face_detection_result = self.face_detector.detect(mp_image)
        annotated_image = self.draw_faces_on_image(image, face_detection_result)

        # Распознавание рук и поз
        hand_detection_results = self.hand_detector.process(image)
        pose_detection_result = self.pose_detector.detect(mp_image)
        annotated_image = self.draw_poses_on_image(annotated_image, pose_detection_result, hand_detection_results)
        #annotated_image = self.draw_hands_on_image(annotated_image, hand_detection_results)

        return annotated_image

    def draw_poses_on_image(self, rgb_image, pose_detection_result, hand_detection_results):
        height = rgb_image.height()
        width = rgb_image.width()

        pose_landmarks_list = pose_detection_result.pose_landmarks
        hand_landmarks_list = hand_detection_results.multi_hand_landmarks
        wrists = []
        if hand_landmarks_list:
            for lm in hand_landmarks_list:
                wrist = lm.landmark[mp_hands.HandLandmark.WRIST]
                wrists.append((wrist.x, wrist.y, wrist.z))

        landmarks = []
        if pose_landmarks_list:
            for landmark in pose_landmarks_list:
                for idx in self.POSE_LANDMARKS:
                    lm = landmark[idx]
                    point = (lm.x, lm.y, lm.z)
                    if idx == 15 or idx == 16: # Запястье - нужно заменить на координаты руки
                        min_dist = 0.01
                        nearest_wrist_idx = None
                        for wrist_idx, wrist in enumerate(wrists):
                            distance = self.get_distance(point, wrist)
                            if distance < min_dist:
                                min_dist = distance
                                nearest_wrist_idx = wrist_idx
                        if nearest_wrist_idx:
                            landmark.append(wrists[nearest_wrist_idx])
                        else:
                            landmarks.append(point)
                    else:
                        landmarks.append(point)

            painter = QPainter(rgb_image)
            painter.setPen(self.red_pen)
            points = []
            for lm in landmarks:
                x = int(lm[0] * width)
                if x < 0:
                    x = 0
                if x > width:
                    x = width
                y = int(lm[1] * height)
                if y < 0:
                    y = 0
                if y > height:
                    y = height
                points.append(QPoint(x, y))
                painter.drawEllipse(x - 1, y - 1, 2, 2)

            painter.setPen(self.green_pen)
            for segment in self.POSE_SEGMENTS:
                for i in range(1, len(segment)):
                    painter.drawLine(points[segment[i - 1]], points[segment[i]])
            painter.end()

        return rgb_image

    def get_distance(self, a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        dz = a[2] - b[2]
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def draw_hands_on_image(self, rgb_image, detection_result):
        annotated_image = np.copy(rgb_image)
        hand_landmarks_list = detection_result.multi_hand_landmarks
        if hand_landmarks_list:
            for handLandmark in hand_landmarks_list:
                mp_drawing.draw_landmarks(annotated_image, handLandmark,
                                          mp_hand_detector.HAND_CONNECTIONS)
        return annotated_image

    def draw_faces_on_image(self, rgb_image, detection_result):
        face_landmarks_list = detection_result.face_landmarks
        annotated_image = np.copy(rgb_image)

        for idx in range(len(face_landmarks_list)):
            face_landmarks = face_landmarks_list[idx]

            face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            face_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
            ])

            # solutions.drawing_utils.draw_landmarks(
            #     image=annotated_image,
            #     landmark_list=face_landmarks_proto,
            #     connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
            #     landmark_drawing_spec=None,
            #     connection_drawing_spec=mp.solutions.drawing_styles
            #     .get_default_face_mesh_tesselation_style())
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

        image = QImage(
            annotated_image.data,
            annotated_image.shape[1],
            annotated_image.shape[0],
            QImage.Format.Format_BGR888,
        )

        painter = QPainter(image)
        painter.setFont(self.emoji_font)
        #painter.drawText(QPoint(5, 75), "😀")
        painter.end()

        return image
