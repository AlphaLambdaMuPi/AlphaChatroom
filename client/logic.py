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
from medium import Medium

import logsetting
logger = logging.getLogger('root')

class Logic(QObject):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.medium = Medium(self)

    @pyqtSlot()
    def hello(self):
        self.medium.connect_server()
        self.medium.login('alpha')
        self.medium.join_channel('beta') 
        

    @pyqtSlot(str)
    def send(self, s):
        logger.debug(s)
        self.medium.send_msg('beta', s)
    
    def receive_msg(self, fr, s):
        self.root.pushList({
            'sender': fr,
            'dataText': s
        })


