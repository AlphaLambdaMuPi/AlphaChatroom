#! /usr/bin/env python

import asyncio
import logging
import base64
import uuid
import hashlib

from connection import StreamConnection

logger = logging.getLogger()

class FileServer:
    def __init__(self, loop=None):
        self._loop = loop
        if not self._loop:
            self._loop = asyncio.get_event_loop()
        self._filemap = {}
        self._connmap = {}

    @asyncio.coroutine
    def __call__(self, sr, sw):
        conn = StreamConnection(sr, sw)
        try:
            yield from asyncio.wait_for(self.get_token(conn), 10.0)
        except asyncio.TimeoutError:
            conn.close()
            return
        else:
            result = yield from recv_file(conn)
    
    @asyncio.coroutine
    def get_token(self, conn):
        yield from conn.recv()

    def request_token(self, filename, filesize):
        m = haslib.sha1()
        m.update(uuid.uuid4().bytes)
        token = base64.b64encode(m.digest())
        self._filemap[token] = (filename, filesize)
        return token

    @asyncio.coroutine
    def stop(self):
        pass

# global object       
file_server = FileServer() 


