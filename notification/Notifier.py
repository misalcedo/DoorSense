from log.NotifierLogger import NotifierLogger
from stream.TimeWindowStream import TimeWindowStream

_DUPLICATE_NOTIFICATION_RECORD = None


class Notifier:
    def __init__(self, notification_strategy, dedupe_window_in_seconds):
        assert 0 <= dedupe_window_in_seconds

        self.notification_history = TimeWindowStream(dedupe_window_in_seconds)
        self.notification_strategy = notification_strategy

    @NotifierLogger
    def notify(self, subject, message, recipients):
        will_notify = self._notification_count() == 0

        if will_notify:
            self._send_notification(message, recipients, subject)
        else:
            self._ignore_notification()

        return will_notify

    def _notification_count(self):
        count = 0

        for notification in self.notification_history:
            if notification is not _DUPLICATE_NOTIFICATION_RECORD:
                count += 1

        return count

    def _send_notification(self, message, recipients, subject):
        self.notification_strategy.notify(subject, message, recipients)
        self.notification_history.add(self._notification_record(subject, message, recipients))

    @staticmethod
    def _notification_record(subject, message, recipients):
        return {'subject': subject, 'message': message, 'recipients': recipients}

    def _ignore_notification(self):
        self.notification_history.add(_DUPLICATE_NOTIFICATION_RECORD)
