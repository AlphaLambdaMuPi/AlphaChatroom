from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *
from PyQt5.QtGui import *

from random import randint

import logging
import logsetting
logger = logging.getLogger('root')

class ImageProvider(QQuickImageProvider):
    def __init__(self):
        super().__init__(QQuickImageProvider.Image)
        self.USE_SIZE = 200
        #self.image = QImage(self.USE_SIZE, self.USE_SIZE, QImage.Format_RGB32)
        self.image = {}
        self.image['__self__'] = QImage(self.USE_SIZE, self.USE_SIZE, QImage.Format_RGB32)
        self.image['__self__'].fill( QColor(randint(0, 255), randint(0, 255), randint(0, 255)) )

    def pushImage(self, _id, url='', base64=''):
        logger.debug("Push Image: %s", _id)
        if(url != ''):
            try:
                raw_image = QImage(QUrl(url).toLocalFile())
            except Exception as e:
                logger.error('Get image from url %s failed: %s', self.url, str(e))
            self.image[_id] = raw_image.scaled(self.USE_SIZE, self.USE_SIZE, Qt.KeepAspectRatio)
            return

        if(base64 != ''):
            qba = QByteArray.fromBase64(base64.encode())
            self.image[_id] = QImage.fromData(qba)
            return

        self.image[_id] = QImage(self.USE_SIZE, self.USE_SIZE).fill(QColor(randint(0, 255), randint(0, 255), randint(0, 255)))
        return

    def requestImage(self, _id, size):

        if _id in self.image:
            return self.image[_id], self.image[_id].size()

        logger.error('The image %s not found', _id)
        return QImage(), QSize(0, 0)

    def base64(self, _id):
        qba = QByteArray()
        buf = QBuffer(qba)
        buf.open(QIODevice.WriteOnly)
        self.image[_id].save(buf, 'PNG')
        return bytearray(qba.toBase64()).decode()


class EmoticonProvider(QQuickImageProvider):

    def __init__(self):
        super().__init__(QQuickImageProvider.Image)
        self.image = QImage('img/emoticon.png')

    def requestImage(self, _id, size):

        r, c = map(int, _id.split('-'))
        SIZE = 2000 / 29
        USE_SIZE = 30
        emo = self.image.copy(
                int(SIZE * c),
                int(SIZE * r),
                int(SIZE),
                int(SIZE)
            ).scaled(USE_SIZE, USE_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        

        return emo, emo.size()
                
