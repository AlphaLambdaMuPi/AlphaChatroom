#! /usr/bin/env python

import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class User:
    def __init__(self, server, nick, conn):
        self._server = server
        self._nick = nick
        self._conn = conn

        self._funcs = {}
        self._funcs['set_nick'] = self.set_nick
        self._funcs['join'] = self.join
        self._funcs['leave'] = self.leave

    @asyncio.coroutine
    def run(self):
        while self._conn.is_connected():
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
        return False

    def get_nick(self, nick):
        return self._nick

    def set_nick(self, nick):
        if self._server.change_nick(self._nick, nick):
            self._nick = nick
            self.send_return(True)
        else:
            self.send_return(False)

    def join(self, chname):
        ch = self._server.get_channel(chname)
        if  not ch.add_user(self):
            self.send_error(
                "can't join channel #{}".format(chname)
            )

    def leave(self, chname):
        ch = self._server.get_channel(chname)
        if ch.remove_user(self):
            self.send_return(True)
        else:
            self.send_return(False)

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
    

