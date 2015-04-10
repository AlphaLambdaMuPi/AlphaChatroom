#!/usr/bin/env python

import asyncio
import logging
import server

from server import chat_server
from fileserver import file_server
import logsetting
from settings import settings as SETTINGS

logsetting.log_setup()
logger = logging.getLogger()

@asyncio.coroutine
def check_tasks():
    now = len(asyncio.Task.all_tasks())
    while now > 2:
        yield from asyncio.sleep(1)
        # print(asyncio.Task.all_tasks())
        now = len(asyncio.Task.all_tasks())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    coro = asyncio.start_server(chat_server, SETTINGS['ip'], SETTINGS['port'])
    coro2 = asyncio.start_server(file_server, SETTINGS['ip'], SETTINGS['port'] + 1)
    s = loop.run_until_complete(coro)
    fs = loop.run_until_complete(coro2)

    logger.info('serving on {}'.format(s.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print()
        loop.run_until_complete(chat_server.stop())
        loop.run_until_complete(file_server.stop())
    finally:
        loop.run_until_complete(check_tasks())
        loop.close()
        print("exit.")
