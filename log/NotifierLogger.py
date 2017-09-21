import logging
from types import MethodType


class NotifierLogger:
    def __init__(self, function):
        self.function = function

    def __call__(self, notifier, subject, message, recipients):
        notified = self.function(notifier, subject, message, recipients)

        logging.info('[NOTIFICATION] %s', {
            'notified': notified,
            'subject': subject,
            'message': message,
            'recipients': recipients
        })

        return notified

    def __get__(self, notifier, _):
        return MethodType(self, notifier)
