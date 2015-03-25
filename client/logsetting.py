import logging
import sys

def init_logging(log):
    formatter = logging.Formatter(fmt = '[%(asctime)s.%(msecs)d] %(module)s - %(levelname)s : %(message)s'
                                  ,datefmt = '%H:%M:%S')
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    log.addHandler(console)
