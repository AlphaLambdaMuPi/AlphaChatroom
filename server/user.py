#! /usr/bin/env python

import asyncio
import logging

logger = logging.getLogger()

class User:
    def __init__(self, server, nick, conn):
        self.nick = nick

        self._server = server
        self._conn = conn
        self._own_chs = {}

        self._funcs = {}
        self._funcs['set_nick'] = self.set_nick
        self._funcs['join'] = self.join
        self._funcs['leave'] = self.leave
        self._funcs['route_message'] = self.route_msg


    def _send(self, data):
        try:
            self._conn.send(data)
        except ConnectionError:
            logger.debug("connection error")

    def send_error(self, errmsg):
        data = {"type": "ERROR", "msg": errmsg}
        self._send(data)
    
    def send_return(self, rid, ret):
        data = {"type": "RETURN", "retid": rid, "ret": ret}
        self._send(data)

    def send_call(self, funcname, *args):
        data = {"type": "CALL", "func": funcname, "params": args}
        self._send(data)
    
    def send_msg(self, msg, fr, ch=None):
        self.send_call("get_message", msg, fr, ch)

    @asyncio.coroutine
    def run(self):
        while self._conn.alive():
            data = yield from self._conn.recv()
            if not isinstance(data, dict):
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
        self._server.del_user(self)

    def set_nick(self, nick):
        if nick == self.nick:
            self.send_return(True)
        elif self._server.change_nick(self, nick):
            self.nick = nick
            self.send_return(123, True)
        else:
            self.send_return(123, False)

    def join(self, chname):
        ch = self._server.get_channel(chname, create=True)
        if not ch.add_user(self):
            self.send_error("can't join channel #{}".format(chname))
        else:
            self.send_call('successful_join_channel', chname)

    def leave(self, chname):
        ch = self._server.get_channel(chname)
        if ch.remove_user(self):
            self.send_return(123, True)
        else:
            self.send_return(123, False)

    def route_msg(self, target_type, target, msg):
        self._server.route_msg(target_type, target, msg, self)
    

