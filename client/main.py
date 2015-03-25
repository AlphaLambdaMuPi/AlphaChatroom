#!/usr/bin/env python3

import sys
import math
import time
import asyncio
import json

import logging
LOG_FILE_NAME = 'client.log'
logging.basicConfig(filename=LOG_FILE_NAME,
                    filemode='a',
                    format='[%(asctime)s.%(msecs)d] %(name)s - %(levelname)s : %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *

from quamash import QEventLoop

@asyncio.coroutine
def test_el():
    i = 0
    while True:
        print(i)
        yield from asyncio.sleep(0.5)
        i += 1

        if i > 10:
            return

@asyncio.coroutine
def tcp_client_connect():

    try:
        reader, writer = yield from asyncio.open_connection('140.112.18.210', 9007)
    except Exception as e:
        logger.error(e)
        return

    while True:
        mesg = json.dumps(x) + '\n'
        writer.write(mesg.encode())
        logger.debug(1, 2)

        data = yield from reader.readline()

class Logic(QObject):
    def __init__(self):
        super().__init__()
        self.a = 100

    @pyqtSlot()
    def hello(self):
        loop = asyncio.get_event_loop()

        logger.debug('Start Connect')
        try:
            loop.create_task(tcp_client_connect())
        except Exception as e:
            logger.error(e)


def init_logging():
    formatter = logging.Formatter(fmt = '[%(asctime)s.%(msecs)d] %(name)s - %(levelname)s : %(message)s'
                                  ,datefmt = '%H:%M:%S')
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.debug('Logging Config Done')

def app_setup():
    '''
    Init app window setups goes here...
    '''

    app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    engine = QQmlApplicationEngine()
    engine.load(QUrl('main_gui.qml'))
    topLevel = engine.rootObjects()[0]

    logic = Logic()
    engine.rootContext().setContextProperty('logic', logic)

    topLevel.show()

    app.aboutToQuit.connect(lambda: loop.close())

    app.exec_()

def main():

    init_logging()

    app_setup()


main()
