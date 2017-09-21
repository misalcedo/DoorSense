from unittest import TestCase

from notification.EmailConfiguration import EmailConfiguration


class TestEmailConfiguration(TestCase):
    def test___init__(self):
        host = 'host'
        port = 1
        timeout = 10
        from_email = 'from_email'
        user = 'user'
        password = 'password'
        email_configuration = EmailConfiguration(host, port, timeout, from_email, user, password)

        self.assertEqual(host, email_configuration.host)
        self.assertEqual(port, email_configuration.port)
        self.assertEqual(timeout, email_configuration.timeout)
        self.assertEqual(from_email, email_configuration.from_email)
        self.assertEqual(user, email_configuration.user)
        self.assertEqual(password, email_configuration.password)
