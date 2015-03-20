#! /usr/bin/env python

import asyncio
from user import User
from channel import Channel

class ChatServer:
    def __init__(self):
        self.channels = {}
        self.users = {}
        self.name = "SYSTEM"
        self.hellostr = "Hi {}, this is your current nickname."

    @asyncio.coroutine
    def __call__(self, sr, sw):
        data = yield from sr.read()
        try:
            data = json.loads(data.decode())
        except UnicodeError:
            logger.info("can't convert byte to string")
        except ValueError:
            logger.info("get wrong json format")
        
        if "nick" in data and data['nick'] != self.name:
            nick = self.gen_nick(data['nick'])
            self.users[nick] = User(self, nick, sr, sw)
            self.users[nick].send_call('init_conn', self.name, nick)
            self.users[nick].send(
                self.hellostr.format(nick),
                self.name
            )
            res = yield from self.users[nick].run()
            if res == False:
                del self.users[nick]

    def gen_nick(nick):
        while nick in self.users:
            nick = nick + '_'
        return nick

    def get_channel(self, chname):
        if chname not in self.channels:
            self.channels[chname] = Channel(self, chname)
        return self.channels[chname]

# global object       
chat_server = ChatServer() 
