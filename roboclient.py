import os
import sys
import configparser
import threading
from PyQt6 import QtGui
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow
from robogui import Ui_MainWindow
from robolog import RoboLog
import robothread
from PIL import Image
from videoconnection import VideoConnection


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.server_ip = '127.0.0.1'
        self.video_thread = None
        self.video_connection = VideoConnection()

        self.setupUi(self)

        # Перенаправление вывода в окно протокола работы
        sys.stdout = RoboLog(self.log_widget, sys.stdout)
        sys.stderr = RoboLog(self.log_widget, sys.stderr, QtGui.QColor(255, 0, 0))

        # Загрузка конфигурационного файла
        self.read_config()

        self.ip_address.setText(self.server_ip)

        self.tabWidget.setTabIcon(0, QtGui.QIcon(r"img\gear.png"))
        self.tabWidget.setTabIcon(1, QtGui.QIcon(r"img\hands.png"))

        self.actionConnect.setIcon(QtGui.QIcon(r"img\connect.png"))
        self.actionConnect.triggered.connect(self.on_connect)

        self.actionExit.setIcon(QtGui.QIcon(r"img\exit.png"))
        self.actionExit.triggered.connect(self.on_exit)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer)


    def read_config(self):
        try:
            config = configparser.ConfigParser()
            config_file = 'robot.ini'
            print(f'Загрузка конфигурационного файла {config_file}')
            config.read(config_file)

            print(f'Секция [net]')
            self.server_ip = config.get('net', 'server')
            print(f'    server: {self.server_ip}')
        except Exception as e:
            print(e)

    def on_exit(self):
        self.write_config()
        self.timer.stop()
        try:
            robothread.stop(self.video_thread)
        except:
            pass
        self.video_connection.stop()

        try:
            os.remove("video.jpg")
        except:
            pass

        self.close()

    def write_config(self):
        config = configparser.RawConfigParser()

        config.add_section('net')
        config.set('net', 'server',  self.ip_address.text())

        with open('robot.ini', 'w') as configfile:
            config.write(configfile)

    def on_connect(self):
        if  self.actionConnect.isChecked():
            self.actionConnect.setText("Отключиться")
            print(f'Подключение к серверу {self.server_ip}')
            self.server_ip = self.ip_address.text()
            try:
                self.video_thread = threading.Thread(target=self.video_connection.open, args=(self.server_ip, ))
                self.video_thread.start()
            except Exception as e:
                print(e)

            self.timer.start(30) # таймер обновления видео
        else:
            self.actionConnect.setText("Подключиться")
            print(f'Отключение от сервера')
            #self.actionConnect.toggle()
            self.timer.stop()
            #try:
                #robothread.stop(self.video_thread)
            #except:
            #    pass
            #self.video_connection.stop()

    def is_valid_jpg(self, jpg_file):
        try:
            bValid = True
            if jpg_file.split('.')[-1].lower() == 'jpg':
                with open(jpg_file, 'rb') as f:
                    buf = f.read()
                    if not buf.startswith(b'\xff\xd8'):
                        bValid = False
                    elif buf[6:10] in (b'JFIF', b'Exif'):
                        if not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'):
                            bValid = False
                    else:
                        try:
                            Image.open(f).verify()
                        except:
                            bValid = False
            else:
                return bValid
        except:
            pass
        return bValid
    def on_timer(self):
        try:
            if self.is_valid_jpg('video.jpg'):
                self.video.setPixmap(QPixmap('video.jpg'))
                #if self.Btn_Tracking_Faces.text() == "Tracing-Off":
                #    self.find_Face(self.TCP.face_x, self.TCP.face_y)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    app.exec()
