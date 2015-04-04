#! /usr/bin/env python

import asyncio
import logging

from fileserver import file_server
from connection import JsonConnection
from user import User
from channel import Channel

logger = logging.getLogger()

class ChatServer:
    def __init__(self, loop=None):
        self._loop = loop
        if not self._loop:
            self._loop = asyncio.get_event_loop()
        self._channels = {}
        self._users = {}
        self._name = "SYSTEM"
        self._hellostr = "Hi {}, this is your current nickname."

    @asyncio.coroutine
    def __call__(self, sr, sw):
        conn = JsonConnection(sr, sw)
        yield from self.add_user(conn)
    
    @asyncio.coroutine
    def add_user(self, conn):
        data = yield from conn.recv()
        if not isinstance(data, dict):
            return

        if "nick" in data and data['nick'] != self._name:
            nick = self.gen_nick(data['nick'])
        self._users[nick] = User(self, file_server, nick, conn)
        self._users[nick].send_call('init_conn', self._name, nick)
        self._users[nick].send_msg(
            self._hellostr.format(nick),
            self._name
        )
        yield from self._users[nick].run()

    def del_user(self, user):
        try:
            del self._users[user.nick]
            logger.info("{} disconnected from server".format(user.nick))
        except KeyError:
            logger.warning("{} is not found in"
                           " the user lsit.".format(user.nick))

    def gen_nick(self, nick):
        while nick in self._users:
            nick = nick + '_'
        return nick

    def change_nick(self, user, new_nick):
        if new_nick in self._users:
            return False

        self._users[new_nick] = user
        try:
            del self._users[user.nick]
        except KeyError:
            logger.warning("{} is not found in"
                           " the user lsit.".format(user.nick))
        return True

    def get_channel(self, chname, *, create=False):
        if chname not in self._channels:
            if create:
                self._channels[chname] = Channel(self, chname)
            else:
                return None
        return self._channels[chname]

    def route_msg(self, target_type, target, msg, user):
        if target_type == "CHANNEL":
            ch = self.get_channel(target)
            if ch:
                ch.broadcast_msg(msg, user.nick)
            else:
                user.send_error("channel doesn't exist.")
        elif target_type == "USER":
            if target in self._users:
                self._users[target].send_msg(msg, user.nick)
            else:
                user.send_error("{} is not online.")

    @asyncio.coroutine
    def stop(self):
        for user in self._users.values():
            yield from user._conn.close()

# global object       
chat_server = ChatServer() 

