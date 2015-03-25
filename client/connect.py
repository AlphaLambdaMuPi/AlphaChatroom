import logging
import asyncio
import json

from settings import *

from logsetting import *
logger = logging.getLogger('root')
init_logging(logger)


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
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    def start(self):
        coro = self.start_tcp_connection()
        self.loop.create_task(coro)
        #loop.create_task(coro)

    @asyncio.coroutine
    def start_tcp_connection(self):
        try:
            reader, writer = yield from asyncio.open_connection(SERVER_IP, 9007)
        except Exception as e:
            logger.error(e)
            return False


        while True:
            x = { 'nick': 'bobogei' }
            mesg = json.dumps(x) + '\n'
            writer.write(mesg.encode())
            logger.debug('wrote: %s ', mesg)

            data = yield from reader.readline()
            logger.debug('receive: %s ', data)

            yield from asyncio.sleep(0.5)
