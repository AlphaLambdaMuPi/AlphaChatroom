#!/usr/bin/env python

import asyncio
import logging
import server

from server import chat_server

async_logger = logging.getLogger("asyncio")
async_logger.setLevel(logging.WARNING)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    start_server = asyncio.start_server(chat_server, 'localhost', 9007)
    s = loop.run_until_complete(start_server)

    print('serving on', s.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("exit.")
    finally:
        loop.close()
