import logging
import sys

LOG_FILE_NAME = 'client.log'
logging.basicConfig(filename=LOG_FILE_NAME,
                    filemode='a',
                    format='[%(asctime)s.%(msecs)d] %(module)s - %(levelname)s : %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger('root')

formatter = logging.Formatter(fmt = '[%(asctime)s.%(msecs)d] %(module)s - %(levelname)s : %(message)s'
                              ,datefmt = '%H:%M:%S')
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
logger.addHandler(console)
