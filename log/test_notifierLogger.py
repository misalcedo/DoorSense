from unittest import TestCase
from unittest.mock import patch

from log.NotifierLogger import NotifierLogger


class TestNotifierLogger(TestCase):
    def setUp(self):
        self.closed_acceleration = 1
        self.allowed_delta = 2

    @patch('log.NotifierLogger.logging')
    def test___call__(self, mocked_logging):
        subject = 'subject'
        message = 'message'
        recipients = ['recipient1', 'recipient2']

        self.fake_method(subject, message, recipients)
        self.assertEqual(1, mocked_logging.info.call_count)

    @NotifierLogger
    def fake_method(self, *arguments):
        return len(arguments) > 0
