#! /usr/bin/env python

import asyncio
import logging

logger = logging.getLogger()

class User:
    def __init__(self, server, nick, conn):
        self.nick = nick

        self._server = server
        self._conn = conn

        self._funcs = {}
        self._funcs['set_nick'] = self.set_nick
        self._funcs['join'] = self.join
        self._funcs['leave'] = self.leave
        self._funcs['route_message'] = self.route_message

    def send_error(self, errmsg):
        data = {"type": "ERROR", "msg": errmsg}
        self._conn.send(data)
    
    def send_return(self, rid, ret):
        data = {"type": "RETURN", "retid": rid, "ret": ret}
        self._conn.send(data)

    def send_call(self, funcname, *args):
        data = {"type": "CALL", "func": funcname, "params": args}
        self._conn.send(data)
    
    def send(self, msg, fr, ch=None):
        data = {"type": "MSG", "msg": msg, "from": fr, "channel": ch}
        self._conn.send(data)

    @asyncio.coroutine
    def run(self):
        while self._conn.alive():
            data = yield from self._conn.recv()
            if not data:
                continue
            if "type" in data and data["type"] == "CALL":
                try:
                    ret = self._funcs[data["func"]](*data["params"])
                    if "retid" in data:
                        self.send_return(data["retid"], ret)
                except KeyError:
                    self.send_error("invalid operation")
            else:
                self.send_error("invalid operation")
        logger.info("{} disconnected from server".format(self.nick))
        return False

    def set_nick(self, nick):
        if nick == self.nick:
            self.send_return(True)
        elif self._server.change_nick(self.nick, nick):
            self.nick = nick
            self.send_return(123, True)
        else:
            self.send_return(123, False)

    def join(self, chname):
        ch = self._server.get_channel(chname)
        if not ch.add_user(self):
            self.send_error(
                "can't join channel #{}".format(chname)
            )

    def leave(self, chname):
        ch = self._server.get_channel(chname)
        if ch.remove_user(self):
            self.send_return(123, True)
        else:
            self.send_return(123, False)

    def route_message(self, target_type, target, msg):
        if target_type == "CHANNEL":
            ch = self._server.get_channel(target, False)
            if not ch:
                self.send_error("channel doesn't exist.")
                return
            ch.send(msg, self.nick)
    

