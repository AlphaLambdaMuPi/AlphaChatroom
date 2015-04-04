#! /usr/bin/env python

import asyncio
import logging

logger = logging.getLogger()

class User:
    def __init__(self, server, fileserver, nick, conn):
        self.nick = nick
        self.pic = ""

        self._server = server
        self._fileserver = fileserver
        self._conn = conn
        self._own_chs = {}
        self._chs = set()

        self._funcs = {}
        self._funcs['set_nick'] = self.set_nick
        self._funcs['join'] = self.join
        self._funcs['leave'] = self.leave
        self._funcs['route_message'] = self.route_msg
        self._funcs['request_channels'] = self.request_channels
        self._funcs['request_users_in_channel'] = self.request_users_in_channel
        self._funcs['set_avatar'] = self.set_avatar

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

    def set_avatar(self, pic):
        self.pic = pic
        self.send_return(123, True)

    def join(self, chname):
        ch = self._server.get_channel(chname, create=True)
        if ch and ch.add_user(self):
            self.send_call('success_join', chname)
            self._chs.add(chname)
        else:
            self.send_error("can't join channel #{}".format(chname))

    def leave(self, chname):
        ch = self._server.get_channel(chname)
        if ch and ch.remove_user(self):
            self.send_return(123, True)
            self._chs.remove(chname)
        else:
            self.send_return(123, False)

    def request_channels(self):
        self.send_call("get_channels", list(self._chs))

    def request_users_in_channel(self, chname):
        ch = self._server.get_channel(chname)
        if ch:
            self.send_call("get_users_in_channel", chname, ch.get_users())
        else:
            self.send_error("channel #{} doesn't exist.".format(chname))

    def send_file(self, filename, filesize):
        token = self._fileserver.request_token(filesize)
        return token

    def route_msg(self, target_type, target, msg):
        self._server.route_msg(target_type, target, msg, self)

    def get_info(self):
        return {
            "nick": self.nick, 
            "pic": self.pic,
        }
