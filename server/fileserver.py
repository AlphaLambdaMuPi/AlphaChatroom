#! /usr/bin/env python

import asyncio
import logging
import base64
import uuid
import json
import hashlib
import hmac
import os.path

from connection import StreamConnection

logger = logging.getLogger()

class FileServer:
    BLOCK_SIZE = 16384
    def __init__(self, tmpdir, *, loop=None):
        self._tmpdir = tmpdir
        self._filemap = {}
        self._connmap = {}
        self._filefutures = {}
        self._loop = loop
        if not self._loop:
            self._loop = asyncio.get_event_loop()

    @asyncio.coroutine
    def __call__(self, sr, sw):
        conn = StreamConnection(sr, sw)
        logger.debug("get connection")
        try:
            op, token = yield from asyncio.wait_for(self.get_token(conn), 10.0)
            logger.debug("get op and token")
        except asyncio.TimeoutError:
            conn.close()
            return
        else:
            if op == "PUT":
                result = yield from self.recv_file(conn, token)
            elif op == "GET":
                result = yield from self.send_file(conn, token)
    
    @asyncio.coroutine
    def get_token(self, conn):
        data = yield from conn.recv()
        try:
            if not data:
                return None, None
            data = json.loads(data.decode())
        except UnicodeError:
            logger.debug("can't convert byte to string")
        except ValueError:
            logger.debug("get wrong json format")
        else:
            if isinstance(data, dict) and 'token' in data and 'op' in data:
                return data['op'], data['token']
        return None, None
    
    @asyncio.coroutine
    def send_file(self, conn, token):
        if token not in self._filemap:
            return False
        try:
            tmpfile = open(os.path.join(self._tmpdir, token), 'rb')
        except OSError:
            logger.debug("file {} doens't exist".format(token))
            return False
        while conn.alive():
            data = tmpfile.read(BLOCK_SIZE)
            if data:
                data = base64.b64decode(data)
                conn.send(data)
                yield from asyncio.sleep(0)
            else:
                break
        tmpfile.close()
        conn.close()

    @asyncio.coroutine
    def recv_file(self, conn, token):
        logger.debug("recv_file start...")
        tmpfile = self.gen_tmpfile(token)
        if not tmpfile:
            return False
        m = hashlib.md5()
        while conn.alive():
            data = yield from conn.recv()
            if data:
                data = base64.b64decode(data)
                tmpfile.write(data)
                m.update(data)
        md5 = m.hexdigest()
        tmpfile.close()
        logger.debug("recv_file done.")
        return True # debugging

        if hmac.compare_digest(md5, self._filemap[token][2]):
            return True
        else:
            try:
                os.remove(tmpfile.name)
            except:
                logger.error("can't delete file {}".format(tmpfile.name))
            return False

    def gen_tmpfile(self, token):
        filepath = os.path.join(self._tmpdir, token)
        if os.path.isfile(filepath):
            return None
        tmpfile = open(filepath, 'wb')
        return tmpfile
    
    def request_token(self, filename, filesize, md5):
        m = hashlib.sha1()
        m.update(uuid.uuid4().bytes)
        token = m.hexdigest()
        self._filemap[token] = (filename, filesize, md5)
        return token

    def get_file_info(self, token):
        if token in self._filemap[token]:
            return self._filemap[token]
        else:
            return None

    def add_recv_callback(self, cb, token):
        pass
        # if token in self._filemap

    @asyncio.coroutine
    def stop(self):
        pass

# global object       
file_server = FileServer('/home/host/filetmp')


