import sys
import os
from logging.handlers import RotatingFileHandler
import logging
logger = logging.getLogger()

logFile = 'farm.log'

def init_logs(debug):
    handler = RotatingFileHandler(logFile, mode='a', backupCount=5)
    if os.path.isfile(logFile):
        handler.doRollover()
    logging.basicConfig(filename=logFile, level=logging.DEBUG)
    console = logging.StreamHandler()
    if debug:
        logLevel = logging.DEBUG
    else:
        logLevel = logging.INFO

    if "pytest" in sys.modules:       
        logLevel = logging.DEBUG

    console.setLevel(logLevel)
    logger.addHandler(console)
    logger.info('Setup logger...')