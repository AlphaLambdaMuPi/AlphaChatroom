#! /usr/bin/env python

import asyncio
import logging

from connection import Connection
from user import User
from channel import Channel

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ChatServer:
    def __init__(self):
        self._channels = {}
        self._users = {}
        self._name = "SYSTEM"
        self._hellostr = "Hi {}, this is your current nickname."

    @asyncio.coroutine
    def __call__(self, sr, sw):
        conn = Connection(sr, sw)
        data = yield from conn.recv()
        
        if not data:
            return

        if "nick" in data and data['nick'] != self._name:
            nick = self.gen_nick(data['nick'])
            self._users[nick] = User(self, nick, conn)
            self._users[nick].send_call('init_conn', self._name, nick)
            self._users[nick].send(
                self._hellostr.format(nick),
                self._name
            )
            res = yield from self._users[nick].run()
            if res == False:
                del self._users[nick]

    def gen_nick(self, nick):
        while nick in self._users:
            nick = nick + '_'
        return nick

    def get_channel(self, chname):
        if chname not in self._channels:
            self._channels[chname] = Channel(self, chname)
        return self._channels[chname]

# global object       
chat_server = ChatServer() 

