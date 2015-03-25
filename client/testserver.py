
@asyncio.coroutine
def tcp_server_connect():

    reader, writer = yield from asyncio.open_connection(SERVER_IP, 9007)

    while True:
        mesg = json.dumps(x) + '\n'
        writer.write(mesg.encode())
        logger.debug(1, 2)

        data = yield from reader.readline()
