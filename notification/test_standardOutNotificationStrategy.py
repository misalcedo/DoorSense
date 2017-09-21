from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from notification.StandardOutNotificationStrategy import StandardOutNotificationStrategy


class TestStandardOutNotificationStrategy(TestCase):
    def setUp(self):
        self.now = datetime(year=2016, day=29, month=9, hour=2, minute=24, second=34)
        self.notification_strategy = StandardOutNotificationStrategy()

    @patch('notification.StandardOutNotificationStrategy.print')
    @patch('notification.StandardOutNotificationStrategy.datetime')
    def test_notify(self, mocked_datetime, mocked_print):
        mocked_datetime.now.return_value = self.now

        subject = 'subject'
        message = 'message'
        recipients = ['recipient1', 'recipient2']

        self.notification_strategy.notify(subject, message, recipients)

        expected = {'subject': subject, 'message': message, 'recipients': recipients, 'time': self.now}
        mocked_print.assert_called_with(expected)
