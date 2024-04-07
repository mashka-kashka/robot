#!/usr/bin/python3

import time
import keyboard
#from getch import getch

class RoboServer:
    def __init__(self):
        self.is_connected = False

    def start(self):
        print("Сервер запущен")
        while True:
            if keyboard.is_pressed("esc"):
                self.stop()

    def stop(self):
        print("Сервер остановлен")
        exit()

if __name__ == '__main__':
    server = RoboServer()
    server.start()

