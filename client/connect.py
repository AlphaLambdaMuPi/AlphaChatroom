import logging
import asyncio
import json

from settings import *

from logsetting import *
logger = logging.getLogger('root')

logger.debug('123131231231321')
print('1231')

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
    def __init__(self, logic):
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.logic = logic
        self.connected = False
        self.joined = False
        self.channel = 'zzzzzz'

    def start(self):
        logger.info('Start connect')
        fut = asyncio.Future()
        self.loop.create_task(self.start_tcp_connection(fut))
        self.loop.create_task(self.send_loop(fut))
        self.loop.create_task(self.receive_loop(fut))
        self.putq( {'nick': 'bobogei'} )
        self.putq( {'type': 'CALL',
            'func': 'join',
            'params': ['zzzzzz']} )
        self.connected = self.joined = True

    def send_text(self, s):
        if not self.joined:
            logger.warning( 'Send text but not joined' )
            return

        self.putq( {
            'type': 'CALL',
            'func': 'route_message',
            'params': ['CHANNEL', self.channel, s],
        })
            

    def putq(self, x):
        self.queue.put_nowait(x)

    @asyncio.coroutine
    def start_tcp_connection(self, fut):
        try:
            self.reader, self.writer = yield from asyncio.open_connection(SERVER_IP, 9007)
        except Exception as e:
            logger.error(e)
            return False

        logger.info('Connected')
        fut.set_result(True)
        return True


    @asyncio.coroutine
    def send_loop(self, fut):
        res = yield from asyncio.wait_for(fut, 20)
        logger.info(res)

        while True:
            x = yield from self.queue.get()
            logger.debug('queue get: %s ', str(x))
            mesg = json.dumps(x) + '\n'
            self.writer.write(mesg.encode())
            logger.debug('wrote: %s ', mesg)

    @asyncio.coroutine
    def receive_loop(self, fut):
        res = yield from asyncio.wait_for(fut, 20)
        logger.info(res)

        while True:
            data = yield from self.reader.readline()
            logger.debug('receive: %s ', data)
            self.logic.receive(data.decode())
            if not len(data) and self.reader.at_eof():
                logger.info('Server connection closed')
                return 
