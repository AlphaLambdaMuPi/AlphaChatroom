#!/usr/bin/env python3

import sys
import math
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *
import asyncio
from quamash import QEventLoop
import json

@asyncio.coroutine
def zzz():
    i = 0
    while True:
        print(i)
        yield from asyncio.sleep(0.5)
        i += 1

@asyncio.coroutine
def tcp_client_connect():
    r, w = yield from asyncio.open_connection('140.112.18.210', 9007)
    x = { 'abc': 'alphabetagamma',
            'nick': 'zzzzzzz'}
    while True:
        print(123)
        mesg = json.dumps(x) + '\n'
        w.write(mesg.encode())

        data = yield from r.readline()
        print('456', data.decode())

class Logic(QObject):
    def __init__(self):
        super().__init__()
        self.a = 100

    @pyqtSlot()
    def hello(self):
        print('Hello!')
        loop = asyncio.get_event_loop()


        print('F1: ', loop.is_running())
        try:
            loop.create_task(tcp_client_connect())
        except Exception as e:
            print(e)
            print('F2: ', loop.is_running())



def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    engine = QQmlApplicationEngine()
    engine.load(QUrl('main_gui.qml'))
    topLevel = engine.rootObjects()[0]

    logic = Logic()
    engine.rootContext().setContextProperty('logic', logic)
    topLevel.show()

    x = { 'abc': 'alphabetagamma',
         'nick': 'zzzzzzz'}

    @asyncio.coroutine
    def tcp_client_connect():
        r, w = yield from asyncio.open_connection('140.112.18.210', 9007)
        while True:
            mesg = json.dumps(x) + '\n'
            print(mesg)
            w.write(mesg.encode())

            data = yield from r.readline()
            print(data.decode())



    #appView = QQuickView()
    #appView.setSource(QUrl('main_gui.qml'))
    #appView.show()
    #main = MainHandle()
    #appView.rootContext().setContextProperty('main', main)



    loop.run_until_complete(app.exec_())

if __name__ == '__main__':
    main()
