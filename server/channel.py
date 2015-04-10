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

    def get_users(self):
        return list(map(lambda user: user.get_info(), self._users.values()))

    def add_user(self, user):
        if user not in self._users:
            self._users[user.nick] = user
            self.broadcast_call("user_join_channel", user.get_info(),
                                self.name)
            # asyncio.call_soon(self.broadcast_call, "user_join_channel",
                              # user.get_info());
            return True
        else:
            return False

    def remove_user(self, user):
        try:
            del self._users[user.nick]
            self.broadcast_call("user_leave_channel", user.nick,
                                self.name)
            # asyncio.call_soon(self.broadcast_call, "user_leave_channel",
                              # user.nick);
            return True
        except KeyError:
            return False
    
    def broadcast_msg(self, msg, fr):
        for user in self._users.values():
            user.send_msg(msg, fr, self.name)

    def broadcast_call(self, funcname, *args):
        for user in self._users.values():
            user.send_call(funcname, *args)

