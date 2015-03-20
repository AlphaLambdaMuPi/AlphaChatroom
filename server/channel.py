#! /usr/bin/env python

import asyncio
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Channel:
    def __init__(self, server, name):
        self.server = server
        self.name = name
        self.users = {}

    def _broadcast(self, data):
        for user in self.users.values():
            user._send(data)

    def add_user(self, user):
        self.users[user.nick] = user

    def remove_user(self, user):
        try:
            del self.users[user.nick]
            return True
        except KeyError:
            return False
    
    def send(self, msg, fr):
        data = {"type": "MSG", "msg": msg, "from": fr, "channel": self.name}
        self._broadcast(data)


