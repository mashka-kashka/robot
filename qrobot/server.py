from PyQt6.QtCore import QObject, pyqtSignal
from log_message_type import LogMessageType
import socket
import toml


class QRobotServer(QObject):
    log_signal = pyqtSignal(object, object)
    stop_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = False

    def start(self):
        if self.running:
            return
        self.running = True

        with open('config.toml', 'r') as f:
            self.config = toml.load(f)
            _video_port = self.config["network"]["video_port"]
            _data_port = self.config["network"]["data_port"]
            _host = self.config["network"]["host"]

            try:
                self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.video_socket.bind((_host, int(_video_port)))
                self.video_socket.listen(1)
                self.log_signal.emit(f"Ожидание подключения клиента к {_host}:{_video_port} для передачи видео", LogMessageType.STATUS)

                self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.data_socket.bind((_host, int(_data_port)))
                self.data_socket.listen(1)
                self.log_signal.emit(f"Ожидание подключения клиента к {_host}:{_data_port} для передачи данных", LogMessageType.STATUS)
            except Exception as e:
                self.log_signal.emit(f"Ошибка {type(e)}: {e}", LogMessageType.ERROR)
                self.stop_signal.emit()

    def stop(self):
        if not self.running:
            return
        self.running = False
        try:
            self.video_connection.close()
            self.data_connection.close()
        except Exception as e:
            pass

    def reset(self):
        self.stop()
        self.start()
