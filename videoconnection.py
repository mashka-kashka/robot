import io
import socket
import struct
import cv2
import numpy as np
from PIL import Image

class VideoConnection:
    def __init__(self):
        self.connection = None
        self.is_connected = False

    def IsValidImage4Bytes(self,buf):
        bValid = True
        if buf[6:10] in (b'JFIF', b'Exif'):
            if not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'):
                bValid = False
        else:
            try:
                Image.open(io.BytesIO(buf)).verify()
            except:
                bValid = False
        return bValid

    def open(self, ip):
        try:
            print("Запуск потока для получения видео")

            #self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           # self.data_socket.connect((ip, 1580))

            #self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.video_socket.connect((ip, 1581))
            #self.video_connection = self.video_socket.makefile('rb')
            #self.is_connected = True
            print("Успешное подключение к роботу")
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            self.is_connected = False
            return

        # while True:
        #     try:
        #         stream_bytes = self.video_connection.read(4)
        #         data_len = struct.unpack('<L', stream_bytes[:4])
        #         jpg = self.connection.read(data_len[0])
        #         if self.IsValidImage4Bytes(jpg):
        #             image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        #             cv2.imwrite('video.jpg', image)
        #             #if self.video_Flag:
        #             #    self.face_detect(image)
        #             #    self.video_Flag = False
        #     except Exception as e:
        #         print(e)
        #         break


    def close(self):
        try:
            self.data_socket.shutdown(socket.SHUT_RDWR)
            self.video_socket.shutdown(socket.SHUT_RDWR)
            self.data_socket.close()
            self.video_socket.close()
        except:
            pass

if __name__ == '__main__':
    pass