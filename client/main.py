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


#from logic import Logic
from medium import Medium
from connect import Connect
from image import ImageProvider, EmoticonProvider
#import resource

import logsetting
logger = logging.getLogger('root')

def app_setup():
    '''
    Init app window setups goes here...
    '''

    app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    #logic = Logic()
    medium = Medium()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('medium', medium)
    imgp = ImageProvider()
    emoticonProvider = EmoticonProvider()
    engine.addImageProvider('avatarImage', imgp)
    engine.addImageProvider('emoticon', emoticonProvider)
    
    engine.load(QUrl('qml/init.qml'))
    topLevel = engine.rootObjects()[0]

    medium.setEngine(engine)
    medium.hello()

    topLevel.show()

    def close_func():
        medium.goodbye()
        loop.close()
    app.aboutToQuit.connect(close_func)
    app.exec_()

def main():
    app_setup()


if __name__ == '__main__':
    main()
