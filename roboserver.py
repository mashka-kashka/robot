#!/usr/bin/python3
import io
import fcntl
import struct
import socket
import threading

from picamera2 import Picamera2, Preview
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from picamera2.encoders import Quality

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = threading.Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class RoboServer:
    def __init__(self):

        self.server_address = None
        self.video_client_address = None
        self.video_socket = None
        self.video_connection = None
        self.video_thread = None
        self.data_client_address = None
        self.data_socket = None
        self.data_connection = None
        self.data_thread = None

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(),
                                0x8915,
                                struct.pack('256s',b'wlan0'[:15])
                                )[20:24])

    def start(self):
        self.server_address = self.get_ip_address()
        self.data_socket = socket.socket()
        self.data_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.data_socket.bind(( self.server_address, 1580))
        self.data_socket.listen(1)
        self.data_thread = threading.Thread(target=self.receive_data)
        self.data_thread.start()

        self.video_socket = socket.socket()
        self.video_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.video_socket.bind(( self.server_address, 1581))
        self.video_socket.listen(1)
        self.video_thread = threading.Thread(target=self.send_video)
        self.video_thread.start()

        print("Cервер запущен")
        print(f"Мой адрес:  { self.server_address}")

            
    def stop(self):
        try:
            self.data_connection.close()
            self.video_connection.close()
        except Exception as e:
            print('\n' + "Подключения отсутствуют")
        exit()

    def send_data(self, data):
        try:
            self.data_connection.send(data.encode('utf-8'))
        except:
            pass

    def receive_data(self):
        try:
            try:
                self.data_connection, self.data_client_address = self.data_socket.accept()
                print(f"Установлено соединение для передачи данных с {self.data_client_address}")
            except Exception as e:
                print(f"Ошибка установки соединения для передачи данных: {e}")
            self.data_socket.close()
            while True:
                try:
                    data = self.data_connection.recv(1024).decode('utf-8')
                except Exception as e:
                    print(e)
                    break
                print(f"Получены данные: {data}")
                break
        except Exception as e:
            print(e)
        self.stop()

    def send_video(self):
        try:
            connection, self.video_client_address = self.video_socket.accept()
            self.video_connection = connection.makefile('wb')
        except:
            pass
        self.server_socket.close()
        print(f"Установлено соединение для передачи видео на адрес {self.video_client_address} ")
        camera = Picamera2()
        camera.configure(camera.create_video_configuration(main={"size": (400, 300)}))
        output = StreamingOutput()
        encoder = JpegEncoder(q=90)
        camera.start_recording(encoder, FileOutput(output), quality=Quality.VERY_HIGH)
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
            try:
                lenFrame = len(output.frame)
                lengthBin = struct.pack('<I', lenFrame)
                self.video_connection.write(lengthBin)
                self.video_connection.write(frame)
            except Exception as e:
                camera.stop_recording()
                camera.close()
                print("Завершение передачи видео ... ")
                break

if __name__ == '__main__':
    server = RoboServer()
    server.start()

