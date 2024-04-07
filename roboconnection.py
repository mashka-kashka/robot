import socket

class RoboConnection:
    def __init__(self):
        self.is_connected = False

    def start(self, ip):
        try:
            self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.data_socket.connect((ip, 1580))

            self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.video_socket.connect((ip, 1581))
            self.video_connection = self.video_socket.makefile('rb')
            self.is_connected = True
            print("Успешное подключение к роботу")
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            self.is_connected = False
            pass

    def stop(self):
        try:
            self.data_socket.shutdown(socket.SHUT_RDWR)
            self.video_socket.shutdown(socket.SHUT_RDWR)
            self.data_socket.close()
            self.video_socket.close()
        except:
            pass

if __name__ == '__main__':
    pass