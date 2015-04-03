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
        self.image = QImage(self.USE_SIZE, self.USE_SIZE, QImage.Format_RGB32)
        self._url = ""

    def requestImage(self, _id, size):
        #image = QImage(100, 100)
        if self.url == '':
            self.image.fill(QColor(randint(0, 255), randint(0, 255), randint(0, 255)))
        else:
            try:
                raw_image = QImage(QUrl(self.url).toLocalFile())
            except Exception as e:
                logger.error('Get image from url %s failed: %s', self.url, str(e))
            self.image = raw_image.scaled(self.USE_SIZE, self.USE_SIZE, Qt.KeepAspectRatio)

        #print(self.image.format())
        #yy = QByteArray()
        #buf = QBuffer(yy)
        #buf.open(QIODevice.WriteOnly)
        #self.image.save(buf, 'PNG')
        #qqq = QImage.fromData(yy)
        #return qqq, QSize(self.USE_SIZE, self.USE_SIZE)

        return self.image, QSize(self.USE_SIZE, self.USE_SIZE)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, u):
        self._url = u

                
