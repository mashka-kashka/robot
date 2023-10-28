#!/usr/bin/python3

from servo import *
from picamera2 import Picamera2
from gpiozero import CPUTemperature
from datetime import datetime
import mediapipe
import cv2
import os

# Параметры кадра
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Ограничения горизонтального перемещения
INIT_HOR_POSITION = 0
MIN_HOR_ANGLE = 10
MAX_HOR_ANGLE = 130
HOR_STEP = 2
HOR_DELTA = 10 * HOR_STEP / 180 * 3.141 * FRAME_WIDTH

# Ограничения вертикального перемещения
INIT_VERT_POSITION = 30
MIN_VERT_ANGLE = 80
MAX_VERT_ANGLE = 150
VERT_STEP = 2 
VERT_DELTA = 10 * VERT_STEP / 180 * 3.141 * FRAME_HEIGHT

pwm = Servo()
cpu = CPUTemperature()
font = cv2.FONT_HERSHEY_COMPLEX
face_detector = cv2.CascadeClassifier("/home/pi/.local/lib/python3.9/site-packages/cv2/data/haarcascade_frontalface_default.xml")

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'BGR888', "size": (FRAME_WIDTH, FRAME_HEIGHT)}))
picam2.start()

# Модуль распознавания рук
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
cv2.startWindowThread()

hor_position = 70
vert_position = 90
pwm.setServoPwm('0', hor_position)
pwm.setServoPwm('1', vert_position)

SEARCH_DELAY = 5
hor_search_step = HOR_STEP
vert_search_step = VERT_STEP
view_time = datetime.now()
say_hello = True

# Отображение температуры процессора
def print_cpu_temperature():
    # Настраиваем цвет в зависимости от температуры процессора
    text_color =  (0, 200, 0)
    if (cpu.temperature > 60):
        text_color = (0, 200, 200)
    if (cpu.temperature > 80):
        text_color = (0, 0, 200)
        
    cv2.putText(frame, f'Температура процессора: {int(cpu.temperature)}', 
        (10, 20), font, 0.5, text_color, 1, cv2.LINE_AA)

# Поиск лиц
def search_faces(): 
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
def track_faces(faces):
    global hor_position
    global vert_position
    
    left = FRAME_WIDTH
    right = 0
    top = 0
    bottom = FRAME_HEIGHT
    for (x, y, w, h) in faces:
        # Отображение рамок
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0))
    
        if x < left:
            left = x
        if x + w > right:
            right = x + w
        if y < bottom:
            bottom = y
        if y + h > top:
            top = y + h

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

with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:
    while True:
        frame = picam2.capture_array()
               
        # Отображение температуры процессора
        print_cpu_temperature()
        
        # Обнаружение рук в кадре
        results = hands.process(frame)
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                view_time = datetime.now()
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)

        # Обнаружение лиц в кадре
        faces = face_detector.detectMultiScale(frame, 1.1, 5)
        if len(faces)==0: # Лица не обнаружены
            time_diff = datetime.now() - view_time
            delay = int(time_diff.total_seconds())
            if delay < SEARCH_DELAY:
                cv2.putText(frame, 
                    f'Лица не найдены {delay} секунд', 
                    (10, 40), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)          
            else:
                say_hello = True
                cv2.putText(frame, 'Ищу лица', 
                    (10, 40), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                search_faces()
        else: # Лица обнаружены
            view_time = datetime.now()
            
            if say_hello:
                os.system('aplay ./audio/привет.wav')
                say_hello = False
            
            # Ценрирование камеры на лицах
            track_faces(faces)

        # Ожидание нажатия кнопки 'Esc' для выхода
        if cv2.waitKey(1) == 27:
          break

        # Отображение кадра
        cv2.imshow('robot', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

cv2.destroyAllWindows()