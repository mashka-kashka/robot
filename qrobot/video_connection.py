from socket import socket

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from PyQt6.QtNetwork import QTcpServer, QHostAddress, QTcpSocket
from wheel.macosx_libfile import swap32

from log_message_type import LogMessageType

class QRobotVideoConnection(QThread):
    log_signal = pyqtSignal(object, object)
    stop_signal = pyqtSignal()
    tcp_server = None
    tcp_client = None

    def __init__(self, logger, host, port):
        super().__init__()
        self.logger = logger
        self.log_signal.connect(self.logger.log)
        self.host = host
        self.port = int(port)

    @pyqtSlot()
    def bind(self):
        try:
            self.tcp_server = QTcpServer()
            self.tcp_server.newConnection.connect(self.on_client_connected)
            self.log_signal.emit(f"Ожидание подключения клиента к {self.host}:{self.port} для передачи видео",
                                 LogMessageType.STATUS)

            self.tcp_server.listen(QHostAddress(self.host), self.port)
        except Exception as e:
            self.log_signal.emit(f"Ошибка {type(e)}: {e}", LogMessageType.ERROR)
            self.stop_signal.emit()

    @pyqtSlot()
    def connect_to_host(self):
        try:
            self.log_signal.emit(f"Попытка подключения к серверу {self.host}:{self.port} для передачи видео",
                                 LogMessageType.STATUS)
            self.tcp_client = QTcpSocket()
            self.tcp_client.disconnected.connect(self.on_client_dissconnected)
            self.tcp_client.connected.connect(self.on_connected_to_host)
            self.tcp_client.connectToHost(QHostAddress(self.host), self.port)
            if not self.tcp_client.waitForConnected(1000):
                self.log_signal.emit(f"Не удалось подключиться к серверу для передачи видео", LogMessageType.WARNING)
                self.stop_signal.emit()
        except Exception as e:
            self.log_signal.emit(f"Ошибка {type(e)}: {e}", LogMessageType.ERROR)
            self.stop_signal.emit()

    def close(self):
        try:
            if self.tcp_server:
                self.log_signal.emit(f"Остановка сервера {self.host}:{self.port} для передачи видео",
                                     LogMessageType.STATUS)
                self.tcp_server.close()
                self.tcp_server = None

            if self.tcp_client:
                self.log_signal.emit(f"Остановка клиента {self.host}:{self.port} для передачи видео",
                                     LogMessageType.STATUS)
                self.tcp_client.close()
                self.tcp_client = None

            self.quit()

        except Exception as e:
           self.log_signal.emit(f"Ошибка {type(e)}: {e}", LogMessageType.ERROR)

    @pyqtSlot()
    def on_client_connected(self):
        while self.tcp_server.hasPendingConnections():
            self.connection = self.tcp_server.nextPendingConnection()
            self.connection.disconnected.connect(self.on_client_dissconnected)

            self.log_signal.emit(f"Подключился клиент {self.connection.peerAddress().toString()} для передачи видео",
                             LogMessageType.STATUS)

    @pyqtSlot()
    def on_connected_to_host(self):
        self.log_signal.emit(f"Успешное подключение к серверу для передачи видео",
                             LogMessageType.STATUS)
    @pyqtSlot()
    def on_client_dissconnected(self):
        self.log_signal.emit(f"Клиент для передачи видео отключился",
                         LogMessageType.WARNING)

       # if self.tcp_client: # Активация кнопки для повторного подключения
       #     self.stop_signal.emit()
