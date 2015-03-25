#! /usr/bin/env python

import asyncio
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Connection:
    def __init__(self, sr, sw):
        self._sr = sr
        self._sw = sw
        self._is_connected = True

    @asyncio.coroutine
    def recv(self):
        if not self._is_connected:
            return

        if self._sr.at_eof():
            self._sw.close()
            self._is_connected = False
            return
        try:
            data = yield from self._sr.readline()
            data = json.loads(data.decode().strip())
        except UnicodeError:
            logger.info("can't convert byte to string")
            data = None
        except ValueError:
            logger.info("get wrong json format")
            data = None
        except ConnectionResetError:
            logger.info("connection with {} was"
                        " dropped".format(self.nick))
            self._sw.close()
            self._is_connected = False
            data = None
        except Exception as e:
            print(e)
            data = None
        if type(data) is not dict:
            logger.info("data is not a dict")
            data = None
        return data

    def send(self, data):
        if not self._is_connected:
            logger.info("connection is dead")
            return
        try:
            data = json.dumps(data) + '\n'
        except ValueError:
            logger.warning("send wrong json format")
        self._sw.write(data.encode())

    def is_connected(self):
        return self._is_connected

