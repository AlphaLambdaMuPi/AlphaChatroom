import logging
import asyncio
import json


from settings import *

from logsetting import *
logger = logging.getLogger('root')

from connect import Connect

class Medium:

    def __init__(self, logic):
        self.connect = Connect(self)
        self.state = 0
        self.channels = set()
        self.logic = logic
        pass

    def connect_server(self):
        try:
            self.connect.start()
        except Exception as e:
            logging.error('Cant connect server: %s', str(e))
            self.state = 0
            return

        self.state = 1

    def login(self, nick):
        try:
            self.connect.putq( {'nick': nick} )
        except Exception as e:
            logging.error('Cant login server: %s', str(e))
            self.state = 0
            return

        self.state = 2
        self.channels = set()

    def join_channel(self, channel_name):

        try:
            self.connect.putq({
                'type': 'CALL',
                'func': 'join',
                'params': [channel_name],
            })
        except Exception as e:
            logging.error('Cant join server: %s', str(e))
        print(channel_name)
        self.success_join(channel_name)


    def success_join(self, channel):
        self.channels.add(channel)
        print(channel, self.channels)

    def send_msg(self, channel_name, mesg):
        if channel_name not in self.channels:
            logger.warning( 'You are not in the channel.' )
            return

        self.connect.putq({
            'type': 'CALL',
            'func': 'route_message',
            'params': ['CHANNEL', channel_name, mesg],
        })

    def receive(self, data):

        if data['type'] == 'MSG':
            self.logic.receive_msg(data['from'], data['msg'])


