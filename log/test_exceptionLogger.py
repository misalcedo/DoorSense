from smtplib import SMTPException
from unittest import TestCase
from unittest.mock import patch

from log.ExceptionLogger import ExceptionLogger


@ExceptionLogger
def succeeds(a):
    return a


@ExceptionLogger
def fails(a, b, c):
    a + b + c
    raise SMTPException('failed!')


class TestExceptionLogger(TestCase):
    @patch('log.ExceptionLogger.logging')
    def test___call__succeed(self, mocked_logging):
        succeeds(0)
        self.assertEqual(0, mocked_logging.error.call_count)

    @patch('log.ExceptionLogger.logging')
    def test___call__fail(self, mocked_logging):
        fails(1, 2, c=3)
        self.assertEqual(1, mocked_logging.error.call_count)
