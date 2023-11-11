#!/usr/bin/python3

import os

# Определяем тип платформы
raspberry = (os.uname()[1] == 'raspberrypi')

if raspberry: # Подключаем только на Raspberry Pi
    from servo import *
    from picamera2 import Picamera2
    from gpiozero import CPUTemperature
    
from datetime import datetime
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import face_detection as mp_face_detector
from mediapipe.python.solutions import hands as mp_hand_detector
import mediapipe as mp
import cv2
import json

# Параметры кадра
FRAME_WIDTH = 1024  
FRAME_HEIGHT = 768
MARGIN = 10 # отступ от края
ROW_SIZE = 30 # высота строки текста

# Ограничения горизонтального перемещения
INIT_HOR_POSITION = 0 # начальный горизонтальный поворот камеры
MIN_HOR_ANGLE = 10 # минимальный угол поворота камеры по горизонтали
MAX_HOR_ANGLE = 130 # максимальный угол по горизонтали
HOR_STEP = 2 # горизонтальный шаг поворота камеры в градусах
# горизонтальный шаг в пикселях
HOR_DELTA = 10 * HOR_STEP / 180 * 3.141 * FRAME_WIDTH

# Ограничения вертикального перемещения
INIT_VERT_POSITION = 30 # начальный вертикальный поворота камеры
MIN_VERT_ANGLE = 80 # минимальный угол поворота камеры по вертикали
MAX_VERT_ANGLE = 150 # максимальный угол поворота камеры по вертикали
VERT_STEP = 2 # вертикальный шаг поворота камеры в градусах 
# вертикальный шаг в пикселях
VERT_DELTA = 10 * VERT_STEP / 180 * 3.141 * FRAME_HEIGHT

pwm = Servo() 
cpu = CPUTemperature()
font = cv2.FONT_HERSHEY_COMPLEX

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(
  main={"format": 'BGR888', "size": (FRAME_WIDTH, FRAME_HEIGHT)}))
picam2.start() # запускаем камеру

cv2.startWindowThread() # запускаем модуль компьютерного зрения

# поворачиваем камеру в начальное положение
hor_position = 70
vert_position = 90
pwm.setServoPwm('0', hor_position)
pwm.setServoPwm('1', vert_position)

SEARCH_DELAY = 5 # задержка перед началом поиска лиц
# шаги поиска лиц
hor_search_step = HOR_STEP
vert_search_step = VERT_STEP
view_time = datetime.now()
palm_time = 0
fist_time = 0
detect_object_mode = False
say_hello = True

# Загружаем словарь
dictionary = {}
with open('dictionary.json') as f: 
    dictionary = json.loads(f.read())

# Модуль обнаружения рук
tip=[8,12,16,20]
hand_detector = mp_hand_detector.Hands(
    static_image_mode=False, 
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7, 
    max_num_hands=2)
                        
# Модуль обнаружения лиц
face_detector = mp_face_detector.FaceDetection(
    min_detection_confidence=0.7, 
    model_selection=0)
                                
# Модуль обнаружения объектов
base_options = mp_python.BaseOptions(
	# efficientdet.tflite
    model_asset_path='./models/efficientdet_lite0.tflite')
options = mp_vision.ObjectDetectorOptions(
    base_options=base_options,
    running_mode=mp_vision.RunningMode.IMAGE,
    max_results=3, 
    score_threshold=0.3)
object_detector = mp_vision.ObjectDetector.create_from_options(options)

# Отображение температуры процессора
def print_cpu_temperature(image):
    # Настраиваем цвет в зависимости от температуры процессора
    text_color =  (0, 200, 0)
    if (cpu.temperature > 60):
        text_color = (0, 200, 200)
    if (cpu.temperature > 80):
        text_color = (0, 0, 200)
        
    cv2.putText(image, f'Температура процессора: {int(cpu.temperature)}', 
        (10, 30), font, 1, text_color, 1, cv2.LINE_AA)

# Поиск лиц
def search_face_detector(): 
    global hor_position
    global hor_search_step
    global vert_position
    global vert_search_step
    
    # Поиск по горизонтали
    hor_position = hor_position + hor_search_step
    if hor_search_step > 0 and hor_position > MAX_HOR_ANGLE:
        hor_position = MAX_HOR_ANGLE
        hor_search_step = hor_search_step * -1
    elif hor_search_step < 0 and hor_position < MIN_HOR_ANGLE:
        hor_position = MIN_HOR_ANGLE
        hor_search_step = hor_search_step * -1
        # Поиск по вертикали
        vert_position = vert_position + vert_search_step
        if vert_search_step > 0 and vert_position > MAX_VERT_ANGLE:
            vert_position = MAX_VERT_ANGLE
            vert_search_step = vert_search_step * -1
        elif vert_search_step < 0 and vert_position < MIN_VERT_ANGLE:
            vert_position = MIN_VERT_ANGLE
            vert_search_step = vert_search_step * -1
        pwm.setServoPwm('1', vert_position)
    pwm.setServoPwm('0', hor_position)
    #print(f"hor {hor_position} vert {vert_position}")
    
# Отслеживание лиц
def track_detections(image, detections):
    global hor_position
    global vert_position
    
    image_rows, image_cols, _ = image.shape
    left = image_cols
    right = 0
    top = 0
    bottom = image_rows
        
    for detection in detections:
        location = detection.location_data
        if not location.HasField('relative_bounding_box'):
            continue
        relative_bounding_box = location.relative_bounding_box
        lb = mp_drawing._normalized_to_pixel_coordinates(
          relative_bounding_box.xmin, relative_bounding_box.ymin, 
          image_cols, image_rows)
        if not lb:
            continue
        rt = mp_drawing._normalized_to_pixel_coordinates(
          relative_bounding_box.xmin + relative_bounding_box.width,
          relative_bounding_box.ymin + relative_bounding_box.height, 
          image_cols, image_rows)
        if not rt:
            continue

        cv2.rectangle(image, lb, rt, (255, 255, 255), 2)
              
        l, b = lb
        r, t = rt
    
        if l < left:
            left = l
        if r > right:
            right = r
        if b < bottom:
            bottom = b
        if t > top:
            top = t
            
    right = FRAME_WIDTH - right
    top = FRAME_HEIGHT - top
    
    if right - left > HOR_DELTA:

        hor_position = hor_position - HOR_STEP
        if (hor_position < MIN_HOR_ANGLE):
            hor_position = MIN_HOR_ANGLE
        pwm.setServoPwm('0', hor_position)            
    elif left - right > HOR_DELTA:
        hor_position = hor_position + HOR_STEP
        if (hor_position > MAX_HOR_ANGLE):
            hor_position = MAX_HOR_ANGLE
        pwm.setServoPwm('0', hor_position)

    if top - bottom > VERT_DELTA:
        vert_position = vert_position + VERT_STEP
        if (vert_position > MAX_VERT_ANGLE):
            vert_position = MAX_VERT_ANGLE
        pwm.setServoPwm('1', vert_position)
    elif bottom - top > VERT_DELTA:
        vert_position = vert_position - VERT_STEP
        if (vert_position < MIN_VERT_ANGLE):
            vert_position = MIN_VERT_ANGLE
        pwm.setServoPwm('1', vert_position)

while True:
	# Получаем следующий кадр от камеры
    frame = picam2.capture_array()
           
    # Отображение температуры процессора
    print_cpu_temperature(frame)
    
    # Обнаружение рук в кадре
    results = hand_detector.process(frame)
    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            view_time = datetime.now()
            
            segments=[]
            for id, pt in enumerate(handLandmarks.landmark):
                 x = int(pt.x * FRAME_WIDTH)
                 y = int(pt.y * FRAME_HEIGHT)
                 segments.append([id, x, y])
            
            fingers_up = 0
            if (len(segments) != 0):
                if segments[0][1:] < segments[4][1:]: 
                    fingers_up = 1
                    
                for id in range(0,4):
                    if segments[tip[id]][2:] < segments[tip[id]-2][2:]:
                        fingers_up += 1
            
            # Переключение режима распознавания объектов
            if fingers_up == 5:
                palm_time = datetime.now()
                if fist_time != 0:
                    time_diff = palm_time - fist_time
                    if time_diff.total_seconds() < 2:
                        detect_object_mode = False                
            elif fingers_up < 2:
                fist_time = datetime.now()
                if palm_time != 0:
                    time_diff = fist_time - palm_time
                    if time_diff.total_seconds() < 2:
                        detect_object_mode = True

            if not detect_object_mode:
                cv2.putText(frame, 
                    f'Поднято пальцев {fingers_up}', 
                    (10, 60), font, 1, (255, 255, 255), 1, cv2.LINE_AA) 
                
                # Отображение пальцев
                mp_drawing.draw_landmarks(frame, handLandmarks, 
                            mp_hand_detector.HAND_CONNECTIONS)
    
    if detect_object_mode # Если робот в режиме обнаружения объектов
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        detection_result = object_detector.detect(mp_image)
        if detection_result:
            # print(detection_result)
            for detection in detection_result.detections:
                # Отображение рамки
                bbox = detection.bounding_box
                start_point = bbox.origin_x, bbox.origin_y
                end_point = bbox.origin_x + bbox.width, \
                            bbox.origin_y + bbox.height
                cv2.rectangle(frame, start_point, end_point, 
                              (0, 165, 255), 2)

                # Отображение названия
                category = detection.categories[0]
                category_name = category.category_name
                translation = dictionary.get(category_name)
                if translation != None:
                    category_name = translation
                probability = round(category.score, 2)
                result_text = category_name + ' (' + str(probability) + ')'
                text_location = (MARGIN + bbox.origin_x,
                                 MARGIN + ROW_SIZE + bbox.origin_y)
                cv2.putText(frame, result_text, text_location, 
                            font, 1, (255, 255, 255), 1, cv2.LINE_AA)
    else: # Не в режиме обнаружения объектов
        # Обнаружение лиц в кадре            
        results = face_detector.process(frame)
        if results.detections: # В кадре есть лица
            view_time = datetime.now()
            
            if say_hello:
                os.system('aplay ./audio/привет.wav')
                say_hello = False
            
            # Центрирование камеры на лицах
            track_detections(frame, results.detections)
        else: # В кадре нет лиц
            time_diff = datetime.now() - view_time
            delay = int(time_diff.total_seconds())
            if delay < SEARCH_DELAY:
                cv2.putText(frame, 
                    f'Поиск через {SEARCH_DELAY - delay} секунд', 
                    (10, 90), font, 1, (255, 255, 255), 1, cv2.LINE_AA)          
            else:
                say_hello = True
                cv2.putText(frame, 'Ищу лица', 
                    (10, 90), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                search_face_detector()  

    # Ожидание нажатия кнопки 'Esc' для выхода
    if cv2.waitKey(1) == 27:
      break

    # Отображение кадра
    cv2.imshow('robot', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

cv2.destroyAllWindows() # Закрываем окно с видео
