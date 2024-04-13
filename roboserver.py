#!/usr/bin/python3

import time

class RoboServer:
    def __init__(self):
        self.is_connected = False

    def start(self):
        print("Сервер запущен")
        while True:
            print('.')
            time.sleep(1)
            
    def stop(self):
        print("Сервер остановлен")
        exit()

if __name__ == '__main__':
    server = RoboServer()
    server.start()

