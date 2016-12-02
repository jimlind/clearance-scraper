#!/usr/bin/python
import logging

def setupLogging(level):
    logging.basicConfig(
        filename = 'browser.log',
        format = '%(asctime)s %(levelname)-8s %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        level = level
    )
    logging.getLogger('Browser')

def setupDebug():
    setupLogging(logging.DEBUG)

def setupWarning():
    setupLogging(logging.WARNING)
