import logging
import asyncio
import json

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *
from quamash import QEventLoop

from settings import *

from connect import Connect

from logsetting import *
logger = logging.getLogger('root')


class Medium(QObject):

    def __init__(self):
        super().__init__()
        self.connect = Connect(self)
        self.state = 0
        self.channels = []
        pass

    def setRoot(self, root):
        self.root = root


    def connect_server(self):
        try:
            self.connect.start()
        except Exception as e:
            logging.error('Cant connect server: %s', str(e))
            self.state = 0
            return

        self.state = 1

    def _login(self, nick):
        try:
            self.connect.putq( {'nick': nick} )
        except Exception as e:
            logging.error('Cant login server: %s', str(e))
            self.state = 0
            return

        self.state = 2
        self.channels = []

    def join_channel(self, channel_name):

        try:
            self.connect.putq({
                'type': 'CALL',
                'func': 'join',
                'params': [channel_name],
            })
        except Exception as e:
            logging.error('Cant join server: %s', str(e))

        logger.info('Success joined channel: %s', channel_name)
        self.success_join(channel_name)


    def success_join(self, channel):
        self.channels.append(channel)
        self.root.channelAdd(channel)

    def send_msg(self, channel_name, mesg):
        if channel_name not in self.channels:
            logger.warning( 'You are not in the channel.' )
            return

        self.connect.putq({
            'type': 'CALL',
            'func': 'route_message',
            'params': ['CHANNEL', channel_name, mesg],
        })

    def receive_msg(self, data):

        logger.info(data)
        if data['type'] == 'CALL' and data['params'][1] != 'SYSTEM':
            logger.info(data)
            self.root.receive_msg({
                'type': 'text',
                'sender': data['params'][1],
                'mesg': data['params'][0]
            })


    @pyqtSlot()
    def hello(self):
        self.connect_server()

    @pyqtSlot(str)
    def login(self, nick):
        self._login(nick)
        self.join_channel('beta') 
        self.root.onLoggedIn()

    @pyqtSlot(str)
    def send(self, s):
        logger.debug(s)
        self.send_msg('beta', s)

