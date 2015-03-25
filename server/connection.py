#! /usr/bin/env python

import asyncio
import json
import logging

logger = logging.getLogger()

class Connection:
    def __init__(self, sr, sw):
        self._sr = sr
        self._sw = sw

    @asyncio.coroutine
    def recv(self):
        if not self.alive():
            raise ConnectionError("connection was closed.")
        data = yield from self._sr.readline()
        data = data.strip()
        return data

    def send(self, data):
        if not self.alive():
            raise ConnectionError("connection was closed.")
        data = data + b'\n'
        try:
            self._sw.write(data)
        except OSError:
            raise ConnectionError("can't send data.")

    @asyncio.coroutine
    def read(self, n=-1):
        if not self.alive():
            raise ConnectionError("connection was closed.")
        data = yield from self._sr.read(n)
        return data
    
    def write(self, data):
        if not self.alive():
            raise ConnectionError("connection was closed.")
        try:
            self._sw.write(data)
        except OSError:
            raise ConnectionError("can't send data.")

    def alive(self):
        return not self._sr.at_eof()


class JsonConnection(Connection):
    def __init__(self, sr, sw):
        super().__init__(sr, sw)

    @asyncio.coroutine
    def recv(self):
        try:
            data = yield from super().recv()
            data = data.decode()
            logger.debug("recv: {}".format(data))
            data = json.loads(data)
        except ConnectionError:
            return
        except UnicodeError:
            logger.debug("can't convert byte to string")
            return
        except ValueError:
            logger.debug("get wrong json format")
            return
        if type(data) is not dict:
            logger.debug("data is not a dict")
            return
        return data

    def send(self, data):
        try:
            logger.debug("send: {}".format(data))
            data = json.dumps(data).encode()
            super().send(data)
        except ConnectionError:
            logger.warning("can't send data")
            return
        except ValueError:
            logger.error("wrong json format")
            return

