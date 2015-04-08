import logging
import asyncio
import json

from settings import *

from logsetting import *
logger = logging.getLogger('root')

from base64 import b64encode, b64decode

@asyncio.coroutine
def test_el():
    i = 0
    while True:
        print(i)
        yield from asyncio.sleep(0.5)
        i += 1

        if i > 10:
            return


class Connect:
    def __init__(self, medium):
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.medium = medium
        self.file_queue = asyncio.Queue()

    def start(self, port = 9007):
        logger.info('Start connect')
        fut = asyncio.Future()
        self.loop.create_task(self.start_tcp_connection(fut, port))
        self.loop.create_task(self.send_loop(fut))
        self.loop.create_task(self.receive_loop(fut))
        self.loop.create_task(self.file_watch_dog())
            

    def putq(self, x):
        self.queue.put_nowait(x)

    def put_call(self, func, *args):
        self.putq({
            'type': 'CALL',
            'func': func,
            'params': args,
            })

    def put_file(self, typ, url, token):
        self.file_queue.put_nowait((typ, url, token))

    @asyncio.coroutine
    def start_tcp_connection(self, fut, port):
        try:
            reader, writer = yield from asyncio.open_connection(SERVER_IP, port)
        except Exception as e:
            logger.error(e)
            return False

        logger.info('Connected')
        fut.set_result((reader, writer))
        return True


    @asyncio.coroutine
    def send_loop(self, fut):
        reader, writer = yield from asyncio.wait_for(fut, 20)
        logger.info(writer)

        while True:
            x = yield from self.queue.get()
            logger.debug('queue get: %s ', str(x))
            mesg = json.dumps(x) + '\n'
            writer.write(mesg.encode())
            logger.debug('wrote: %s ', mesg)

    @asyncio.coroutine
    def receive_loop(self, fut):
        reader, writer = yield from asyncio.wait_for(fut, 20)
        logger.info(reader)

        while True:
            data = yield from reader.readline()
            logger.debug('receive: %s ', data)
            try:
                self.medium.receive(json.loads(data.decode()))
            except Exception as e:
                logger.error('Json decode error: %s', str(e))
            if not len(data) and reader.at_eof():
                logger.info('Server connection closed')
                return 
    
    @asyncio.coroutine
    def file_watch_dog(self):
        while True:
            typ, url, token = yield from self.file_queue.get()
            print(typ, url, token, typ == 'SEND')
            if typ == 'SEND':
                fut = asyncio.Future()
                self.loop.create_task(self.start_tcp_connection(fut, 9008))
                self.loop.create_task(self.send_file_loop(fut, url, token))

    @asyncio.coroutine
    def send_file_loop(self, fut, url, token):
        reader, writer = yield from asyncio.wait_for(fut, 20)
        logger.info(writer)

        writer.write( json.dumps({
            'op': 'PUT',
            'token': token,
        }).encode() + b'\n' )
        logger.debug('Wrote first line, start send file %s...', url)

        with open(url, 'rb') as f:
            while True:
                logger.debug('Send file loop!')
                data = f.read(16384)
                if not data: break
                b64data = b64encode(data)
                #logger.debug('Sending data %s ...', str(b64data))
                writer.write(
                        b64data + b'\n'
                    )
                yield from asyncio.sleep(0)

        logger.debug('Done!')
        writer.write_eof()

            


class FileSendConnect:
    def __init__(self, url, token):
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.url = url
        self.token = token

    def start(self, port = 9008):
        
        logger.info('Start connect')
        fut = asyncio.Future()
        self.loop.create_task(self.start_tcp_connection(fut, port))
        self.loop.create_task(self.send_loop(fut))
            
    @asyncio.coroutine
    def start_tcp_connection(self, fut, port):
        try:
            self.reader, self.writer = yield from asyncio.open_connection(SERVER_IP, port)
        except Exception as e:
            logger.error(e)
            return False

        logger.info('File Server Connected')
        fut.set_result(True)
        return True


    @asyncio.coroutine
    def send_loop(self, fut):
        res = yield from asyncio.wait_for(fut, 20)
        logger.info(res)

        self.writer.write( json.dumps({
            'op': 'PUT',
            'token': self.token,
        }).encode() + b'\n' )
        logger.debug('Wrote first line, start send file %s...', self.url)

        with open(self.url, 'rb') as f:
            while True:
                logger.debug('Send file loop!')
                data = f.read(16384)
                if not data: break
                b64data = b64encode(data)
                #logger.debug('Sending data %s ...', str(b64data))
                self.writer.write(
                        b64data + b'\n'
                    )
                yield from asyncio.sleep(0)

        logger.debug('Done!')
        self.writer.write_eof()


