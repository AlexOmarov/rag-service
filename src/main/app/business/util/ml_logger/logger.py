"""
Factory method for creating logger
"""

import logging

_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"


def create_logger(name):
    """ Create formatted logger with default config """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(_get_stream_handler())
    return logger


def _get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_LOG_FORMAT))
    return stream_handler
