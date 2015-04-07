from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *
from PyQt5.QtMultimedia import *

from medium import Medium

class VideoProbe(QVideoProbe):

    framed = pyqtSignal(QVideoFrame)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._source = ''
        self._medium = None

    @pyqtProperty(QMediaObject)
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source
        self.setSource(source.property('mediaObject'))
        self.videoFrameProbed.connect(self.emitFrame)
        print(self.isActive())


    @pyqtSlot(QVideoFrame)
    def emitFrame(self, frame):
        print('get frame')


