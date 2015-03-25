#! /usr/bin/env python

import asyncio
import logging

from connection import JsonConnection
from user import User
from channel import Channel

logger = logging.getLogger()

class ChatServer:
    def __init__(self):
        self._channels = {}
        self._users = {}
        self._name = "SYSTEM"
        self._hellostr = "Hi {}, this is your current nickname."

    @asyncio.coroutine
    def __call__(self, sr, sw):
        conn = JsonConnection(sr, sw)
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

    def get_channel(self, chname, create=True):
        if chname not in self._channels:
            if create:
                self._channels[chname] = Channel(self, chname)
            else:
                return None
        return self._channels[chname]

# global object       
chat_server = ChatServer() 

