#!/usr/bin/env python
# Подключаем необходимые библиотеки
import cv2, sys, time, os
from buildhat import Motor

# Параметры кадра
FRAME_WIDTH = 320
FRAME_HEIGHT = 200

# Ограничения горизонтального перемещения
INIT_HOR_POSITION = 0
MIN_HOR_ANGLE = -60
MAX_HOR_ANGLE = 60

# Ограничения вертикального перемещения
INIT_VERT_POSITION = 10
MIN_VERT_ANGLE = -10
MAX_VERT_ANGLE = 80

# Подключаем и настраиваем видеокамеру
os.system('sudo modprobe bcm2835-v4l2')
os.system('v4l2-ctl -p 5')

# Запуск захвата видео
vid_capture = cv2.VideoCapture(0)
if (vid_capture.isOpened() == False):
    print("Ошибка подключения камеры")
    exit()
  
vid_capture.set(cv2.CAP_PROP_FRAME_WIDTH,  FRAME_WIDTH);
vid_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT);
time.sleep(3)

# Подключение модуля обнаружения лиц
CLS_PATH = '/usr/share/opencv4/lbpcascades/lbpcascade_frontalface.xml'
face_classifier = cv2.CascadeClassifier(CLS_PATH)

# Подключение моторов
h_motor = Motor('A')
h_motor.run_to_position(INIT_HOR_POSITION)

v_motor = Motor('B')
v_motor.run_to_position(INIT_VERT_POSITION)

# Основной цикл работы
search_direction = 1
while True:
    ret, frame = vid_capture.read()
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
     
    # Ожидание нажатия кнопки 'q' для выхода
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
    # Лиц не обнаружено
    if len(faces)==0:
        h_motor.stop()
        v_motor.stop()
        time.sleep(1)
        continue
        
    # Отображение рамок вокруг обнаруженных лиц
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Координаты центра лица
        cx = x + (w / 2)
        cy = y + (h / 2)        

        # Определяем текущую озицию
        h_pos = h_motor.get_aposition()

        print(f"Позиция камеры: {h_pos} Центр лица: ({cx}, {cy})")
        
        hf =  float(cx) / FRAME_WIDTH
        h_motor.run_to_position(MIN_HOR_ANGLE * (1.0 - hf) + 
        MAX_HOR_ANGLE * hf)
        
        vf =  float(cy) / FRAME_HEIGHT
        v_motor.run_to_position(MIN_VERT_ANGLE * (1.0 - vf) + 
        MAX_VERT_ANGLE * vf)
        
        # Обрабатываем только первое лицо
        break
    
    # Отображение кадра
    cv2.imshow('Робот', frame)

# Отключение моторов и камеры перед выходом
h_motor.stop()
v_motor.stop()
vid_capture.release()
cv2.destroyAllWindows()
