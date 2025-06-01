"""
Tests of the logger
"""

import logging

from src.main.app.business.util.ml_logger.logger import create_logger


class TestLogger:
    """
    Class for logger tests
    """
    def _setup(self):
        print("basic setup into class")

    def _teardown(self):
        print("basic teardown into class")

    @classmethod
    def _setup_class(cls):
        print("class setup")

    @classmethod
    def _teardown_class(cls):
        print("class teardown")

    def _setup_method(self):
        print("method setup")

    def _teardown_method(self):
        print("method teardown")

    def test_created_logger(self):
        """
        Logger creation test
        """

        logger_name = "TEST_LOGGER"
        log = create_logger(logger_name)

        assert log is not None
        assert log.level == logging.INFO

    def test_when_logger_is_created_name_is_applied(self):
        """
        Logger name test
        """

        logger_name = "TEST_LOGGER"
        log = create_logger(logger_name)

        assert log.name == logger_name
