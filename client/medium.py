import logging
import asyncio
import json
import re
import os
import random
import string
import subprocess
import signal

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *
from quamash import QEventLoop

from datetime import datetime

from settings import *
import regex

from connect import Connect, FileSendConnect

from logsetting import *
logger = logging.getLogger('root')


class Medium(QObject):

    avatarChanged = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.connect = Connect(self)
        self.file_connect = Connect(self)
        self.state = 0
        self.channels = []
        self.name = ''
        self._file_map = {}
        pass

    def goodbye(self):
        if not self._ps is None:
            self._ps.kill()

    def setEngine(self, engine):
        self.engine = engine
        self.root = engine.rootObjects()[0]


    def connect_server(self):
        try:
            self.connect.start()
        except Exception as e:
            logging.error('Cant connect server: %s', str(e))
            self.state = 0
            return

        self.state = 1

    def _login(self, nick):
        
        self.name = nick
        try:
            self.connect.putq( {'nick': nick} )
        except Exception as e:
            logging.error('Cant login server: %s', str(e))
            self.state = 0
            return

        self.state = 2
        self.channels = []

    def join_channel(self, channel):

        try:
            self.connect.putq({
                'type': 'CALL',
                'func': 'join',
                'params': [channel],
            })
        except Exception as e:
            logging.error('Cant join server: %s', str(e))

        logger.info('Success joined channel: %s', channel)


    def send_msg(self, channel_type, channel, mesg):
        if channel_type == 'CHANNEL' and (channel not in self.channels):
            logger.warning( 'You are not in the channel.' )
            #return
        #mesg = re.sub(r'\^_\^;;', r"<img src='Image://emoticon/4-16'>", mesg)
        #mesg = re.sub('\$([^$]+)\$', r'<img src="http://latex.codecogs.com/png.latex?\1"/>', mesg)
        #mesg = re.sub('\n', r'<br>', mesg)
        logger.info(mesg)


        self.connect.putq({
            'type': 'CALL',
            'func': 'route_message',
            'params': [channel_type, channel, mesg],
        })

    def receive_msg(self, data):

        logger.info("receive_msg gets :" + str(data))
        if data['type'] == 'CALL' and data['params'][1] != 'SYSTEM':
            logger.info("Get call:" + str(data))
            self.root.receive_msg({
                'type': 'text',
                'data': {
                    'sender': data['params'][1],
                    'mesg': data['params'][0]
                }
            })

    def receive(self, data):
        if data['type'] == 'CALL':
            func = 'S' + data['func']
            try:
                func = getattr(self, func)
            except AttributeError:
                logger.error('The function %s is not found', func)
                return

            if not callable(func):
                logger.error('The function %s is not callable', func)
                return

            try:
                res = func(*data['params'])
            except Exception as e:
                logger.error('Call function %s Error: %s', func, e)

    def hello(self):
        self.connect_server()

    def time_string(self):
        return datetime.now().strftime('%H:%M')

    def set_avatar(self):
        self.connect.put_call('set_avatar', 
                self.engine.imageProvider('avatarImage').base64('__self__')
            )

    def Sget_message(self, msg, fr, channel):
        if(channel is None):
            channel = 'User:' + fr
            print(fr)
        msg = regex.do_sub(msg)
        self.root.receive_msg(channel, {
            'type': 'text',
            'data': {
                'sender': fr,
                'mesg': msg,
                'timeStr': self.time_string()
            }
        })

    def Ssuccess_join(self, channel):
        self.channels.append(channel)
        self.root.channelAddActive(channel)

    def Sget_users_in_channel(self, ch, ls):
        for x in ls:
            self.engine.imageProvider('avatarImage').pushImage(_id=x['nick'], base64=x['pic'])

        self.root.receiveChatUsersList(ch, [{'name': x['nick']} for x in ls])

    def Suser_join_channel(self, x, ch):
        self.engine.imageProvider('avatarImage').pushImage(_id=x['nick'], base64=x['pic'])
        logger.debug('Get user <%s> join channel [%s].', x['nick'], ch)
        self.root.receiveUserJoin(ch, {'name': x['nick']})

    def Ssend_file_accepted(self, token, retid):
        print(self._file_map)
        logger.debug('retid = %s, file_url = %s', retid, self._file_map[retid])
        #fsc = FileSendConnect(self._file_map[retid], token)
        #fsc.start()
        self.connect.put_file('SEND', self._file_map[retid], token)

    def Sfile_uploaded(self, token, info, user, ch):
        self.root.receive_msg(ch, {
            'type': 'file',
            'data': {
                'sender': user,
                'file_name': info[0],
                'file_size': info[1],
                'token': token,
                'timeStr': datetime.now().strftime('%H:%M')
            }
        })


    def Sget_streaming_feed(self, url):
        
        logger.debug("exec ffmpeg -f v4l2 -i /dev/video0 -thread_queue_size 512 -f alsa -i hw:0,0 -async 1 {} > /dev/null 2>&1".format(url))
        self._ps = subprocess.Popen(
                "exec ffmpeg -f v4l2 -i /dev/video0 -thread_queue_size 512 -f alsa -i hw:0,0 -async 1 {} > /dev/null 2>&1".format(url),
                shell = True
            )
        

    def Sget_streaming_point(self, url, user, ch):
        logger.debug("Get point: %s, %s, %s", url, user, ch)
        self.root.receive_msg(ch, {
            'type': 'streaming',
            'data': {
                'sender': user,
                'url': url
            }
        })


    @pyqtSlot(str)
    def Qlogin(self, nick):
        if len(nick) > 30: return False
        if not re.match('[\w-]+', nick): return False
        self._login(nick)
        self.root.onLoggedIn(nick)
        self.set_avatar()
        return True

    @pyqtSlot(str)
    def Qjoin(self, channel):
        logger.info('qml request join')
        self.join_channel(channel)

    @pyqtSlot(str, str)
    def Qsend(self, ch, s):
        logger.debug("Qsend channel = %s : %s", ch, s)
        if(ch[:5] == 'User:'):
            self.send_msg('USER', ch[5:], s)
            self.root.receive_msg('User:' + ch[5:], {
                'type': 'text',
                'data': {
                    'sender': self.name,
                    'mesg': s,
                    'timeStr': self.time_string(),
                }
            })
        else: self.send_msg('CHANNEL', ch, s)

    def random_string(self, length = 20):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


    @pyqtSlot(str)
    def Qavatar(self, url):
        self.engine.imageProvider('avatarImage').pushImage(_id='__self__', url=url)
        self.avatarChanged.emit()

    @pyqtSlot(str, str)
    def QsendFile(self, url, ch):
        file_url = QUrl(url).toLocalFile()
        if not os.path.isfile(file_url):
            logger.warning('file %s isn\'t a regular file', file_url)
            return

        rnd_str = self.random_string()
        self._file_map[rnd_str] = file_url
        self.connect.put_call(
            'send_file',
            os.path.basename(file_url),
            os.path.getsize(file_url),
            '12345MD512345',
            ch,
            rnd_str
        )
        #self.avatarChanged.emit()

    def refreshProgress(self, token, l):
        self.root.refreshProgress(token, l)

    @pyqtSlot(str)
    def QgetUsers(self, ch):
        if(ch[:5] == 'User:'): return
        self.connect.put_call('request_users_in_channel', ch)

    @pyqtSlot(str)
    def QleaveChannel(self, ch):
        self.connect.put_call('leave', ch)

    @pyqtSlot(str, str)
    def QstartGetFile(self, file_name, token):
        fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download')
        fn = os.path.join(fn, file_name)
        logger.debug('Start get file, %s, %s', fn, token)
        self.connect.put_file('GET', fn, token)

    @pyqtSlot(str)
    def QstartGetStreaming(self, url):
        fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download')
        fn = os.path.join(fn, file_name)
        logger.debug('Start get file, %s, %s', fn, token)
        self.connect.put_file('GET', fn, token)

    @pyqtSlot(str)
    def QstartStreaming(self, ch):
        self.connect.put_call('start_streaming', ch)
        self.root.receive_msg(ch, {
            'type': 'streamingIndicate',
            'data': {},
        })

    @pyqtSlot(str)
    def QcallReleaseFeed(self, ch):
        logger.debug('Kill subprocess %s', self._ps.pid)
        self.connect.put_call('stop_streaming', ch)
        #os.killpg(self._ps.pid, signal.SIGTERM)
        self._ps.kill()

    
        

