#!/usr/bin/env python3

import sys
import math
import time
import asyncio
import json

import logging

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *

from quamash import QEventLoop


from logic import Logic
from connect import Connect
import logsetting
logger = logging.getLogger('root')



def app_setup():
    '''
    Init app window setups goes here...
    '''

    app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    logic = Logic()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('logic', logic)
    
    engine.load(QUrl('main_gui.qml'))
    topLevel = engine.rootObjects()[0]

    logic.setRoot(topLevel)
    logic.hello()


    topLevel.show()

    app.aboutToQuit.connect(lambda: loop.close())
    app.exec_()

def main():
    app_setup()


main()
