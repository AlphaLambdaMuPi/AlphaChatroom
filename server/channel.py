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
            user.send(data)

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
    
    def broadcast_msg(self, msg, fr):
        for user in self._users.values():
            user.send_msg(msg, fr, self.name)

