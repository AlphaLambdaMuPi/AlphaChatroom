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
    def __init__(self):
        super().__init__()
        self.medium = Medium(self)

    def setRoot(self, root):
        self.root = root

    @pyqtSlot()
    def hello(self):
        self.medium.connect_server()
        
    @pyqtSlot(str)
    def login(self, nick):
        self.medium.login('alpha')
        self.medium.join_channel('beta') 
        self.root.onLoggedIn()

    @pyqtSlot(str)
    def send(self, s):
        logger.debug(s)
        self.medium.send_msg('beta', s)
    
    def receive_msg(self, fr, s):
        self.root.receive_msg({
            'type': 'text',
            'sender': fr,
            'mesg': s
        })

    def join_channel(self, s):
        self.root.channelAdd(s)



