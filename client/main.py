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
                    format='[%(asctime)s.%(msecs)d] %(module)s - %(levelname)s : %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger('root')

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *

from quamash import QEventLoop

#from logic import Logic
from connect import Connect
from logsetting import *

class Logic(QObject):
    def __init__(self):
        super().__init__()
        self.connect = Connect()

    @pyqtSignature("")
    def hello(self):
        loop = asyncio.get_event_loop()
        logger.debug('Start Connect')
        return
        #try:
            #self.connect.start()
        #except Exception as e:
            #logger.error(e)


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

    init_logging(logger)

    app_setup()


main()
