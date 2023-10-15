#!/usr/bin/env python
# Подключаем необходимые библиотеки
import cv2, sys, time, os
from buildhat import Motor
from gpiozero import CPUTemperature

# Параметры кадра
FRAME_WIDTH = 320
FRAME_HEIGHT = 200

# Ограничения горизонтального перемещения
INIT_HOR_POSITION = 0
MIN_HOR_ANGLE = -45
MAX_HOR_ANGLE = 45

# Ограничения вертикального перемещения
INIT_VERT_POSITION = 30
MIN_VERT_ANGLE = 10
MAX_VERT_ANGLE = 60

cpu = CPUTemperature()
font = cv2.FONT_HERSHEY_COMPLEX

# Подключаем и настраиваем видеокамеру
os.system('sudo modprobe bcm2835-v4l2')
os.system('v4l2-ctl -p 10')

# Запуск захвата видео
vid_capture = cv2.VideoCapture(0)
if (vid_capture.isOpened() == False):
    print("Ошибка подключения камеры")
    exit()
  
vid_capture.set(cv2.CAP_PROP_FRAME_WIDTH,  FRAME_WIDTH);
vid_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT);
time.sleep(1)

# Подключение модуля обнаружения лиц
CLS_PATH = '/usr/share/opencv4/lbpcascades/lbpcascade_frontalface.xml'
face_classifier = cv2.CascadeClassifier(CLS_PATH)

# Подключение моторов
h_motor = Motor('A')
h_motor.run_to_position(INIT_HOR_POSITION)
h_motor.set_default_speed(1)

v_motor = Motor('B')
v_motor.run_to_position(INIT_VERT_POSITION)
 
# Основной цикл работы
while True:
    ret, frame = vid_capture.read(1)
    if ret == False:
        print("Ошибка получения кадра")
        continue

    # Поворот кадра
    frame = cv2.flip(frame, -1)

    # Преобразование кадра для передачи модулю обнаружения лиц
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray = cv2.equalizeHist(gray)

    # Обнаружение лиц
    faces = face_classifier.detectMultiScale(frame, 1.1, 3, 0, (10, 10))

    # Определяем текущую озицию
    h_pos = h_motor.get_aposition()
    v_pos = v_motor.get_aposition()
    
    text_color =  (0, 200, 0)
    if (cpu.temperature > 60):
        text_color =  (0, 0, 200)
        
    cv2.putText(frame, f'Температура процессора: {int(cpu.temperature)}', (10, 20), font, 0.5, text_color, 1, cv2.LINE_AA)
    
    if len(faces)==0: 
        cv2.putText(frame, 'Лица не найдены', (10, 40), font, 0.5, text_color, 1, cv2.LINE_AA)
        v_motor.stop()
        h_motor.stop()
    
    # Отображение рамок вокруг обнаруженных лиц
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Координаты центра лица
        cx = x + (w / 2)
        cy = y + (h / 2)        

        print(f"Центр лица: ({cx}, {cy})")
        
        # Определяем текущую озицию
        h_pos = h_motor.get_position()
        v_pos = v_motor.get_position()
        
        hf = float(cx) / FRAME_WIDTH
        new_hpos = MIN_HOR_ANGLE * (1 - hf) + MAX_HOR_ANGLE * hf
        h_motor.run_to_position(new_hpos, speed=1)

        vf = float(cy) / FRAME_HEIGHT
        new_vpos = MIN_VERT_ANGLE * (1 - vf) + MAX_VERT_ANGLE * vf
        v_motor.run_to_position(new_vpos, speed=1)
                
        
        # Обрабатываем только первое лицо
        break
    
    # Отображение кадра
    cv2.imshow('Робот', frame)
    
    # Ожидание нажатия кнопки 'q' для выхода
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Отключение моторов и камеры перед выходом
h_motor.stop()
v_motor.stop()
vid_capture.release()
cv2.destroyAllWindows()
