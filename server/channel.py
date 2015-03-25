#! /usr/bin/env python

import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Channel:
    def __init__(self, server, name):
        self._server = server
        self._name = name
        self._users = {}

    def _broadcast(self, data):
        for user in self._users.values():
            user._conn.send(data)

    def add_user(self, user):
        self._users[user.get_nick()] = user

    def remove_user(self, user):
        try:
            del self._users[user.nick]
            return True
        except KeyError:
            return False
    
    def send(self, msg, fr):
        data = {"type": "MSG", "msg": msg, "from": fr, "channel": self.name}
        self._broadcast(data)


