import logging
import asyncio
import json

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *
from quamash import QEventLoop

from settings import *
from logsetting import *
from connect import Connect

import logsetting
logger = logging.getLogger('root')

class Logic(QObject):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.connect = Connect(self)

    @pyqtSlot()
    def hello(self):
        loop = asyncio.get_event_loop()
        logger.debug('Start Connect')
        #try:
        self.connect.start()
        #except Exception as e:
        #logger.error(e)

    @pyqtSlot(str)
    def send(self, s):
        logger.debug(s)
        self.connect.send_text(s)
    
    def receive(self, s):
        try:
            print(s, self.root.pushList)
        except Exception as e:
            print(e)
        self.root.pushList(s)
        #root

