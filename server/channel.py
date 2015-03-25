#! /usr/bin/env python

import asyncio
import logging

logger = logging.getLogger()

class Channel:
    def __init__(self, server, name):
        self.name = name

        self._server = server
        self._users = {}

    def _broadcast(self, data):
        for user in self._users.values():
            user._conn.send(data)

    def add_user(self, user):
        if user not in self._users:
            self._users[user.nick] = user
            return True
        else:
            return False

    def remove_user(self, user):
        try:
            del self._users[user.nick]
            return True
        except KeyError:
            return False
    
    def send(self, msg, fr):
        data = {"type": "MSG", "msg": msg, "from": fr, "channel": self.name}
        self._broadcast(data)


