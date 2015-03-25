import logging
import asyncio
import json

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *
from quamash import QEventLoop

from settings import *
from logsetting import *
from connect import Connect
logger = logging.getLogger('root')

init_logging(logger)


