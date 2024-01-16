#!/bin/python3
import argparse
import os
import platform
from logging.handlers import RotatingFileHandler
import logging
import time
logger = logging.getLogger()

from .slack import Slack

import farm

# https://thingspeak.com/channels/68316/private_show

def main():
    logger.info("PiFarm v1.0")
    logger.info(f'python-version = {platform.python_version()}')

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="Debug mode, forces use of windows", action="store_true")
    args = parser.parse_args()

    farm.init_logs(args.debug)

    try:
        logger.debug(f'Setting up sensor array...')
        ## init the farm    
        Slack.send('Farm is UP')
        sensors = farm.SensorArray()
        sensors.append(farm.Sensor_tmp102('test'))

        while True:
            sensors.read()
            sensors.publish()
            time.sleep(60 * 15)

    finally:
        Slack.send('Farm is DOWN')

if __name__ == "__main__":
    main()
