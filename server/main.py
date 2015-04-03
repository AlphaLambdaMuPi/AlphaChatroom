#!/usr/bin/env python

import asyncio
import logging
import server

from server import chat_server
import logsetting

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

    coro = asyncio.start_server(chat_server, '0.0.0.0', 9007)
    s = loop.run_until_complete(coro)

    logger.info('serving on {}'.format(s.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print()
        loop.run_until_complete(chat_server.stop())
    finally:
        loop.run_until_complete(check_tasks())
        loop.close()
        print("exit.")
