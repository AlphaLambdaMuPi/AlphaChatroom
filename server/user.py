#! /usr/bin/env python

import asyncio
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class User:
    def __init__(self, server, nick, sr, sw):
        self.server = server
        self.nick = nick
        self.sr = sr
        self.sw = sw

        self.funcs = {}
        self.funcs['set_nick'] = self.set_nick
        self.funcs['join'] = self.join
        self.funcs['leave'] = self.leave

    def _send(self, data):
        try:
            data = json.dumps(data)
        except ValueError:
            logger.warning("send wrong json format")
        self.sw.write(data.encode());

    @asyncio.coroutine
    def run(self):
        while True:
            try:
                data = yield from self.sr.read()
                data = json.loads(data.decode().strip())
            except UnicodeError:
                logger.info("can't convert byte to string")
            except ValueError:
                logger.info("get wrong json format")
            except ConnectionResetError:
                logger.info("connection with {} was"
                            " dropped".format(self.nick))
                self.sw.close()
                return False

            if "type" in data and data["type"] == "CALL":
                try:
                    ret = self.funcs[data["func"]](*data["params"])
                    if "retid" in data:
                        self.send_return(data["retid"], ret)
                except KeyError:
                    self.send_error("invalid operation")

        
    def set_nick(self, nick):
        if self.server.change_nick(self.nick, nick):
            self.nick = nick
            self.send_return(True)
        else:
            self.send_return(False)

    def join(self, chname):
        ch = self.server.get_channel(chname)
        if  not ch.add_user(self):
            self.send_error(
                "can't join channel #{}".format(chname)
            )

    def leave(self, chname):
        ch = self.server.get_channel(chname)
        if ch.remove_user(self):
            self.send_return(True)
        else:
            self.send_return(False)

    def send_error(self, errmsg):
        data = {"type": "ERROR", "msg": errmsg}
        self._send(data)
    
    def send_return(self, rid, ret):
        data = {"type": "RETURN", "retid": rid, "ret": ret}
        self._send(data)

    def send_call(self, funcname, *args):
        data = {"type": "CALL", "ret": d}
        self._send(data)
    
    def send(self, msg, fr, ch=None):
        data = {"type": "MSG", "msg": msg, "from": fr, "channel": ch}
        self._send(data)
    

