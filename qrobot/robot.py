import math
import json
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
import pandas as pd
from triton.language import dtype


class QRobot(QObject):
    HAND_LANDMARKS = ['WRIST', 'THUMB_CMC', 'THUMB_MCP', 'THUMB_IP', 'THUMB_TIP', 'INDEX_FINGER_MCP',
                      'INDEX_FINGER_PIP',
                      'INDEX_FINGER_DIP', 'INDEX_FINGER_TIP', 'MIDDLE_FINGER_MCP', 'MIDDLE_FINGER_PIP',
                      'MIDDLE_FINGER_DIP',
                      'MIDDLE_FINGER_TIP', 'RING_FINGER_MCP', 'RING_FINGER_PIP', 'RING_FINGER_DIP', 'RING_FINGER_TIP',
                      'PINKY_MCP', 'PINKY_PIP', 'PINKY_DIP', 'PINKY_TIP']
    POSE_LANDMARKS = ['LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW', 'LEFT_HIP', 'RIGHT_HIP',
                       'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE', 'RIGHT_ANKLE', 'LEFT_HEEL', 'RIGHT_HEEL',
                       'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX']
    POSE_LANDMARK_IDS = list(range(11, 15)) + list(range(23, 33))
    ROBOT_SEGMENTS = ([[0, 1, 2, 3, 4], [0, 5, 6, 7, 8], [0, 17, 18, 19, 20], [9, 10, 11, 12], [13, 14, 15, 16],
                      [5, 9, 13, 17], [21, 22, 23, 24, 25], [21, 26, 27, 28, 29], [21, 38, 39, 40, 41],
                      [30, 31, 32, 33], [34, 35, 36, 37], [26, 30, 34, 38], [0, 44, 42, 43, 45, 21],
                      [43, 47, 49, 51, 53, 55, 51], [42, 46, 48, 50, 52, 54, 50], [46, 47]])
    ARM_PREFIXES = ['LEFT_', 'RIGHT_']

    def __init__(self):
        super().__init__()

        self.red_pen = QPen()
        self.red_pen.setWidth(3)
        self.red_pen.setColor(QColor(200, 0, 0))
        self.green_pen = QPen()
        self.green_pen.setWidth(3)
        self.green_pen.setColor(QColor(0, 200, 0))
        self.emoji_font = QFont("Noto Color Emoji", 64)
        self.robot_data = {}

        # Список наименований ключевых точек
        QRobot.ROBOT_LANDMARKS = []
        for prefix in QRobot.ARM_PREFIXES:
            self.ROBOT_LANDMARKS += [prefix + x for x in QRobot.HAND_LANDMARKS]
        QRobot.ROBOT_LANDMARKS += QRobot.POSE_LANDMARKS

        # Модуль распознавания ладони на изображении
        self.hand_detector = mp_hand_detector.Hands(
            static_image_mode=False,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=2)

        # Модуль распознавания поз на изображении
        base_options = python.BaseOptions(model_asset_path='../models/pose_landmarker_full.task')
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=True,
            num_poses=1)
        self.pose_detector = vision.PoseLandmarker.create_from_options(options)

        # Модуль распознавания лиц на изображении
        base_options = python.BaseOptions(model_asset_path='../models/face_landmarker.task')
        options = vision.FaceLandmarkerOptions(base_options=base_options,
                                              output_face_blendshapes=True,
                                              output_facial_transformation_matrixes=True,
                                              num_faces=1)
        self.face_detector = vision.FaceLandmarker.create_from_options(options)

    def get_ranges(self, input_list, width, height):
        x_min = x_max = None
        y_min = y_max = None
        z_min = z_max = None
        visible = False
        data = None
        if input_list:
            for lm in input_list:
                if not x_min or lm.x < x_min:
                    x_min = max(0.0, lm.x)
                if not y_min or lm.y < y_min:
                    y_min = max(0.0, lm.y)
                if not z_min or lm.z < z_min:
                    z_min = max(0.0, lm.z)
                if not x_max or lm.x > x_max:
                    x_max = min(1.0, lm.x)
                if not y_max or lm.y > y_max:
                    y_max = min(1.0, lm.y)
                if not z_max or lm.z > z_max:
                    z_max = min(1.0, lm.z)
                if x_min > 0.0 or x_max < 1.0 or y_min > 0.0 or y_max < 1.0:
                    visible = True
            data = {'visible': visible, 'x_min': x_min, 'x_max': x_max,
                    'y_min': y_min, 'y_max': y_max, 'z_min': z_min, 'z_max': z_max,
                    'rect': (int(x_min * width), int(y_min * height), int(x_max * width), int(y_max * height))}
        return data
    # Обработка кадра
    def process_frame(self, image):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        height = mp_image.height
        width = mp_image.width

        data = {'Кадр' : {'Ширина' : width, 'Высота' : height}}

        # Распознавание лиц
        face_detection_result = self.face_detector.detect(mp_image)
        annotated_image = self.draw_faces_on_image(image, face_detection_result)

        if len(face_detection_result.face_landmarks) > 0:
            data['Лицо'] = self.get_ranges(face_detection_result.face_landmarks[0], width, height)

        # Распознавание рук и поз
        hand_detection_results = self.hand_detector.process(image)
        hand_landmarks_list = hand_detection_results.multi_hand_landmarks
        if hand_landmarks_list:
            for idx, lm in enumerate(hand_landmarks_list):
                bounds = self.get_ranges(lm.landmark, width, height)
                classification = hand_detection_results.multi_handedness[idx].classification[0]
                data["Правая ладонь" if classification.label == 'Left' else "Левая ладонь"] = bounds

        sceleton = {}
        pose_detection_result = self.pose_detector.detect(mp_image)
        pose_landmarks_list = pose_detection_result.pose_landmarks
        if pose_landmarks_list:
            for i, idx in enumerate(QRobot.POSE_LANDMARK_IDS):
                lm = pose_landmarks_list[0][idx]
                if lm.visibility > 0.9:
                    sceleton[QRobot.POSE_LANDMARKS[i]] = {'x': lm.x, 'y': lm.y, 'z': lm.z,
                                                          'point': (int(lm.x * width), int(lm.y * height))}

        if hand_landmarks_list:
            for idx, lm in enumerate(hand_landmarks_list):
                is_right_palm = hand_detection_results.multi_handedness[idx].classification[0].label == 'Left'
                for pidx, pt in enumerate(lm.landmark):
                    if is_right_palm:
                        sceleton['RIGHT_' + QRobot.HAND_LANDMARKS[pidx]] = {'x': pt.x, 'y': pt.y, 'z': pt.z,
                                                                            'point': (int(pt.x * width),
                                                                                      int(pt.y * height))}
                    else:
                        sceleton['LEFT_' + QRobot.HAND_LANDMARKS[pidx]] = {'x': pt.x, 'y': pt.y, 'z': pt.z,
                                                                           'point': (int(pt.x * width),
                                                                                     int(pt.y * height))}

        data['Скелет'] = sceleton
#        with open("sceleton.json", "w") as outfile:
#            json.dump(data, outfile)

        annotated_image = self.draw_sceleton_on_image(annotated_image, data)

        #annotated_image = self.draw_poses_on_image(annotated_image, pose_detection_result, hand_detection_results)
        #annotated_image = self.draw_hands_on_image(annotated_image, hand_detection_results)

        return annotated_image

    def draw_sceleton_on_image(self, image, data):
        painter = QPainter(image)
        painter.setFont(self.emoji_font)
        #painter.drawText(QPoint(5, 75), "😀")
        sceleton = data['Скелет']
        painter.setPen(self.green_pen)
        for segment in QRobot.ROBOT_SEGMENTS:
            for i in range(1, len(segment)):
                start_lm = self.ROBOT_LANDMARKS[segment[i - 1]]
                if not start_lm in sceleton:
                    continue

                end_lm = self.ROBOT_LANDMARKS[segment[i]]
                if not end_lm in sceleton:
                    continue

                a = sceleton[start_lm]['point']
                b = sceleton[end_lm]['point']
                painter.drawLine(a[0], a[1], b[0], b[1])
        painter.end()
        return image

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
                for idx in self.POSE_LANDMARK_IDS:
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
            for segment in self.ROBOT_SEGMENTS:
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
