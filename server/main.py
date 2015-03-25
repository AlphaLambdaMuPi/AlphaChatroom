#!/usr/bin/env python

import asyncio
import logging
import server

from server import chat_server
import logsetting

logsetting.log_setup()
logger = logging.getLogger()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    start_server = asyncio.start_server(chat_server, '0.0.0.0', 9007)
    s = loop.run_until_complete(start_server)

    logger.info('serving on {}'.format(s.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("exit.")
    finally:
        loop.close()
