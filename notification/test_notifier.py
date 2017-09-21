from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import Mock, patch

from notification.Notifier import Notifier


class TestNotifier(TestCase):
    def setUp(self):
        self.now = datetime(year=2016, day=29, month=9, hour=2, minute=24, second=34)
        self.mocked_notification_strategy = Mock()
        self.notifier = Notifier(self.mocked_notification_strategy, 10)

    def test_notify(self):
        subject = 'subject'
        message = 'message'
        recipients = ['recipient1', 'recipient2']

        self.assertEqual(True, self.notifier.notify(subject, message, recipients))
        self.mocked_notification_strategy.notify.assert_called_once_with(subject, message, recipients)

    @patch('stream.TimeWindowStream.datetime')
    def test_not_notify_again(self, mocked_datetime):
        mocked_datetime.now.return_value = self.now

        subject = 'subject'
        message = 'message'
        recipients = ['recipient1', 'recipient2']

        self.assertEqual(True, self.notifier.notify(subject, message, recipients))
        mocked_datetime.now.return_value = self.now + timedelta(seconds=9)
        self.assertEqual(False, self.notifier.notify(subject, message + '2', recipients))

        self.mocked_notification_strategy.notify.assert_called_once_with(subject, message, recipients)

    @patch('stream.TimeWindowStream.datetime')
    def test_notify_again(self, mocked_datetime):
        mocked_datetime.now.return_value = self.now

        subject = 'subject'
        message = 'message'
        recipients = ['recipient1', 'recipient2']

        self.assertEqual(True, self.notifier.notify(subject, message, recipients))
        mocked_datetime.now.return_value = self.now + timedelta(seconds=10)
        self.assertEqual(True, self.notifier.notify(subject, message, recipients))
        self.assertEqual(False, self.notifier.notify(subject, message, recipients))

        self.assertEqual(2, self.mocked_notification_strategy.notify.call_count)
