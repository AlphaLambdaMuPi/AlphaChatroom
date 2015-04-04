import logging
import asyncio
import json

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *
from quamash import QEventLoop

from settings import *

from connect import Connect

from logsetting import *
logger = logging.getLogger('root')


class Medium(QObject):

    avatarChanged = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.connect = Connect(self)
        self.state = 0
        self.channels = []
        pass


    def setEngine(self, engine):
        self.engine = engine
        self.root = engine.rootObjects()[0]


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



    def send_msg(self, channel_name, mesg):
        logger.info(self.channels)
        if channel_name not in self.channels:
            logger.warning( 'You are not in the channel.' )
            return

        self.connect.putq({
            'type': 'CALL',
            'func': 'route_message',
            'params': ['CHANNEL', channel_name, mesg],
        })

    def receive_msg(self, data):

        logger.info("receive_msg gets :" + str(data))
        if data['type'] == 'CALL' and data['params'][1] != 'SYSTEM':
            logger.info("Get call:" + str(data))
            self.root.receive_msg({
                'type': 'text',
                'sender': data['params'][1],
                'mesg': data['params'][0]
            })

    def receive(self, data):
        if data['type'] == 'CALL':
            func = 'S' + data['func']
            try:
                func = getattr(self, func)
            except AttributeError:
                logger.error('The function %s is not found', func)
                return

            if not callable(func):
                logger.error('The function %s is not callable', func)
                return

            try:
                res = func(*data['params'])
            except Exception as e:
                logger.error('Call function %s Error: %s', func, e)

    def hello(self):
        self.connect_server()
                
    def Sget_message(self, msg, fr, channel):
        self.root.receive_msg(channel, {
            'type': 'text',
            'sender': fr,
            'mesg': msg,
        })

    def Ssuccess_join(self, channel):
        self.channels.append(channel)
        self.root.channelAdd(channel)




    @pyqtSlot(str)
    def Qlogin(self, nick):
        self._login(nick)
        self.root.onLoggedIn()

    @pyqtSlot(str)
    def Qjoin(self, channel):
        logger.info('qml request join')
        self.join_channel(channel)

    @pyqtSlot(str, str)
    def Qsend(self, ch, s):
        logger.debug("Qsend channel = %s : %s", ch, s)
        self.send_msg(ch, s)

    @pyqtSlot(str)
    def Qavatar(self, url):
        self.engine.imageProvider('avatarImage').url = url
        self.avatarChanged.emit()
