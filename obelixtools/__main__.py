#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import API
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO
)

if __name__ is '__main__':
    logger = logging.getLogger(__name__)
    test = API()
    test.check_connection()
    test.speedtest()
