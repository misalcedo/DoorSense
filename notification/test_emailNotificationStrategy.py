from unittest import TestCase
from unittest.mock import patch, Mock

from notification.EmailConfiguration import EmailConfiguration
from notification.EmailNotificationStrategy import EmailNotificationStrategy


class TestEmailNotificationStrategy(TestCase):
    def setUp(self):
        host = 'host'
        port = 1
        timeout = 10
        from_email = 'from_email'
        user = 'user'
        password = 'password'

        self.email_configuration = EmailConfiguration(host, port, timeout, from_email, user, password)
        self.notification_strategy = EmailNotificationStrategy(self.email_configuration)

    @patch('notification.EmailNotificationStrategy.SMTP')
    def test_notify(self, mocked_smtp):
        mocked_smtp_instance = Mock()
        mocked_smtp_instance.__setattr__('__enter__', lambda smtp: mocked_smtp_instance)
        mocked_smtp_instance.__setattr__('__exit__', lambda smtp, exception, value, traceback: None)

        mocked_smtp.return_value = mocked_smtp_instance

        subject = 'subject'
        message = 'message'
        recipients = ['recipient1', 'recipient2']

        self.notification_strategy.notify(subject, message, recipients)

        self.assertEqual(1, mocked_smtp_instance.starttls.call_count)
        self.assertEqual(1, mocked_smtp_instance.send_message.call_count)

        mocked_smtp_instance.login.assert_called_once_with(user=self.email_configuration.user,
                                                           password=self.email_configuration.password)

        mocked_smtp.assert_called_once_with(host=self.email_configuration.host,
                                            port=self.email_configuration.port,
                                            timeout=self.email_configuration.timeout)
